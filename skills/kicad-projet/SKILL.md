---
name: kicad-projet
description: Travailler sur un projet KiCad (10) — contrôles ERC/DRC, dossier de fabrication (Gerber, perçages, nomenclature, position, PDF) pour JLCPCB ou PCBWay, travail à deux sur GitHub sans s'écraser, revue de schéma. À utiliser pour « vérifie ma carte », « exporte les Gerber », « commande du PCB », « travailler à deux sur KiCad », ou un fichier .kicad_pro.
---

# Projet KiCad

kicad-cli 10 : `%LOCALAPPDATA%\Programs\KiCad\10.0\bin\kicad-cli.exe`.
Projets d'école : `~/Documents/Ecole/` (vide-cave : dépôt git `glm02/projet-vide-cave`).

## Outil : contrôles et fabrication

```
python ~/.claude/skills/kicad-projet/fabrication.py <dossier-du-projet> [--sortie <dossier>] [--sans-controle]
```
ERC, DRC avec parité schéma/PCB (nombre d'erreurs par type), Gerber des
couches de fabrication + perçages en zip, nomenclature CSV (lisible par
Excel), positions CPL, schéma PDF. Ne modifie pas les fichiers du projet ;
sortie par défaut : `<projet>/fabrication/<date>/`.

## Revue d'une carte

1. Lancer l'outil. Toute **erreur** ERC/DRC est à corriger ou à justifier
   une par une. Avertissements fréquents :
   - `lib_footprint_mismatch` : l'empreinte de la carte diffère de la
     bibliothèque (souvent sans gravité ; « Mettre à jour les empreintes
     depuis la bibliothèque » si voulu) ;
   - `unconnected_items` : piste manquante, toujours à traiter.
2. Lire le schéma PDF : alimentations et découplage (100 nF près de chaque
   circuit intégré), isolement secteur (optotriac, distances), protections
   (fusible, varistance), connecteurs repérés, valeurs et tensions des
   condensateurs.
3. PCB : largeur des pistes selon le courant (IPC-2221 ; ≈ 1 mm par ampère
   en cuivre 35 µm comme ordre de grandeur), isolement 230 V (≥ 3 mm, fente
   si besoin), plan de masse, trous de fixation, sérigraphie lisible.
4. Rendre la liste : problème, endroit (repère ou coordonnées), correction.

Fini quand l'ERC et le DRC n'ont plus d'erreur et que chaque point des
étapes 2 et 3 est vérifié ou signalé.

## Travailler à deux sur GitHub

- `.gitignore` : `*-backups/`, `fp-info-cache`, `*.lck`, `~*.lck`,
  `_autosave-*`, `*.kicad_prl`, `fabrication/`.
- Avant d'ouvrir KiCad : `git pull`. Après : enregistrer, fermer KiCad,
  `git add -A && git commit -m "<quoi>" && git push`.
- Un seul à la fois sur un même fichier (`.kicad_sch` ou `.kicad_pcb`) :
  les fusions de fichiers KiCad se passent mal. Se répartir par feuille de
  schéma hiérarchique, ou se prévenir.
- Le collègue sans git en ligne de commande : GitHub Desktop suffit (Fetch,
  Pull, Commit, Push).
- Conflit sur un fichier KiCad : ne pas fusionner à la main ; garder une
  version (`git checkout --theirs/--ours`) et refaire l'autre modification.
