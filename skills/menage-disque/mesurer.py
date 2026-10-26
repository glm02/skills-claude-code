"""Ce qui prend de la place sur le disque C:, et ce qui se nettoie sans risque.

Usage : python mesurer.py [--min-go 1]
Lecture seule : le script ne supprime rien. Il classe :
  - caches régénérables (npm, pip, uv, navigateurs Playwright, Temp…) ;
  - gros dossiers du profil et de Program Files (≥ --min-go) ;
  - node_modules et .next des projets (régénérés par npm install / build).
"""
import argparse, os, shutil, sys
from pathlib import Path

H = Path.home()
LOCAL = Path(os.environ.get("LOCALAPPDATA", H / "AppData/Local"))
ROAMING = Path(os.environ.get("APPDATA", H / "AppData/Roaming"))

# Emplacement → (nom, comment le vider proprement)
CACHES = {
    LOCAL / "Temp": ("Fichiers temporaires", "supprimer le contenu (fichiers en cours d'usage ignorés)"),
    LOCAL / "npm-cache": ("Cache npm", "npm cache clean --force"),
    LOCAL / "pip/Cache": ("Cache pip", "pip cache purge"),
    LOCAL / "uv/cache": ("Cache uv", "uv cache clean"),
    LOCAL / "pnpm/store": ("Store pnpm", "pnpm store prune"),
    LOCAL / "ms-playwright": ("Navigateurs Playwright", "garder la version utilisée, supprimer les anciennes"),
    LOCAL / "Yarn/Cache": ("Cache Yarn", "yarn cache clean"),
    H / ".cache": ("Caches divers (~/.cache)", "regarder par sous-dossier"),
    H / ".gradle/caches": ("Cache Gradle", "supprimer, régénéré au build"),
    H / ".m2/repository": ("Dépôt Maven", "supprimer, régénéré au build"),
    LOCAL / "Docker": ("Docker", "docker system prune (avec accord)"),
    LOCAL / "CrashDumps": ("Rapports de plantage", "supprimer"),
    LOCAL / "Microsoft/Windows/INetCache": ("Cache web Windows", "Nettoyage de disque Windows"),
    Path("C:/Windows/SoftwareDistribution/Download"): ("Mises à jour Windows téléchargées", "Nettoyage de disque → fichiers système (admin)"),
    Path("C:/$Recycle.Bin"): ("Corbeille", "vider la corbeille"),
}


def taille(p: Path) -> int:
    total = 0
    pile = [p]
    while pile:
        d = pile.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            pile.append(e.path)
                        else:
                            total += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return total


def go(n):
    return f"{n / 1024**3:6.1f} Go"


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--min-go", type=float, default=1.0)
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    seuil = o.min_go * 1024**3

    u = shutil.disk_usage("C:/")
    print(f"Disque C: {go(u.used).strip()} utilisés sur {go(u.total).strip()}, {go(u.free).strip()} libres\n")

    print("== Caches régénérables")
    total_caches = 0
    for p, (nom, comment) in CACHES.items():
        if p.exists():
            t = taille(p)
            total_caches += t
            if t > 200 * 1024**2:
                print(f"{go(t)}  {nom} — {comment}  [{p}]")
    print(f"{go(total_caches)}  au total\n")

    print("== node_modules et .next des projets (régénérables)")
    regen = []
    for racine in (H / "Documents", H / "orca", H):
        if not racine.exists():
            continue
        profondeur_max = 2 if racine == H else 4
        for dossier, sous, _ in os.walk(racine):
            niveau = len(Path(dossier).relative_to(racine).parts)
            if niveau >= profondeur_max or "AppData" in dossier:
                sous[:] = []
                continue
            for s in list(sous):
                if s in ("node_modules", ".next", ".turbo", "dist", ".venv"):
                    regen.append(Path(dossier) / s)
                    sous.remove(s)
    regen = sorted({(taille(p), p) for p in set(regen)}, reverse=True)
    for t, p in regen[:15]:
        if t > 300 * 1024**2:
            print(f"{go(t)}  {p}")
    print(f"{go(sum(t for t, _ in regen))}  au total\n")

    print(f"== Gros dossiers (≥ {o.min_go} Go)")
    candidats = [H / d for d in os.listdir(H) if (H / d).is_dir() and d not in ("AppData",)]
    candidats += [LOCAL / d for d in os.listdir(LOCAL) if (LOCAL / d).is_dir()]
    candidats += [ROAMING / d for d in os.listdir(ROAMING) if (ROAMING / d).is_dir()]
    candidats += [Path("C:/ProgramData") / d for d in os.listdir("C:/ProgramData") if (Path("C:/ProgramData") / d).is_dir()]
    for pf in ("C:/Program Files", "C:/Program Files (x86)"):
        candidats += [Path(pf) / d for d in os.listdir(pf) if (Path(pf) / d).is_dir()]
    deja = set(CACHES)
    gros = sorted(((taille(p), p) for p in candidats if p not in deja), reverse=True)
    for t, p in gros:
        if t >= seuil:
            print(f"{go(t)}  {p}")


if __name__ == "__main__":
    main()
