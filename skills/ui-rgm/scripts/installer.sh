#!/usr/bin/env bash
# Pose l'interface RGM dans un projet Next.js + Tailwind v4 existant.
#   bash installer.sh <dossier-du-projet>
# Copie les composants de référence dans src/components/rgm/ et les effets dans
# src/app/rgm-effets.css, puis installe les dépendances. N'écrase rien : un
# fichier déjà présent est laissé tel quel et signalé.
set -euo pipefail

ICI="$(cd "$(dirname "$0")/.." && pwd)"
PROJET="${1:?dossier du projet manquant}"
[ -f "$PROJET/package.json" ] || { echo "Pas de package.json dans $PROJET"; exit 1; }

mkdir -p "$PROJET/src/components/rgm" "$PROJET/src/app"
for f in "$ICI"/references/composants/*.tsx; do
  cible="$PROJET/src/components/rgm/$(basename "$f")"
  if [ -e "$cible" ]; then echo "déjà présent, laissé : $cible"; else cp "$f" "$cible"; fi
done
if [ -e "$PROJET/src/app/rgm-effets.css" ]; then echo "déjà présent, laissé : src/app/rgm-effets.css"
else cp "$ICI/references/effets.css" "$PROJET/src/app/rgm-effets.css"; fi

cd "$PROJET"
npm install @appica/ui-react @base-ui/react motion three simple-icons lucide-react \
  tw-animate-css clsx tailwind-merge class-variance-authority next-themes sonner

cat <<'FIN'

Reste à faire à la main (voir SKILL.md, étape 2) :
  1. Dans globals.css : reprendre les jetons :root / .dark et les lignes @source
     d'Appica depuis references/globals.css, puis  @import "./rgm-effets.css";
  2. Police Geist via next/font (variable --font-sans).
  3. Corriger les imports des composants copiés (@/components/... → @/components/rgm/...)
     et remplacer @/lib/site par les données du nouveau projet.
FIN
