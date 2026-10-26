"""Contrôles et dossier de fabrication d'un projet KiCad, en une commande.

Usage : python fabrication.py <dossier-du-projet ou fichier .kicad_pro> [--sortie DOSSIER] [--sans-controle]

Fait, avec kicad-cli (KiCad 10) :
  1. ERC du schéma et DRC du circuit (avec parité schéma/PCB) → nombre
     d'erreurs et d'avertissements, rapports JSON ;
  2. Gerber + perçages (format attendu par JLCPCB / PCBWay) dans un zip ;
  3. nomenclature (BOM) CSV, schéma en PDF, position des composants (CPL).
Rien n'est écrit dans le dossier du projet si --sortie est donné ; par défaut
la sortie va dans <projet>/fabrication/<date>/.
"""
import argparse, datetime, json, shutil, subprocess, sys, zipfile
from pathlib import Path

CLI_CANDIDATS = [
    Path.home() / "AppData/Local/Programs/KiCad/10.0/bin/kicad-cli.exe",
    Path("C:/Program Files/KiCad/10.0/bin/kicad-cli.exe"),
    Path.home() / "AppData/Local/Programs/KiCad/9.0/bin/kicad-cli.exe",
]


def cli():
    for c in CLI_CANDIDATS:
        if c.exists():
            return str(c)
    return shutil.which("kicad-cli") or sys.exit("kicad-cli introuvable : installer KiCad 10.")


def lancer(*args):
    r = subprocess.run([cli(), *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode not in (0, 5):  # 5 = violations trouvées (ERC/DRC avec --exit-code-violations)
        print(f"échec : {' '.join(map(str, args[:3]))}\n{r.stderr.strip()[-600:]}")
    return r.returncode


def compter(rapport):
    d = json.loads(Path(rapport).read_text(encoding="utf-8"))
    violations = [v for s in d.get("sheets", [{}]) for v in s.get("violations", [])] + d.get("violations", []) \
        + d.get("unconnected_items", []) + d.get("schematic_parity", [])
    err = sum(1 for v in violations if v.get("severity") == "error")
    types = {}
    for v in violations:
        types[v.get("type", "?")] = types.get(v.get("type", "?"), 0) + 1
    return err, len(violations) - err, sorted(types.items(), key=lambda t: -t[1])[:6]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("projet", type=Path)
    a.add_argument("--sortie", type=Path)
    a.add_argument("--sans-controle", action="store_true")
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    pro = o.projet if o.projet.suffix == ".kicad_pro" else next(o.projet.glob("*.kicad_pro"), None)
    if not pro:
        sys.exit("Aucun .kicad_pro dans ce dossier.")
    sch, pcb = pro.with_suffix(".kicad_sch"), pro.with_suffix(".kicad_pcb")
    out = o.sortie or pro.parent / "fabrication" / datetime.date.today().isoformat()
    (out / "gerber").mkdir(parents=True, exist_ok=True)
    print(f"Projet {pro.stem} → {out}")

    if not o.sans_controle:
        if sch.exists():
            lancer("sch", "erc", "--format", "json", "--severity-all", "-o", out / "erc.json", sch)
            e, w, t = compter(out / "erc.json")
            print(f"ERC : {e} erreur(s), {w} avertissement(s)" + (f" — {t}" if t else ""))
        if pcb.exists():
            lancer("pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity", "-o", out / "drc.json", pcb)
            e, w, t = compter(out / "drc.json")
            print(f"DRC : {e} erreur(s), {w} avertissement(s)" + (f" — {t}" if t else ""))

    if sch.exists():
        lancer("sch", "export", "pdf", "-o", out / f"{pro.stem}-schema.pdf", sch)
        lancer("sch", "export", "bom", "--fields", "Reference,Value,Footprint,${QUANTITY},${DNP}",
               "--labels", "Repère,Valeur,Empreinte,Quantité,Non monté", "--group-by", "Value,Footprint",
               "-o", out / f"{pro.stem}-bom.csv", sch)
        bom = out / f"{pro.stem}-bom.csv"
        if bom.exists():  # BOM UTF-8 avec signature : Excel lit alors les accents correctement
            bom.write_text(bom.read_text(encoding="utf-8"), encoding="utf-8-sig")
    if pcb.exists():
        # Seulement les couches qu'un fabricant utilise, cuivres internes compris.
        texte = pcb.read_text(encoding="utf-8", errors="replace")
        internes = sorted({f"In{n}.Cu" for n in range(1, 31) if f'"In{n}.Cu"' in texte}, key=lambda c: int(c[2:-3]))
        couches = ["F.Cu", *internes, "B.Cu", "F.Mask", "B.Mask", "F.Silkscreen", "B.Silkscreen", "F.Paste", "B.Paste", "Edge.Cuts"]
        lancer("pcb", "export", "gerbers", "--layers", ",".join(couches), "-o", out / "gerber", pcb)
        lancer("pcb", "export", "drill", "--format", "excellon", "-o", str(out / "gerber") + "/", pcb)
        lancer("pcb", "export", "pos", "--format", "csv", "--units", "mm", "--side", "both", "-o", out / f"{pro.stem}-cpl.csv", pcb)
        z = out / f"{pro.stem}-gerber.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
            for g in (out / "gerber").iterdir():
                f.write(g, g.name)
        print(f"Gerber : {len(list((out / 'gerber').iterdir()))} fichiers → {z.name}")
    print("Fichiers : " + ", ".join(sorted(p.name for p in out.iterdir() if p.is_file())))


if __name__ == "__main__":
    main()
