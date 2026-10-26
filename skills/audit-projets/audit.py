"""Audit de tous les dépôts git de Rafaël : état git, secrets suivis, failles npm.

Usage : python -I audit.py [--npm] [--racine DOSSIER ...]
Sortie : un tableau Markdown sur la sortie standard.
Les secrets ne sont jamais affichés : seulement le fichier, la ligne et le type.
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

RACINES = [Path.home() / "Documents" / "GitHub", Path.home() / "Documents", Path.home()]
PROPRIOS = ("glm02/",)  # dépôts à soi ; les autres sont des clones de projets tiers

# Motifs de secrets courants. On ne garde que le nom du motif dans le rapport.
MOTIFS = {
    "clé privée": r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----",
    "Stripe live": r"sk_live_[0-9a-zA-Z]{16,}",
    "Resend": r"\bre_[0-9a-zA-Z]{16,}_[0-9a-zA-Z]{8,}",
    "OpenAI/Anthropic": r"\bsk-(proj-|ant-)?[0-9a-zA-Z_-]{32,}",
    "GitHub token": r"\b(ghp|gho|github_pat)_[0-9a-zA-Z_]{30,}",
    "AWS": r"\bAKIA[0-9A-Z]{16}\b",
    "Google API": r"\bAIza[0-9A-Za-z_-]{35}\b",
    "Telegram bot": r"\b\d{8,10}:AA[0-9A-Za-z_-]{33}\b",
    "JWT (service_role ?)": r"\beyJ[0-9A-Za-z_-]{20,}\.eyJ[0-9A-Za-z_-]{40,}\.[0-9A-Za-z_-]{20,}",
}
EXCLUS = re.compile(r"(\.example|\.sample|\.md$|package-lock\.json|pnpm-lock|yarn\.lock|\.min\.js$|/node_modules/)")


def git(rep, *args):
    r = subprocess.run(["git", "-C", str(rep), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip() if r.returncode == 0 else ""


def trouver_depots(racines):
    vus = set()
    for racine in racines:
        if not racine.is_dir():
            continue
        profondeur = 1 if racine == Path.home() else 2
        for d in [racine, *racine.glob("*"), *(racine.glob("*/*") if profondeur > 1 else [])]:
            try:
                if (d / ".git").exists() and d.resolve() not in vus and d.resolve() != Path.home():
                    vus.add(d.resolve())
                    yield d
            except OSError:
                continue


def secrets_suivis(rep):
    trouves = []
    fichiers = git(rep, "ls-files").splitlines()
    for f in fichiers:
        nom = f.replace("\\", "/")
        if re.search(r"(^|/)\.env(\.|$)", nom) and not re.search(r"\.(example|exemple|sample|template)$", nom):
            trouves.append(f"{nom} (fichier .env suivi)")
    for nom_motif, motif in MOTIFS.items():
        sortie = git(rep, "grep", "-n", "-I", "-E", "-o", motif, "--", ".")
        for ligne in sortie.splitlines():
            chemin, num, valeur = ligne.split(":", 2)
            if EXCLUS.search(chemin.replace("\\", "/")):
                continue
            if nom_motif.startswith("JWT"):
                role = role_jwt(valeur)
                if role == "anon":  # clé publique Supabase, prévue pour le navigateur
                    continue
                nom_motif = f"JWT rôle {role}"
            trouves.append(f"{chemin}:{num} ({nom_motif})")
    return sorted(set(trouves))


def role_jwt(jeton):
    """Lit le rôle d'un JWT sans vérifier la signature, pour trier anon / service_role."""
    import base64
    try:
        charge = jeton.split(".")[1]
        charge += "=" * (-len(charge) % 4)
        return json.loads(base64.urlsafe_b64decode(charge)).get("role", "inconnu")
    except (IndexError, ValueError):
        return "illisible"


def failles_npm(rep):
    if not (rep / "package-lock.json").exists():
        return "-"
    r = subprocess.run("npm audit --json --omit=dev", cwd=rep, capture_output=True, text=True, shell=True, encoding="utf-8", errors="replace")
    try:
        v = json.loads(r.stdout)["metadata"]["vulnerabilities"]
        return f"{v.get('critical', 0)} crit / {v.get('high', 0)} haute"
    except (ValueError, KeyError):
        return "?"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--npm", action="store_true", help="lancer npm audit sur ses propres dépôts (lent)")
    p.add_argument("--racine", nargs="*", type=Path)
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    lignes, alertes = [], []
    for rep in sorted(trouver_depots(a.racine or RACINES), key=lambda d: d.name.lower()):
        origine = git(rep, "remote", "get-url", "origin").replace("https://github.com/", "").removesuffix(".git")
        a_soi = origine.startswith(PROPRIOS) or not origine
        modifs = len(git(rep, "status", "--porcelain").splitlines())
        en_avance = git(rep, "rev-list", "--count", "@{u}..HEAD") or ("pas de suivi" if origine else "pas de remote")
        dernier = git(rep, "log", "-1", "--format=%cs")
        secrets = secrets_suivis(rep) if a_soi else []
        npm = failles_npm(rep) if (a.npm and a_soi) else ""
        lignes.append(f"| {rep.name} | {'à soi' if a_soi else 'tiers'} | {git(rep, 'branch', '--show-current')} | {modifs} | {en_avance} | {dernier} | {len(secrets)} | {npm} |")
        for s in secrets:
            alertes.append(f"- `{rep.name}` : {s}")

    print("| Dépôt | Type | Branche | Fichiers modifiés | Commits non poussés | Dernier commit | Secrets suivis | npm audit |")
    print("|---|---|---|---|---|---|---|---|")
    print("\n".join(lignes))
    print("\n## Secrets ou .env suivis par git\n")
    print("\n".join(alertes) if alertes else "Aucun.")


if __name__ == "__main__":
    main()
