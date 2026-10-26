---
name: demarrer-projet
description: Démarrer un nouveau projet de code proprement en quelques minutes — dossier, git, dépôt GitHub privé, .gitignore et .env.example, AGENTS.md / CLAUDE.md en français, stack habituelle de Rafaël (Next.js, shadcn/ui, Supabase, Vercel), premier déploiement. À utiliser pour « nouveau projet », « crée-moi le repo », « on commence un site / une app », « mets en ordre le projet ».
---

# Démarrer un projet

Pour un site vitrine client complet, le skill `site-a-z` prend le relais
après l'étape 4.

## Étapes

1. **Cadrer** en 3 lignes : à quoi sert le projet, pour qui, ce qui doit
   marcher à la fin de la première session. Choisir la stack :
   - site ou app web : Next.js (App Router, TypeScript), Tailwind, shadcn/ui
     (+ ObsidianUI, cult-ui selon le style), Vercel ;
   - données / comptes : Supabase (skill `supabase-projet`) ;
   - script ou outil : Python avec `uv`, ou Node.
2. **Créer** dans `~/Documents/GitHub/<nom-en-minuscules-sans-espaces>` :
   `npx create-next-app@latest <nom> --ts --tailwind --eslint --app --src-dir
   --use-pnpm` (ou `uv init`), puis `npx shadcn@latest init`.
3. **Fichiers de base** :
   - `.gitignore` : `.env*` sauf `.env.example`, `node_modules`, `.next`,
     `.vercel`, `*.local.*`, dossiers de données perso et de photos brutes ;
   - `.env.example` : les noms des variables, sans valeurs ;
   - `AGENTS.md` (et `CLAUDE.md` qui le référence) : réponse en français,
     but du projet, boucle `git status → modifier → lint/typecheck/test/build
     → captures 390/1440 → commit en français → push`, règles (secrets,
     données personnelles), section « État » datée ;
   - `README.md` court : lancer en local, déployer.
4. **Dépôt** : `git init`, premier commit, `gh repo create glm02/<nom>
   --private --source . --push`. Public seulement si Rafaël le demande, et
   après le skill `audit-projets` sur le dépôt.
5. **Déployer** : `vercel link` puis `vercel --prod` (skill `vercel-prod`),
   ouvrir l'URL.

Fini quand le dépôt privé existe sur GitHub, que `pnpm build` passe et que
l'URL de production répond.
