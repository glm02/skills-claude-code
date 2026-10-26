"""Analyse de sécurité d'un dépôt GitHub (ou d'un dossier) AVANT de l'utiliser.

Usage :
  python analyser.py https://github.com/owner/repo     # clone en quarantaine puis analyse
  python analyser.py owner/repo
  python analyser.py <dossier-local>                    # analyse un dossier déjà présent
  options : --json (rapport machine), --garder (ne pas supprimer un dépôt ROUGE)

Rien du dépôt n'est exécuté : clone sans sous-modules ni liens symboliques,
puis lecture des fichiers comme du texte. Verdict :
  VERT   rien de suspect trouvé (ce n'est pas une garantie absolue) ;
  ORANGE des points à relire à la main avant tout usage ;
  ROUGE  comportement typique d'un logiciel malveillant : ne pas utiliser.
Le dépôt reste dans ~/quarantaine-repos/<owner>__<repo> ; le rapport y est
écrit dans .analyse-securite.json (avec le commit analysé).
"""
import argparse, datetime as dt, json, math, os, re, shutil, subprocess, sys, urllib.request
from collections import Counter
from pathlib import Path

QUARANTAINE = Path.home() / "quarantaine-repos"
TAILLE_MAX_LECTURE = 2 * 1024 * 1024
DOSSIERS_IGNORES = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next"}

# (gravité, nom, motif) — gravité : 3 = ROUGE, 2 = ORANGE, 1 = à noter
MOTIFS = [
    # Vol de données : navigateurs, portefeuilles, messageries, clés
    # Un vrai chemin de profil de navigateur, pas le simple mot « Cookies » d'un en-tête HTTP.
    (3, "lecture des mots de passe / cookies des navigateurs", r"(Google[\\/]+Chrome|Microsoft[\\/]+Edge|BraveSoftware|Opera Software|Chromium)[^\n]{0,60}User Data|User Data[\\/]+(Default|Profile \d+)[\\/]+(Login Data|Network[\\/]+Cookies|Web Data)|Mozilla[\\/]+Firefox[\\/]+Profiles|\blogins\.json\b|\bkey4\.db\b"),
    # Chemins et identifiants d'extensions de portefeuilles, pas les simples mots (« phantom » est courant).
    (3, "accès aux portefeuilles crypto", r"(Exodus[\\/]+exodus\.wallet|Electrum[\\/]+wallets|atomic[\\/]+Local Storage|Coinomi[\\/]+Coinomi|wallet\.dat\b|nkbihfbeogaeaoehlefnkodbefgpgknn|bfnaelmomeimhlpmgjnjophhpkkoljpa|ejbalbakoplchlghecdalmeeeajnimhm|hnfanknocfeofbddgcijnmhnfnkdnaad)"),
    (3, "vol de session Discord / Telegram", r"(discord(app)?[\\/]+Local Storage|leveldb.*discord|tdata[\\/]|Telegram Desktop[\\/]+tdata)"),
    (3, "envoi vers un webhook Discord", r"discord(app)?\.com/api/webhooks/"),
    (2, "envoi vers un bot Telegram codé en dur", r"api\.telegram\.org/bot\d{6,}:"),
    (2, "lecture des clés SSH ou des identifiants cloud", r"\.ssh[\\/]+id_(rsa|ed25519)|\.aws[\\/]+credentials|\.config[\\/]+gcloud|\.kube[\\/]+config"),
    # Exécution cachée / téléchargement d'une charge
    (3, "PowerShell encodé", r"powershell[^\n]{0,80}-(e|en|enc|encodedcommand)\s+[A-Za-z0-9+/=]{20,}"),
    (3, "téléchargement puis exécution PowerShell", r"(IEX|Invoke-Expression)\s*\(?\s*(New-Object\s+Net\.WebClient|\(?iwr|\(?irm|Invoke-WebRequest|Invoke-RestMethod)|DownloadString\s*\(|DownloadFile\s*\([^)]*\.(exe|dll|ps1|bat|scr)"),
    (3, "téléchargement d'un exécutable puis lancement", r"(curl|wget|Invoke-WebRequest|urllib|requests\.get|fetch)\b[^\n]{0,200}\.(exe|scr|msi|dll|bat|vbs)\b[^\n]{0,200}(start|Start-Process|os\.startfile|subprocess|exec|spawn|chmod \+x)"),
    (2, "script distant exécuté directement (curl | sh)", r"(curl|wget)\s[^\n|]{0,200}\|\s*(sudo\s+)?(ba|z)?sh\b|(irm|iwr)\s[^\n|]{0,200}\|\s*iex"),
    (3, "code décodé puis exécuté (base64 → eval/exec)", r"(eval|exec|Function)\s*\(\s*(atob|Buffer\.from|base64\.b64decode|bytes\.fromhex|codecs\.decode|zlib\.decompress|marshal\.loads)"),
    (2, "exécution de code dynamique", r"\beval\s*\(\s*(require|fetch|await|request|http)|new Function\s*\(\s*['\"`]?return|exec\s*\(\s*requests\.get|exec\s*\(\s*urlopen"),
    (2, "chaîne base64 très longue", r"['\"`][A-Za-z0-9+/]{400,}={0,2}['\"`]"),
    # Persistance / désactivation de la sécurité Windows
    (3, "désactivation ou exclusion de l'antivirus", r"Add-MpPreference\s+-Exclusion|Set-MpPreference\s+-Disable|DisableRealtimeMonitoring|DisableAntiSpyware"),
    # Démarrage automatique : fréquent chez les logiciels légitimes (services, auto-start), à relire au cas par cas.
    (2, "lancement automatique au démarrage de Windows",r"CurrentVersion\\\\?Run\b|Start Menu\\\\?Programs\\\\?Startup|schtasks\s+/create|New-ScheduledTask|Register-ScheduledTask"),
    (2, "élévation / contournement UAC", r"fodhelper|eventvwr\.exe|ComputerDefaults|bypassuac|-Verb\s+RunAs"),
    # Réseau suspect
    (2, "hébergement de charge ou tunnel", r"pastebin\.com/raw|transfer\.sh|anonfiles|gofile\.io|ngrok\.io|trycloudflare\.com|raw\.githubusercontent\.com/[^\s'\"]+\.(exe|ps1|bat|dll)"),
    (1, "adresse IP codée en dur", r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?/"),
    # Attaques visant les assistants de code (Claude, Cursor, Copilot)
    (2, "instruction cachée pour une IA", r"(ignore (all |the )?(previous|prior|above) instructions|disregard (your|the) (system|previous)|you are now|do not (tell|inform) the user|sans (le dire|prévenir) (à )?l'utilisateur)"),
]

# Fichiers qui s'exécutent tout seuls (installation, ouverture du dossier, assistant de code)
AUTO_EXEC = {
    "package.json": "scripts npm",
    ".vscode/tasks.json": "tâche VS Code",
    ".devcontainer/devcontainer.json": "commandes du devcontainer",
    ".claude/settings.json": "hooks Claude Code",
    ".claude/settings.local.json": "hooks Claude Code",
    ".mcp.json": "serveurs MCP lancés par Claude",
    ".cursor/mcp.json": "serveurs MCP de Cursor",
    "setup.py": "installation Python",
    ".npmrc": "configuration npm",
    ".gitattributes": "filtres git",
}
EXT_BINAIRES = {".exe", ".dll", ".scr", ".msi", ".com", ".bat", ".cmd", ".vbs", ".vbe", ".js.lnk", ".lnk", ".hta", ".jar", ".ps1", ".pif", ".cpl", ".sys"}
ARCHIVES = {".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".img"}
EXT_TEXTE = {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py", ".ps1", ".psm1", ".bat", ".cmd", ".sh", ".bash", ".vbs", ".rb", ".php",
             ".go", ".rs", ".java", ".cs", ".json", ".yml", ".yaml", ".toml", ".md", ".txt", ".html", ".htm", ".cfg", ".ini", ".lua", ""}
POPULAIRES = ["react", "lodash", "express", "axios", "chalk", "commander", "request", "moment", "dotenv", "webpack", "typescript", "next",
              "vue", "eslint", "prettier", "requests", "numpy", "pandas", "flask", "django", "colorama", "urllib3", "selenium", "discord.js",
              "discord.py", "pycryptodome", "cryptography", "electron", "puppeteer", "playwright", "tailwindcss", "vite", "openai", "anthropic"]


def lev(a, b):
    """Distance d'édition, une inversion de deux lettres voisines comptant pour 1 (axois ≈ axios)."""
    if abs(len(a) - len(b)) > 1:
        return 2
    if len(a) == len(b):
        ecarts = [i for i in range(len(a)) if a[i] != b[i]]
        if len(ecarts) == 2 and ecarts[1] == ecarts[0] + 1 and a[ecarts[0]] == b[ecarts[1]] and a[ecarts[1]] == b[ecarts[0]]:
            return 1
    prec = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prec[j] + 1, cur[j - 1] + 1, prec[j - 1] + (ca != cb)))
        prec = cur
    return prec[-1]


def entropie(s):
    c = Counter(s)
    return -sum(n / len(s) * math.log2(n / len(s)) for n in c.values()) if s else 0


def cloner(cible):
    m = re.match(r"^(?:https?://github\.com/|git@github\.com:)?([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", cible)
    if not m:
        sys.exit("Adresse non reconnue : donner https://github.com/owner/repo ou owner/repo.")
    owner, repo = m.groups()
    dest = QUARANTAINE / f"{owner}__{repo}"
    if dest.exists():
        shutil.rmtree(dest, onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
    QUARANTAINE.mkdir(exist_ok=True)
    # Pas de sous-modules, pas de liens symboliques, protections NTFS : rien ne s'exécute au clone.
    r = subprocess.run(["git", "-c", "core.symlinks=false", "-c", "core.protectNTFS=true", "-c", "protocol.file.allow=never",
                        "-c", "core.hooksPath=" + os.devnull, "clone", "--depth", "1", "--no-recurse-submodules",
                        f"https://github.com/{owner}/{repo}.git", str(dest)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Clone impossible : {r.stderr.strip()[-300:]}")
    return owner, repo, dest


def fiche_github(owner, repo):
    """Réputation du dépôt et de son auteur, via gh (déjà connecté) ou l'API publique."""
    def api(chemin):
        if shutil.which("gh"):
            r = subprocess.run(["gh", "api", chemin], capture_output=True, text=True, encoding="utf-8")
            if r.returncode == 0:
                return json.loads(r.stdout)
        req = urllib.request.Request(f"https://api.github.com/{chemin}", headers={"User-Agent": "agent-local"})
        with urllib.request.urlopen(req, timeout=20) as f:
            return json.load(f)
    try:
        d = api(f"repos/{owner}/{repo}")
        u = api(f"users/{owner}")
    except Exception as e:
        return {"erreur": str(e)[:120]}
    age = lambda s: (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(s.replace("Z", "+00:00"))).days
    return {"etoiles": d.get("stargazers_count"), "forks": d.get("forks_count"), "issues": d.get("open_issues_count"),
            "licence": (d.get("license") or {}).get("spdx_id"), "archive": d.get("archived"), "fork": d.get("fork"),
            "cree_il_y_a_jours": age(d["created_at"]), "pousse_il_y_a_jours": age(d["pushed_at"]),
            "auteur_type": u.get("type"), "auteur_cree_il_y_a_jours": age(u["created_at"]), "auteur_depots": u.get("public_repos"),
            "auteur_abonnes": u.get("followers")}


def analyser(racine: Path):
    alertes = []  # (gravité, catégorie, fichier, détail)
    ajouter = lambda g, cat, f, det: alertes.append((g, cat, str(f).replace("\\", "/"), det[:160]))
    nb_fichiers = 0
    for dossier, sous, fichiers in os.walk(racine):
        sous[:] = [s for s in sous if s not in DOSSIERS_IGNORES]
        for nom in fichiers:
            p = Path(dossier) / nom
            rel = p.relative_to(racine)
            relp = str(rel).replace("\\", "/")
            nb_fichiers += 1
            ext = "".join(p.suffixes[-2:]).lower() if p.suffix.lower() == ".lnk" else p.suffix.lower()
            try:
                taille = p.stat().st_size
                debut = p.open("rb").read(4)
            except OSError:
                continue
            if ext in EXT_BINAIRES or debut[:2] == b"MZ":
                ajouter(3 if debut[:2] == b"MZ" or ext in {".exe", ".scr", ".dll", ".hta", ".pif", ".cpl"} else 2,
                        "exécutable ou script Windows fourni", rel, f"{taille // 1024} Ko")
            if ext in ARCHIVES:
                ajouter(2, "archive fournie (contenu invisible)", rel, f"{taille // 1024} Ko")
            if relp in AUTO_EXEC or relp.endswith("/package.json") and "node_modules" not in relp:
                verifier_auto(p, relp, ajouter)
            if taille > TAILLE_MAX_LECTURE or (ext not in EXT_TEXTE and debut[:2] != b"#!"):
                continue
            try:
                texte = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if re.search(r"[‪-‮⁦-⁩]", texte):
                ajouter(3, "caractères invisibles qui inversent le texte (Trojan Source)", rel, "bidi")
            if ext in {".md", ".txt", ""} or nom.upper() in {"CLAUDE.MD", "AGENTS.MD", ".CURSORRULES"}:
                if re.search(r"[​-‏⁠﻿\U000e0000-\U000e007f]", texte[1:]):
                    ajouter(2, "texte invisible dans un fichier d'instructions", rel, "caractères zéro-largeur ou balises")
            # Le code de test ne s'exécute pas à l'installation et manipule ces cas exprès : un cran de moins.
            de_test = bool(re.search(r"(^|/)(tests?|__tests__|spec|fixtures|examples?|docs?)/|(^|/)test_|[._](test|spec)\.", relp, re.I))
            for grav, nom_motif, motif in MOTIFS:
                m = re.search(motif, texte, re.I)
                if m:
                    ligne = texte.count("\n", 0, m.start()) + 1
                    g = max(1, grav - 1) if de_test else grav
                    ajouter(g, nom_motif + (" (fichier de test)" if de_test else ""), f"{rel}:{ligne}", m.group(0).replace("\n", " "))
            if ext in {".js", ".py", ".ps1", ".ts", ".cjs", ".mjs"} and not re.search(r"\.min\.|dist/|vendor/", relp):
                longues = [l for l in texte.splitlines() if len(l) > 3000]
                if longues and entropie(longues[0][:5000]) > 5.2:
                    ajouter(2, "code obfusqué (ligne très longue et aléatoire)", rel, f"{len(longues[0])} caractères")
                if texte.count("\n") > 3 and re.search(r"^\s{150,}\S", texte, re.M):
                    ajouter(3, "code caché après des centaines d'espaces", rel, "décalage horizontal")
    return alertes, nb_fichiers


def verifier_auto(p, relp, ajouter):
    try:
        texte = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if relp.endswith("package.json"):
        try:
            j = json.loads(texte)
        except ValueError:
            return
        for cle in ("preinstall", "install", "postinstall", "prepare", "preuninstall", "postuninstall"):
            if cle in j.get("scripts", {}):
                ajouter(2, "script lancé automatiquement par npm install", relp, f"{cle}: {j['scripts'][cle]}")
        deps = {**j.get("dependencies", {}), **j.get("devDependencies", {}), **j.get("optionalDependencies", {})}
        for nom, version in deps.items():
            if re.match(r"(git\+|https?://|github:|[\w-]+/[\w.-]+$|file:)", str(version)):
                ajouter(2, "dépendance hors registre npm", relp, f"{nom}: {version}")
            for pop in POPULAIRES:
                if nom != pop and lev(nom, pop) == 1 and len(pop) > 3:
                    ajouter(3, "nom de paquet imitant un paquet connu (typosquatting)", relp, f"{nom} ≈ {pop}")
    elif relp in (".claude/settings.json", ".claude/settings.local.json"):
        if '"hooks"' in texte:
            ajouter(3, "le dépôt définit des hooks Claude Code (commandes lancées à l'ouverture)", relp, "hooks")
        if re.search(r'"(allow|defaultMode)"', texte):
            ajouter(2, "le dépôt élargit les permissions de Claude Code", relp, "permissions")
    elif relp in (".mcp.json", ".cursor/mcp.json"):
        ajouter(2, "le dépôt déclare des serveurs MCP (programmes lancés par l'assistant)", relp, texte[:120].replace("\n", " "))
    elif relp == ".vscode/tasks.json" and "folderOpen" in texte:
        ajouter(3, "tâche VS Code lancée à l'ouverture du dossier", relp, "runOn: folderOpen")
    elif relp == ".devcontainer/devcontainer.json" and re.search(r"(postCreate|postStart|initialize)Command", texte):
        ajouter(2, "commandes lancées par le devcontainer", relp, "postCreate/initializeCommand")
    elif relp == "setup.py" and re.search(r"cmdclass|os\.system|subprocess|urlopen|requests", texte):
        ajouter(2, "setup.py exécute du code à l'installation", relp, "cmdclass/subprocess")
    elif relp == ".npmrc" and re.search(r"registry\s*=|ignore-scripts\s*=\s*false", texte):
        ajouter(2, "registre npm ou scripts imposés par le dépôt", relp, texte[:100])
    elif relp == ".gitattributes" and "filter=" in texte:
        ajouter(1, "filtre git déclaré", relp, "filter=")


def verdict(alertes, fiche):
    pire = max((g for g, *_ in alertes), default=0)
    raisons = []
    if fiche and "erreur" not in fiche:
        if fiche["auteur_cree_il_y_a_jours"] < 60 and (fiche["etoiles"] or 0) > 50:
            raisons.append("compte auteur récent mais beaucoup d'étoiles (étoiles achetées ?)")
            pire = max(pire, 2)
        if fiche["auteur_cree_il_y_a_jours"] < 30:
            raisons.append("compte auteur créé il y a moins d'un mois")
            pire = max(pire, 2)
        if (fiche["etoiles"] or 0) > 200 and (fiche["issues"] or 0) == 0 and (fiche["forks"] or 0) < 5:
            raisons.append("beaucoup d'étoiles mais ni issue ni fork : popularité artificielle probable")
            pire = max(pire, 2)
    return {3: "ROUGE", 2: "ORANGE"}.get(pire, "VERT"), raisons


def main():
    a = argparse.ArgumentParser()
    a.add_argument("cible")
    a.add_argument("--json", action="store_true")
    a.add_argument("--garder", action="store_true")
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    if Path(o.cible).is_dir():
        racine, fiche, nom = Path(o.cible).resolve(), None, Path(o.cible).name
    else:
        owner, repo, racine = cloner(o.cible)
        fiche, nom = fiche_github(owner, repo), f"{owner}/{repo}"
    commit = subprocess.run(["git", "-C", str(racine), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    alertes, nb = analyser(racine)
    couleur, raisons = verdict(alertes, fiche)
    rapport = {"depot": nom, "dossier": str(racine), "commit": commit, "date": dt.datetime.now().isoformat(timespec="seconds"),
               "verdict": couleur, "reputation": fiche, "raisons_reputation": raisons, "fichiers_lus": nb,
               "alertes": [{"gravite": g, "type": c, "ou": f, "extrait": d} for g, c, f, d in sorted(alertes, reverse=True)]}
    (racine / ".analyse-securite.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    if o.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print(f"Dépôt {nom} · commit {commit[:10]} · {nb} fichiers lus")
        if fiche and "erreur" not in fiche:
            print(f"Réputation : {fiche['etoiles']} étoiles, {fiche['forks']} forks, {fiche['issues']} issues, licence {fiche['licence']}, "
                  f"dépôt créé il y a {fiche['cree_il_y_a_jours']} j, compte auteur ({fiche['auteur_type']}) créé il y a {fiche['auteur_cree_il_y_a_jours']} j")
        for r in raisons:
            print(f"  ! {r}")
        noms = {3: "ROUGE ", 2: "ORANGE", 1: "note  "}
        for g, c, f, d in sorted(alertes, reverse=True)[:40]:
            print(f"  {noms[g]} {c} — {f} — {d}")
        if len(alertes) > 40:
            print(f"  … {len(alertes) - 40} autres dans .analyse-securite.json")
        print(f"\nVERDICT : {couleur}")
    if couleur == "ROUGE" and not o.garder and not Path(o.cible).is_dir():
        shutil.rmtree(racine, onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
        print("Dépôt ROUGE supprimé de la quarantaine (relancer avec --garder pour l'examiner).")


if __name__ == "__main__":
    main()
