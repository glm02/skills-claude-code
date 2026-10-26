---
name: audit-mobile
description: Contrôle visuel d'un site sur téléphone et ordinateur — captures automatiques, débordements, textes qui se chevauchent, boutons trop petits, images cassées — puis corrections et preuve après coup. À utiliser pour « sur téléphone c'est tout pourri », « c'est pas responsive », « le texte se superpose », « fais un check-up de l'UI », et avant d'annoncer qu'une interface est finie.
---

# Audit téléphone + ordinateur

## Outil

```
node ~/.claude/skills/audit-mobile/captures.mjs <dossier-sortie> <url> [url ...]
```
Captures pleine page à 390 px et 1440 px, plus `rapport.json` : débordement
horizontal, éléments trop larges, chevauchements de texte, cibles tactiles
< 40 px, images cassées, erreurs JavaScript. Marche sur l'URL en ligne ou
sur le serveur local (`npm run dev`). Utilise Chrome installé (rien à
télécharger). Mettre les captures dans le dossier scratchpad, jamais dans le dépôt.

## Étapes

1. Lister les pages qui comptent : accueil, chaque page service ou produit,
   contact, compte client, admin (connecté si possible).
2. Lancer l'outil sur toutes ces pages.
3. **Regarder chaque capture téléphone** (Read sur le PNG, en découpant avec
   `magick <png> -crop 390x900+0+<y>` pour les pages longues). Le rapport
   automatique ne voit pas tout : contraste faible, texte blanc sur fond
   blanc, élément 3D décentré, bandeau qui gêne, trop de texte.
   Confirmer chaque défaut du rapport sur l'image : un défaut non visible est
   un faux positif.
4. Liste des défauts : page, largeur, ce qui ne va pas, cause probable
   (fichier CSS / composant), gravité (bloque l'usage / gêne / cosmétique).
5. Corriger par ordre de gravité, dans le composant ou la feuille de style
   d'origine (pas de rustine locale qui casse ailleurs).
6. Relancer l'outil sur les mêmes pages et comparer.

Fini quand chaque page de la liste a été vue à 390 et 1440 px après
correction, sans défaut « bloque l'usage » ni « gêne » restant.

## Goûts de Rafaël (retours passés)

Épuré, peu de texte, composants (shadcn/ui, ObsidianUI) plutôt que du fait
main ; fond 3D très léger et lent (il donne la migraine sinon) ; pas de
bandeau collant « Appeler / Devis » sur téléphone ; pas de doubles cartes
imbriquées ; textes posés sur un fond, jamais directement sur des points 3D.
