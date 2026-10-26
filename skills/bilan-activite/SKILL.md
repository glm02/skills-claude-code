---
name: bilan-activite
description: Temps passé par projet et résumé de ce qui a été fait sur une période — à partir des sessions Claude Code et des commits — pour facturer, chiffrer un devis, calculer un taux horaire, remplir un rapport ou faire le point de la semaine. À utiliser pour « combien de temps j'ai passé sur X », « qu'est-ce que j'ai fait cette semaine / ce mois », « récap de mon activité ».
---

# Bilan d'activité

## Outil

```
python ~/.claude/skills/bilan-activite/bilan.py --depuis 2026-10-01 [--jusqu 2026-10-31] [--projet <nom>] [--pause 45]
```
Heures par projet (plages de travail : messages espacés de moins de 45 min,
15 min minimum par plage), jours actifs, première et dernière date. Les
worktrees Orca sont rangés sous leur projet.

## Étapes

1. Lancer l'outil sur la période demandée.
2. **Ce qui a été fait**, projet par projet :
   `git -C <dépôt> log --since=<date> --until=<date> --no-merges
   --format='%ad %s' --date=short`, regroupé en 3 à 8 réalisations
   compréhensibles par un non-technicien (« espace admin : campagnes SMS
   ciblées par commune »), pas une liste de commits.
3. Selon le but :
   - *facture / taux horaire* : prix convenu ÷ heures = taux ; donner une
     fourchette (le temps de réflexion hors session n'est pas compté) ;
   - *point de la semaine* : fait / en cours / bloqué et par qui ;
   - *rapport (stage, école)* : réalisations et compétences mobilisées.

Fini quand chaque projet de la période a ses heures et ses réalisations.

## Limites à dire

Ce sont des heures de présence en session, pas une feuille de temps : le
travail sans Claude (Figma, appels, déplacements) n'y est pas.
