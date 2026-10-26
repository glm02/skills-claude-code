---
name: rapport-tp
description: Rédiger un compte rendu de TP, un rapport de SAÉ ou de projet du BUT GEII — structure, schémas, tableaux de mesures, calculs avec unités et incertitudes, courbes, analyse, conclusion — en Word ou PDF. À utiliser pour « fais-moi le compte rendu du TP », « rapport de SAÉ », « mets en forme mes mesures », « trace la courbe », ou un devoir à rendre au prof.
---

# Compte rendu de TP / rapport GEII

Le travail est celui de Rafaël : partir de ses mesures, photos et notes ;
ne jamais inventer une mesure ni un résultat.

## Étapes

1. **Rassembler** : sujet du TP (PDF), mesures (photos de cahier, tableur,
   captures d'oscilloscope), schémas, consignes de rendu (format, longueur,
   date). Ce qui manque : le demander, ou laisser un repère `[À COMPLÉTER]`
   bien visible.
2. **Plan** :
   1. Objectifs (ce que le TP doit montrer, en 2-3 lignes) ;
   2. Matériel et montage (schéma, liste des appareils, calibres) ;
   3. Manipulations : pour chaque partie, protocole, tableau de mesures,
      calculs, courbe ;
   4. Analyse : écart théorie / mesure en %, causes plausibles (calibre,
      tolérance des composants, résistance interne, échauffement) ;
   5. Conclusion : réponse aux objectifs, ce qui a été appris.
3. **Calculs** : formule littérale, puis application numérique, puis
   résultat avec unité et nombre de chiffres significatifs cohérent avec la
   mesure. Incertitude quand le sujet la demande (précision de l'appareil
   en % lecture + digits).
4. **Courbes** : matplotlib, axes titrés avec unités, points de mesure +
   courbe théorique, PNG 300 dpi ; échelle log pour un diagramme de Bode.
5. **Document** : Word via le skill `anthropic-skills:docx` (titres
   numérotés, légendes « Figure n », tableaux centrés, en-tête avec nom,
   groupe et date), ou PDF. Relire : orthographe, unités, numérotation.

Fini quand chaque question du sujet a sa réponse dans le rapport, et chaque
résultat chiffré son unité et sa source (mesure ou calcul).

## Style

Français scientifique simple, phrases courtes, présent ou passé composé,
« nous » pour un travail en binôme. Pas de remplissage.
