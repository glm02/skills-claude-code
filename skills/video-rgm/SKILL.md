---
name: video-rgm
description: Faire une vidéo verticale TikTok/Reels pour RGM Dev (agents IA, automatisation, sites web) avec HyperFrames, une bibliothèque de composants React prêts à animer (téléphone, conversation, notifications, flux façon n8n, orbite de logos, éditeur de code, terminal, carte d'offre, compteur, tâches cochées, sous-titres), de vrais logos de marques (Gmail, WhatsApp, Google Agenda, Slack, n8n…), la musique de brag et une voix off ElevenLabs. À utiliser pour « fais-moi une vidéo TikTok », « une vidéo sur mes agents IA », « une vidéo avec les vrais logos », « ajoute une voix off », ou toute vidéo promo de RGM Dev.
---

# Vidéo RGM (HyperFrames + React + vrais logos + ElevenLabs)

Lire aussi le skill `hyperframes` (contrat de rendu), et pour l'audio le skill
`brag` (`references/audio.md` : musiques, sons, repères de tempo). Ce skill
remplace leur étape « storylines » : le plan s'écrit ici.

## 1. Créer le projet

```bash
bash ~/.claude/skills/video-rgm/scripts/nouveau-projet.sh <dossier> "gmail whatsapp googlecalendar slack"
```

Par défaut sous `~/Desktop/video-rgm-saas/<nom>/`. Le script copie le modèle
(`index.html`, `assets/composants.js|css`, police Geist, logo RGM), les logos
demandés, la musique brag vol-10 (110 BPM) et ses repères
(`assets/music/reperes.md`), et l'énergie de la musique pour l'audio-réactif
(`assets/audio-rms.js`). Logos disponibles : `logos/logos.json` (38 marques,
couleurs officielles). Il n'y a pas de logo Microsoft, LinkedIn, Qonto,
Pennylane ou Doctolib dans Simple Icons : ne pas en dessiner un faux, écrire le
nom à la place.

## 2. Écrire le plan (dans `PLAN.md` du projet)

- Accroche déjà lisible à l'image 0 (c'est la vignette TikTok), puis
  révélation, 2 ou 3 moments forts, appel à l'action. 18 à 25 s.
- Montrer le produit en marche (conversation, flux, notifications), pas un
  diaporama. Chaque scène dit une seule chose.
- Prix, délais, inclus : recopier `src/lib/contenu-defaut.ts` du dépôt
  `rgm dev master`, jamais inventer. Les textes d'interface (« Rendez-vous
  ajouté ») sont illustratifs : aucun vrai nom de client.
- Les coupes et les arrivées en série tombent sur la grille de la musique
  (`reperes.md`) ; un texte à lire tient environ 0,3 s par mot.
- Voix off : script court (≈ 2,5 mots par seconde), qui complète l'image au
  lieu de la lire.

## 3. Composer avec les composants

Dans `index.html`, chaque scène est un clip HTML avec un hôte vide ; on y monte
un composant puis on l'anime avec `RGM.anim.*` dans la timeline.

| Composant | Montre | Animation |
|---|---|---|
| `Titre` (`*mot*` = bleu, `\n` = ligne) | gros titre | `anim.mots` |
| `Logo`, `LogoRGM` | vrai logo en tuile | GSAP direct |
| `OrbiteLogos` | outils autour de l'agent | `anim.orbite` |
| `BandeLogos` | défilé de logos | `anim.defilement` |
| `FluxAgent` | entrées → agent → sorties, paquets qui circulent | `anim.flux` |
| `Telephone` (+ `app: "whatsapp"`) | conversation client/agent | `anim.conversation` |
| `Notification` (`slug` = logo de l'app) | ce que l'agent a fait | `anim.pile` |
| `Editeur`, `Terminal` | création de l'agent | `anim.frappe`, `anim.lignes` |
| `Faisceau` | cadre au liseré lumineux du site | `anim.faisceau` |
| `CarteOffre` | offre et prix réels | `anim.compteur` sur `.rgm-prix-min` |
| `Compteur`, `ListeTaches` | chiffres, tâches cochées | `anim.compteur`, `anim.cocher` |
| `SousTitres` + `RGM.grouperMots` | sous-titres de la voix | `anim.sousTitres` |
| `Bouton`, `Toast` | appel à l'action, badge | `anim.appui`, `anim.ping` (sur `.rgm-ping` seulement : il efface ce qu'il anime) |
| fond | halo qui respire avec la musique | `anim.audioReactif` |

Règles :
- Monter tous les composants (`RGM.monter`) **avant** `document.fonts.ready`,
  construire la timeline dedans et l'enregistrer à la fin.
- Le texte reste entre 168 et 1330 px de haut (interface TikTok autour).
- Un nouveau composant va dans `assets/composants.js` du skill (pas seulement
  dans le projet) s'il resservira.

## 4. Voix off ElevenLabs

Clé posée une fois par Rafaël, jamais dans la conversation :
`powershell -ExecutionPolicy Bypass -File ~/.claude/skills/poser-secret/scripts/poser-elevenlabs.ps1`
(saisie masquée, test HTTP, fichier `~/.secrets/elevenlabs.env` lisible par lui seul).

```bash
S=~/.claude/skills/video-rgm/scripts/voix-elevenlabs.mjs
node $S --test                                  # code HTTP seulement
node $S --liste                                 # choisir une voix française
node $S --texte PLAN-voix.txt --sortie assets/voix --voix <ID>   # voix.mp3 + mots.json
node $S --effet "whoosh doux" --duree 1 --sortie assets/sfx/whoosh.mp3
```

La voix choisie est gardée dans `config.json`. Brancher la voix en
`<audio id="voix" data-volume="1">`, baisser la musique à 0,14–0,18, caler les
scènes sur `mots.json` et afficher les sous-titres (`SousTitres`).
Une prise par scène (`--sortie assets/voix/s1`, `s2`…) se cale mieux sur l'image
qu'un seul long fichier ; regrouper ensuite les mots décalés dans
`assets/voix/mots.js` (`window.VOIX_MOTS`), chargé en `<script>` (pas de fetch).
Les sous-titres (top 1150 px) seulement là où cette bande est libre, et pas
quand le titre à l'écran dit déjà la phrase. Vérifier sur une capture.
Si ElevenLabs ne répond pas, le dire et livrer sans voix plutôt qu'avec une
autre voix.

## 5. Vérifier, rendre, livrer

1. `npx hyperframes check --json` : zéro erreur, contrastes contrôlés.
2. `npx hyperframes snapshot --at ...` sur chaque scène et une transition :
   regarder les images, corriger débordements et chevauchements.
3. `npx hyperframes render --quality delivery --output renders/<nom>.mp4`.
4. Volume social (toujours depuis le rendu brut, jamais deux fois de suite) :
   `ffmpeg -i brut.mp4 -c:v copy -af "loudnorm=I=-14.5:TP=-2:LRA=11,alimiter=limit=0.84:level=false" -ar 48000 -c:a aac -b:a 192k out.mp4`,
   puis `npx hyperframes audio out.mp4 --json` : viser −15 à −14 LUFS, crête sous −1 dB, `clipping.count` à 0
   (le loudnorm seul, en une passe, a déjà fait saturer à +1 dB).
5. Extraire 4 ou 5 images du MP4 final (`ffmpeg -ss <t> -frames:v 1`) et les
   regarder : les captures peuvent être bonnes et le MP4 non (logos en `<img>`
   sortis vides une fois). Les logos passent par `assets/logos.js` (tracés
   intégrés, généré par `scripts/logos-js.mjs`) : le relancer après avoir
   ajouté un SVG dans `assets/logos/`.
6. Dire à Rafaël : chemin du MP4, ce qui a été vu et mesuré (le son n'est pas
   écouté), crédit musique « Sascha Ende (ende.app), CC BY 4.0 » à mettre en
   description.

## Logos : rappel

Les logos viennent de Simple Icons (CC0 pour les tracés, `logos/LICENSE-simple-icons.md`)
mais restent des marques déposées (`logos/DISCLAIMER-simple-icons.md`) : les
montrer pour dire « je me branche sur cet outil », jamais pour laisser croire à
un partenariat ou à une recommandation de la marque.
