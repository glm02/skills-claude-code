"""Temps passé par projet, d'après les sessions Claude Code et les commits git.

Usage : python bilan.py [--depuis 2026-10-01] [--jusqu 2026-10-31] [--projet atout] [--pause 45]

Une « plage de travail » regroupe les messages de Rafaël espacés de moins de
--pause minutes ; chaque plage compte au moins 15 min. Les sessions des
worktrees Orca d'un même projet sont regroupées sous le nom du projet.
C'est une estimation du temps de présence, à présenter comme telle.
"""
import argparse, datetime as dt, glob, json, os, re, sys
from collections import defaultdict
from pathlib import Path

BASE = Path.home() / ".claude" / "projects"


def nom_projet(dossier: str) -> str:
    """c--Users-rafae-Documents-GitHub-Atout-travaux → atout-travaux ;
    C--Users-rafae-orca-workspaces-Atout-travaux-seabiscuit → atout-travaux."""
    n = re.sub(r"^[cC]--Users-[^-]+-?", "", dossier)
    if n.startswith("orca-workspaces-"):
        # orca-workspaces-<dépôt>-<worktree> : on garde le dépôt, connu par le dossier d'Orca.
        reste = n[len("orca-workspaces-"):].lower()
        depots = Path.home() / "orca" / "workspaces"
        noms = sorted((re.sub(r"[^a-z0-9]+", "-", d.name.lower()) for d in depots.iterdir() if d.is_dir()), key=len, reverse=True) if depots.exists() else []
        n = next((d for d in noms if reste == d or reste.startswith(d + "-")), reste)
    n = re.sub(r"^(Documents-GitHub-|Documents-)", "", n).lower()
    n = re.sub(r"^stagebot-stagebot$", "stagebot", n)
    return "accueil" if n in ("", "rafae") else n


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--depuis", default=(dt.date.today() - dt.timedelta(days=30)).isoformat())
    a.add_argument("--jusqu", default=dt.date.today().isoformat())
    a.add_argument("--projet", default="")
    a.add_argument("--pause", type=int, default=45)
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    debut = dt.datetime.fromisoformat(o.depuis).replace(tzinfo=dt.timezone.utc)
    fin = dt.datetime.fromisoformat(o.jusqu).replace(tzinfo=dt.timezone.utc) + dt.timedelta(days=1)

    instants = defaultdict(list)
    for f in glob.glob(str(BASE / "*" / "*.jsonl")):
        projet = nom_projet(Path(f).parent.name)
        if o.projet and o.projet.lower() not in projet:
            continue
        for ligne in open(f, encoding="utf-8", errors="replace"):
            if '"type":"user"' not in ligne.replace(" ", ""):
                continue
            try:
                e = json.loads(ligne)
                t = dt.datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
            except (ValueError, KeyError):
                continue
            if debut <= t < fin:
                instants[projet].append(t)

    pause = dt.timedelta(minutes=o.pause)
    lignes, total = [], dt.timedelta()
    par_jour = defaultdict(dt.timedelta)
    for projet, ts in instants.items():
        ts.sort()
        duree, jours = dt.timedelta(), set()
        d0 = prec = ts[0]
        for t in ts[1:] + [None]:
            if t is None or t - prec > pause:
                plage = max(prec - d0, dt.timedelta(minutes=15))
                duree += plage
                par_jour[d0.astimezone().date()] += plage
                jours.add(d0.astimezone().date())
                if t is not None:
                    d0 = t
            if t is not None:
                prec = t
        total += duree
        lignes.append((duree, projet, len(jours), ts[0].astimezone().date(), ts[-1].astimezone().date()))

    h = lambda d: f"{d.total_seconds() / 3600:5.1f} h"
    print(f"Période {o.depuis} → {o.jusqu} (pause > {o.pause} min = nouvelle plage)\n")
    print("| Projet | Temps | Jours actifs | Du | Au |\n|---|---|---|---|---|")
    for duree, projet, nj, d1, d2 in sorted(lignes, reverse=True):
        print(f"| {projet} | {h(duree).strip()} | {nj} | {d1} | {d2} |")
    print(f"\nTotal : {h(total).strip()} sur {len(par_jour)} jours actifs")


if __name__ == "__main__":
    main()
