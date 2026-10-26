---
name: menage-disque
description: Libérer de la place sur le disque C: du PC — mesurer ce qui prend de la place, vider les caches régénérables, node_modules des vieux projets, téléchargements, jeux et logiciels inutilisés, avec accord avant toute suppression. À utiliser pour « j'ai plus de place », « trie mon PC », « qu'est-ce qui prend de la place », « vire les dossiers qui servent à rien ».
---

# Ménage du disque

## Outil

```
python ~/.claude/skills/menage-disque/mesurer.py [--min-go 1]
```
Lecture seule, 2 à 5 minutes. Trois listes : caches régénérables (avec la
commande propre pour chacun), `node_modules` / `.next` / `.venv` des
projets, gros dossiers du profil et des programmes.

## Étapes

1. Mesurer avec l'outil.
2. **Sans risque, à faire directement** (se régénère tout seul) :
   `npm cache clean --force`, `pip cache purge`, `uv cache clean`,
   `pnpm store prune`, contenu de `%TEMP%`, versions de Playwright non
   utilisées (garder la plus récente). Annoncer les gigaoctets gagnés.
3. **Avec accord de Rafaël, liste à l'appui** :
   - `node_modules` / `.next` des projets non touchés depuis 1 mois
     (`npm install` les recrée) ;
   - Corbeille, Téléchargements (lister les plus gros fichiers d'abord) ;
   - jeux et logiciels (Steam, Ubisoft, CapCut, anciens KiCad ou SDK
     Microchip) : désinstaller par Paramètres → Applications, jamais en
     supprimant le dossier ;
   - données d'applications désinstallées (dossiers orphelins dans
     `AppData`) : vérifier que l'appli n'est plus installée.
4. **Ne jamais toucher** : `Documents`, `Pictures`, dépôts git avec du
   travail non poussé (skill `audit-projets`), `.ssh`, `.claude`, profils de
   navigateurs, `Claude-Data`, données de jeux sauvegardées.
5. Remesurer et donner le gain : avant → après.

Fini quand le gain est mesuré et que chaque suppression de l'étape 3 a été
validée par Rafaël.
