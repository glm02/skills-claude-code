---
name: portfolio-projet
description: Ajouter ou mettre à jour un projet, un TP ou des photos sur le portfolio de Rafaël (www.rafaelgmille.site, dépôt Stagebot) — fiche projet, photos nettoyées, logos d'outils, mise en ligne vérifiée. À utiliser pour « ajoute ce projet au portfolio », « j'ai mis les nouvelles photos », « mets mon TP sur le site », « ajoute des outils à ma boîte à outils ».
---

# Projet sur le portfolio

Dépôt : `~/Documents/GitHub/stagebot/Stagebot` (Next.js, Vercel, push sur
`main` = mise en ligne). Ses règles sont dans `AGENTS.md` du dépôt : les
relire, elles priment.

## Étapes

1. **Matière** : photos (dossier `images/` du dépôt, ignoré par git), notes
   ou compte rendu de Rafaël, dépôt GitHub du projet s'il est public.
   Ce qu'il a fait lui-même doit être clair : le demander en cas de doute.
2. **Photos** : skill `photos-web` vers `public/projets/<slug>/01.jpg, 02.jpg…`
   (largeur 1600, GPS retiré, visages et adresses floutés ou recadrés).
   Regarder chaque photo avant de la publier.
3. **Fiche** dans `src/lib/site.ts` (`PROJETS` pour l'électrique, `PROJETS_DEV`
   pour le développement) en suivant le type `Projet` : `ref`, `slug`,
   `titre`, `resume` (une phrase : le problème résolu), `tags`, `statut`,
   `schema`, `contexte`, `objectif`, `contribution` (ses actions à lui,
   verbes concrets), `outils`, `photos` avec légendes, `depot`.
   Les légendes reprennent ses mots ; rien qui dépasse le CV.
4. **Outils et logos** : un nouveau logiciel ou composant dans les listes
   d'outils, avec son vrai logo (voir `docs/logos.md` du dépôt).
5. **Vérifier** : `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`
   verts, puis skill `audit-mobile` sur `/projets` et `/projets/<slug>`.
6. Commit en français, push sur `main`, puis contrôler la fiche en ligne.

Fini quand la fiche s'affiche en ligne avec ses photos, à 390 et 1440 px.

## Règles du portfolio

Uniquement des bleus (logos en couleurs d'origine dans des tuiles) ; rien de
trop personnel (âge, adresse, téléphone, mail, maison familiale) ; anglais
B2, espagnol niveau collège.
