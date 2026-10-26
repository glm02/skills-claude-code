"""Envoie à Rafaël, sur Telegram, une vidéo, une image, un fichier, un lien ou un message.

Usage :
  python envoyer.py <chemin-ou-url> [<chemin-ou-url> ...] [-m "texte d'accompagnement"]
  python envoyer.py -m "Message seul"
  python envoyer.py --test          # vérifie le bot et la conversation sans rien envoyer
  python envoyer.py --essai ...     # montre ce qui serait envoyé, sans appeler Telegram

Le type est deviné : vidéo (sendVideo, lisible directement), image (sendPhoto),
lien http(s) (message avec aperçu), autre fichier (sendDocument).
Une vidéo de plus de 50 Mo (limite des bots) est recompressée avec ffmpeg ;
si elle dépasse encore, le script le dit au lieu d'échouer en silence.

Configuration : ~/.claude/secrets/telegram.env (posé par poser-bot.ps1) :
  TELEGRAM_BOT_TOKEN=...   TELEGRAM_CHAT_ID=...
Le jeton n'est jamais affiché : l'URL de l'API le contient, on n'en montre
que le code HTTP et la description d'erreur de Telegram.
"""
import argparse, html, json, mimetypes, os, shutil, subprocess, sys, tempfile, uuid
import urllib.error, urllib.request
from pathlib import Path

CONFIG = Path.home() / ".claude" / "secrets" / "telegram.env"
LIMITE = 50 * 1024 * 1024  # 50 Mo : plafond d'envoi de fichiers pour un bot
VIDEOS = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
IMAGES = {".png", ".jpg", ".jpeg", ".webp"}


def config():
    valeurs = {}
    if CONFIG.exists():
        for ligne in CONFIG.read_text(encoding="utf-8-sig").splitlines():
            if "=" in ligne and not ligne.lstrip().startswith("#"):
                k, v = ligne.split("=", 1)
                valeurs[k.strip()] = v.strip().strip('"')
    jeton = os.environ.get("TELEGRAM_BOT_TOKEN") or valeurs.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID") or valeurs.get("TELEGRAM_CHAT_ID")
    if not jeton or not chat:
        sys.exit(f"Bot non configuré : lancer poser-bot.ps1 (attendu : {CONFIG}).")
    return jeton, chat


def dimensions(video: Path) -> dict:
    """Largeur, hauteur (rotation comprise) et durée de la vidéo, lues par ffprobe."""
    if not shutil.which("ffprobe"):
        return {}
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", str(video)],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        d = json.loads(r.stdout)
        s = d["streams"][0]
        l, h = int(s["width"]), int(s["height"])
        if any(abs(int(x.get("rotation", 0))) == 90 for x in s.get("side_data_list", [])):
            l, h = h, l
        return {"width": l, "height": h, "duration": round(float(d["format"]["duration"]))}
    except (ValueError, KeyError, IndexError):
        return {}


def vignette(video: Path):
    """Image d'aperçu JPEG (≤ 320 px, < 200 Ko) prise à 1 s, comme l'exige Telegram."""
    if not shutil.which("ffmpeg"):
        return None
    sortie = Path(tempfile.gettempdir()) / f"{video.stem}-vignette.jpg"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", str(video), "-frames:v", "1",
                        "-vf", "scale='if(gt(iw,ih),320,-2)':'if(gt(iw,ih),-2,320)'", "-q:v", "4", str(sortie)])
    return sortie if r.returncode == 0 and sortie.exists() else None


def appel(jeton, methode, champs, fichier=None, miniature=None):
    url = f"https://api.telegram.org/bot{jeton}/{methode}"
    if fichier:
        cle, chemin = fichier
        borne = uuid.uuid4().hex
        corps = bytearray()
        for k, v in champs.items():
            corps += f"--{borne}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        pieces = [(cle, chemin)] + ([("thumbnail", miniature)] if miniature else [])
        for nom, p in pieces:
            type_mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            corps += (f"--{borne}\r\nContent-Disposition: form-data; name=\"{nom}\"; filename=\"{p.name}\"\r\n"
                      f"Content-Type: {type_mime}\r\n\r\n").encode()
            corps += p.read_bytes() + b"\r\n"
        corps += f"--{borne}--\r\n".encode()
        req = urllib.request.Request(url, data=bytes(corps), headers={"Content-Type": f"multipart/form-data; boundary={borne}"})
    else:
        req = urllib.request.Request(url, data=json.dumps(champs).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            desc = json.load(e).get("description", "")
        except ValueError:
            desc = ""
        sys.exit(f"Telegram a refusé {methode} : HTTP {e.code} {desc}")


def compresser(video: Path) -> Path:
    """Ramène une vidéo sous 50 Mo : 720 px de large au plus, débit calculé sur la durée."""
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        sys.exit(f"{video.name} fait {video.stat().st_size // 2**20} Mo (> 50) et ffmpeg est introuvable.")
    duree = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                                 capture_output=True, text=True).stdout.strip() or 60)
    kbps = max(300, int(45 * 8 * 1024 / duree) - 128)  # 45 Mo visés, 128 kb/s pour le son
    sortie = Path(tempfile.gettempdir()) / f"{video.stem}-telegram.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", "scale='min(720,iw)':-2",
                    "-c:v", "libx264", "-b:v", f"{kbps}k", "-maxrate", f"{kbps}k", "-bufsize", f"{2 * kbps}k",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(sortie)], check=True)
    if sortie.stat().st_size > LIMITE:
        sys.exit(f"{video.name} dépasse encore 50 Mo après compression : envoyer plutôt un lien.")
    return sortie


def envoyer(element, legende, jeton, chat, essai):
    legende_html = html.escape(legende)[:1000] if legende else ""
    if element.startswith(("http://", "https://")):
        texte = (f"{legende_html}\n" if legende_html else "") + html.escape(element)
        champs = {"chat_id": chat, "text": texte, "parse_mode": "HTML", "link_preview_options": {"url": element, "prefer_large_media": True}}
        print(f"lien → {element}")
        return essai or appel(jeton, "sendMessage", champs)

    chemin = Path(element).expanduser().resolve()
    if not chemin.is_file():
        sys.exit(f"Introuvable : {chemin}")
    ext = chemin.suffix.lower()
    if ext in VIDEOS:
        methode, cle = "sendVideo", "video"
        if chemin.stat().st_size > LIMITE and not essai:
            chemin = compresser(chemin)
    elif ext in IMAGES and chemin.stat().st_size < 10 * 2**20:
        methode, cle = "sendPhoto", "photo"
    else:
        methode, cle = "sendDocument", "document"
        if chemin.stat().st_size > LIMITE:
            sys.exit(f"{chemin.name} dépasse 50 Mo : envoyer un lien à la place.")
    champs = {"chat_id": chat, "parse_mode": "HTML"}
    if legende_html:
        champs["caption"] = legende_html
    miniature = None
    if methode == "sendVideo":
        champs["supports_streaming"] = "true"
        # Sans largeur/hauteur, Telegram affiche un cadre carré et écrase les vidéos verticales.
        champs.update(dimensions(chemin))
        miniature = vignette(chemin)
    print(f"{cle} → {chemin.name} ({chemin.stat().st_size / 2**20:.1f} Mo)")
    return essai or appel(jeton, methode, champs, (cle, chemin), miniature)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("elements", nargs="*")
    a.add_argument("-m", "--message", default="")
    a.add_argument("--test", action="store_true")
    a.add_argument("--essai", action="store_true")
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    jeton, chat = ("essai", "0") if o.essai else config()

    if o.test:
        moi = appel(jeton, "getMe", {})["result"]
        conv = appel(jeton, "getChat", {"chat_id": chat})["result"]
        print(f"Bot @{moi['username']} prêt ; conversation trouvée ({conv.get('type')}).")
        return
    if not o.elements:
        if not o.message:
            a.error("rien à envoyer")
        print("message")
        if not o.essai:
            appel(jeton, "sendMessage", {"chat_id": chat, "text": o.message})
        return
    for i, e in enumerate(o.elements):
        envoyer(e, o.message if i == 0 else "", jeton, chat, o.essai)
    print("Envoyé." if not o.essai else "Essai : rien n'a été envoyé.")


if __name__ == "__main__":
    main()
