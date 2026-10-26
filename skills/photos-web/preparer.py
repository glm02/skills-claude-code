"""Prépare un lot de photos pour un site : retire les métadonnées (GPS, appareil,
date), applique l'orientation, redimensionne, exporte en WebP et JPEG.

Usage : python -I preparer.py <dossier-source> <dossier-sortie> [--largeur 1600] [--qualite 80]

Pourquoi : des photos de téléphone publiées telles quelles donnent l'adresse
exacte du chantier ou du domicile (coordonnées GPS dans l'EXIF). Ici rien ne
sort avec ses métadonnées, et les originaux ne sont jamais modifiés.
"""
import argparse, sys
from pathlib import Path
from PIL import Image, ImageOps

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}
GPS_IFD = 0x8825


def nom_propre(p: Path) -> str:
    """Nom de fichier sans espaces ni accents, pour des URL lisibles."""
    import unicodedata, re
    s = unicodedata.normalize("NFKD", p.stem).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "photo"


def main():
    a = argparse.ArgumentParser()
    a.add_argument("source", type=Path)
    a.add_argument("sortie", type=Path)
    a.add_argument("--largeur", type=int, default=1600)
    a.add_argument("--qualite", type=int, default=80)
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if o.sortie.resolve() == o.source.resolve():
        sys.exit("La sortie doit être un autre dossier : les originaux ne sont jamais écrasés.")
    o.sortie.mkdir(parents=True, exist_ok=True)

    fichiers = sorted(p for p in o.source.rglob("*") if p.suffix.lower() in EXTENSIONS)
    avec_gps, total_avant, total_apres, noms = 0, 0, 0, set()
    for p in fichiers:
        try:
            img = Image.open(p)
        except Exception as e:  # HEIC sans greffon, fichier corrompu
            print(f"ignorée : {p.name} ({type(e).__name__})")
            continue
        if img.getexif().get_ifd(GPS_IFD):
            avec_gps += 1
        img = ImageOps.exif_transpose(img)  # garder le bon sens avant de jeter l'EXIF
        if img.width > o.largeur:
            img = img.resize((o.largeur, round(img.height * o.largeur / img.width)), Image.LANCZOS)
        base = nom_propre(p)
        while base in noms:
            base += "-2"
        noms.add(base)
        # Image neuve : seuls les pixels sont copiés, aucune métadonnée ne suit.
        if img.mode == "P":  # une palette ne se recopie pas par paste
            img = img.convert("RGBA")
        propre = Image.new(img.mode, img.size)
        propre.paste(img)
        if propre.mode in ("RGBA", "LA", "P"):
            propre.save(o.sortie / f"{base}.webp", "WEBP", quality=o.qualite)
            propre.convert("RGBA").save(o.sortie / f"{base}.png", optimize=True)
            sortie_jpg = o.sortie / f"{base}.png"
        else:
            propre = propre.convert("RGB")
            propre.save(o.sortie / f"{base}.webp", "WEBP", quality=o.qualite)
            propre.save(o.sortie / f"{base}.jpg", "JPEG", quality=o.qualite + 5, optimize=True, progressive=True)
            sortie_jpg = o.sortie / f"{base}.jpg"
        total_avant += p.stat().st_size
        total_apres += (o.sortie / f"{base}.webp").stat().st_size
        print(f"{p.name} → {base}.webp + {sortie_jpg.suffix[1:]} ({propre.width}×{propre.height})")

    # Contrôle : aucune sortie ne doit garder d'EXIF.
    restes = [f.name for f in o.sortie.iterdir() if f.suffix in (".jpg", ".webp") and Image.open(f).getexif()]
    print(f"\n{len(fichiers)} photos, {avec_gps} avaient des coordonnées GPS.")
    print(f"Poids WebP : {total_avant // 1024} Ko → {total_apres // 1024} Ko")
    print("Métadonnées restantes : " + (", ".join(restes) if restes else "aucune"))


if __name__ == "__main__":
    main()
