---
name: supabase-projet
description: Brancher Supabase sur un site Next.js / Vercel de Rafaël — tables et migrations SQL à coller, RLS, connexion (mot de passe admin, OAuth Google), URL de redirection, modèles d'emails d'authentification, variables d'environnement. À utiliser pour « supabase », « les liens de connexion marchent pas », « Unable to exchange external code », « relation does not exist », « fais-moi les templates de connexion ».
---

# Supabase dans un projet

Rafaël colle lui-même le SQL dans l'éditeur Supabase et les variables dans
Vercel : lui donner des blocs prêts à coller, dans l'ordre.

## Étapes

1. **Schéma** : une migration par changement dans `supabase/migrations/
   <AAAAMMJJHHMM>_<nom>.sql`, rejouable (`create table if not exists`,
   `create policy` précédé de `drop policy if exists`). Un seul bloc à coller,
   tables avant les données (`relation "x" does not exist` = ordre inversé
   ou migration oubliée). Sur le Supabase partagé du VPS : un schéma par
   projet, jamais `public` (mémoire `supabase-vps-schema-partage.md`).
2. **RLS** sur chaque table, dans la même migration : `alter table … enable
   row level security` + politiques minimales (lecture publique seulement si
   la donnée est publique ; écriture admin via la clé `service_role` côté
   serveur uniquement). Vérifier ensuite avec `curl` et la clé `anon` qu'une
   table privée renvoie `[]` ou 401.
3. **Connexion** :
   - admin : mot de passe classique (`ADMIN_PASSWORD` dans Vercel), pas de
     lien magique — choix répété de Rafaël ;
   - clients : lien magique ou Google OAuth si demandé ;
   - Authentication → URL Configuration : *Site URL* = domaine de production,
     *Redirect URLs* = `https://<domaine>/auth/callback`,
     `https://*-<équipe>.vercel.app/auth/callback` et
     `http://localhost:3000/auth/callback`. « Unable to exchange external
     code » = URL de redirection absente ou secret OAuth faux côté Google.
4. **Emails d'auth** (Confirm sign up, Magic link, Reset password, Invite,
   Change email) : HTML autonome, styles en ligne, couleurs du site, bouton
   `{{ .ConfirmationURL }}`, texte français court ; un bloc par modèle.
   Envoi par le SMTP de Resend pour sortir de la limite de Supabase.
5. **Variables** : `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   (publiques) ; `SUPABASE_SERVICE_ROLE_KEY` serveur seulement (skill
   `poser-secret`). Fichier `.env.example` sans valeurs dans le dépôt.
6. **Tester** en vrai : inscription ou connexion de bout en bout sur la
   production, lecture/écriture depuis l'admin, refus avec la clé `anon`.

Fini quand l'étape 6 passe sur le domaine de production.
