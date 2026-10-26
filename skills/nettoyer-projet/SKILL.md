---
name: nettoyer-projet
description: Nettoyer un dépôt de code — fichiers et composants inutilisés, dépendances en trop, doublons, vieux tests et brouillons, branches mortes — sans rien casser, avec une branche de sauvegarde et le build vert. À utiliser pour « clean tout le projet », « vire les fichiers qui servent à rien », « trop de branches », « le projet est en bordel ».
---

# Nettoyer un projet

## Étapes

1. **Sauvegarde** : `git status` propre (sinon commit ou stash d'abord),
   puis `git branch sauvegarde-avant-menage-<date>`. Tout ce qui est retiré
   reste récupérable par cette branche.
2. **Repérer**, sans rien supprimer :
   - fichiers et exports inutilisés, dépendances en trop :
     `npx knip` (JS/TS) ; Python : `uvx vulture .` ;
   - fichiers jamais importés ni servis : captures, `*.bak`, `*-old.*`,
     `test*.html`, dossiers d'essais, zip, gros médias (`git ls-files | xargs
     du`… ou tri par taille) ;
   - branches : `git branch --merged main` (fusionnées) et branches
     distantes sans activité depuis 1 mois ;
   - doublons de composants (deux boutons, deux cartes qui font la même chose).
3. **Classer** : sûr à supprimer / à vérifier / à garder. Attention aux faux
   « inutilisés » : pages chargées par convention (Next.js `app/`), routes
   API appelées de l'extérieur (crons, webhooks), fichiers de `public/`
   référencés dans du contenu, scripts lancés à la main sur un serveur.
4. **Supprimer** le lot « sûr », puis lint, typecheck, tests, build. Un échec
   → remettre le fichier concerné. Montrer à Rafaël le lot « à vérifier ».
5. Branches : supprimer les branches locales fusionnées ; les distantes
   seulement avec son accord.
6. Commit « Ménage : … » avec la liste de ce qui a été retiré et pourquoi ;
   vérifier le site en ligne après déploiement.

Fini quand le build est vert, que le site en ligne fonctionne et que le
commit liste chaque élément retiré.
