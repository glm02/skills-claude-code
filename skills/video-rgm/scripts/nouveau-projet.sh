#!/usr/bin/env bash
# Crée un projet vidéo RGM prêt à remplir.
#   bash nouveau-projet.sh <dossier> "<logos séparés par des espaces>" [piste-brag]
# Exemple :
#   bash nouveau-projet.sh ~/Desktop/video-rgm-saas/agent-outils "gmail whatsapp googlecalendar slack"
# La piste par défaut est vol-10 (110 BPM) des musiques fournies par le skill brag.
set -euo pipefail

ICI="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:?dossier manquant}"
LOGOS="${2:-}"
PISTE="${3:-happy-beats-business-moves-vol-10-by-ende-dot-app}"
BRAG="$HOME/.claude/skills/brag/assets"
EXTRAIT="$HOME/.claude/skills/media-use/audio/scripts/extract-audio-data.py"

if [ -e "$DEST/index.html" ]; then echo "$DEST/index.html existe déjà, rien n'est écrasé."; exit 1; fi
mkdir -p "$DEST/assets/logos" "$DEST/assets/music" "$DEST/assets/sfx" "$DEST/assets/voix"
cp -r "$ICI/modele/." "$DEST/"
NOM="$(basename "$DEST")"
printf '{\n  "name": "%s",\n  "private": true,\n  "type": "module"\n}\n' "$NOM" > "$DEST/package.json"
printf '{\n  "id": "%s",\n  "name": "%s"\n}\n' "$NOM" "$NOM" > "$DEST/meta.json"

for slug in $LOGOS; do
  if [ -f "$ICI/logos/$slug.svg" ]; then cp "$ICI/logos/$slug.svg" "$DEST/assets/logos/"; else echo "Logo inconnu : $slug (voir $ICI/logos/logos.json)"; fi
done
# Les tracés intégrés à la page : un <img> SVG peut sortir vide au rendu.
node "$ICI/scripts/logos-js.mjs" "$DEST"

if [ -f "$BRAG/music/$PISTE.mp3" ]; then
  cp "$BRAG/music/$PISTE.mp3" "$DEST/assets/music/musique.mp3"
  [ -f "$BRAG/music/cues/$PISTE.music-cues.md" ] && cp "$BRAG/music/cues/$PISTE.music-cues.md" "$DEST/assets/music/reperes.md"
  if [ -f "$EXTRAIT" ]; then
    python "$EXTRAIT" "$DEST/assets/music/musique.mp3" --fps 30 --bands 4 -o "$DEST/assets/music/audio-data.json" >/dev/null
    node -e '
      const fs = require("fs"); const d = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
      const f = d.frames.slice(0, 2700);
      const r = f.map((x) => +x.rms.toFixed(3)), b = f.map((x) => +x.bands[0].toFixed(3));
      fs.writeFileSync(process.argv[2], "// Énergie de la musique, 30 valeurs par seconde.\nwindow.AUDIO_RMS=" + JSON.stringify(r) + ";\nwindow.AUDIO_BASSE=" + JSON.stringify(b) + ";\n");
    ' "$DEST/assets/music/audio-data.json" "$DEST/assets/audio-rms.js"
  fi
else
  echo "Musique brag introuvable : le projet sera muet tant qu'aucune piste n'est posée."
  echo "window.AUDIO_RMS=[];window.AUDIO_BASSE=[];" > "$DEST/assets/audio-rms.js"
fi

echo "Projet prêt : $DEST"
