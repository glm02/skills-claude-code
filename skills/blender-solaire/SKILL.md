---
name: blender-solaire
description: Modéliser une maison dans Blender et y poser des panneaux solaires à l'échelle — plan, murs, toit en pente, pose automatique des panneaux sur un pan, comptage et puissance, rendu. À utiliser pour « modélise la maison sur Blender », « mets les panneaux sur le toit », « combien de panneaux tiennent », « raccourcis Blender », ou un fichier .blend de maison.
---

# Maison et panneaux solaires dans Blender

Blender 5.2 : `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
Travailler en mètres (Propriétés de scène → Unités → Métrique, échelle 1).

## Outil : pose des panneaux

`~/.claude/skills/blender-solaire/poser_panneaux.py` remplit chaque face
sélectionnée d'un toit avec des panneaux à l'échelle (par défaut 1,134 ×
1,722 m, 425 Wc, marge de 30 cm, écart de 2 cm, grille centrée) dans la
collection « Panneaux PV », puis affiche le nombre de panneaux et les kWc.
Relancer le script remplace la pose précédente.
- Dans Blender : sélectionner le pan (mode Édition, touche 3, clic), Tab,
  Scripting → ouvrir le script → Run Script.
- Sans interface :
  `blender maison.blend --background --python poser_panneaux.py -- --objet Toit --paysage --sauver`
  Comparer portrait et paysage : le paysage gagne souvent un rang.

## Étapes pour une maison

1. **Mesures** : emprise au sol, hauteur à l'égout, pente du toit (ou
   hauteur du faîtage), orientation (azimut du pan sud), obstacles (cheminée,
   velux, arbres). Un plan dessiné par Rafaël fait foi sur toute
   supposition : le suivre exactement, et dire ce qui manque.
2. **Volume** : un cube à l'emprise (S pour dimensionner en tapant les
   valeurs), puis le toit : sélectionner l'arête du haut, monter le faîtage
   (G Z <hauteur>), ou extruder (E) un profil de pignon le long de la maison.
   Le toit doit être un objet séparé, ses pans des faces planes.
3. **Nord** : orienter la scène pour que +Y soit le nord ; le pan sud
   regarde alors −Y. Demander l'orientation réelle plutôt que la deviner.
4. **Obstacles** : modéliser cheminée et velux ; découper le pan (K, couteau)
   pour exclure leur zone avant la pose, ou supprimer les panneaux qui les
   recouvrent.
5. **Poser** les panneaux avec l'outil, choisir l'orientation, noter le
   nombre et les kWc, puis passer au skill `dimensionnement-pv` pour la
   production.
6. **Rendu** pour présenter : caméra (Numpad 0 ; Ctrl+Alt+Numpad 0 pour
   caler sur la vue), moteur Eevee, soleil réglé sur l'azimut et l'heure.

## Raccourcis utiles

Tab édition/objet · 1/2/3 sommets/arêtes/faces · G/R/S déplacer/tourner/
échelle, suivis de X/Y/Z et d'une valeur · E extruder · I insérer une face ·
Ctrl+R boucle d'arêtes · K couteau · F remplir · M fusionner · Shift+D
dupliquer · Ctrl+A appliquer l'échelle (à faire avant de mesurer) ·
N panneau de mesures · Numpad 1/3/7 face/côté/dessus · Numpad 5 perspective.

## Confidentialité

Le .blend d'une maison familiale reste sur le PC : pas d'adresse, de
coordonnées GPS ni de vue reconnaissable dans un dépôt git ou une page publique.
