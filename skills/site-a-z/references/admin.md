# Données, formulaires et espace admin

## Base Supabase

- Instance self-hosted du VPS (partagée entre projets) : **un schéma par
  projet** (ex. `liccia`), exposé dans les schémas de l'API ; jamais `public`.
  Projet cloud dédié : `public` convient.
- **RLS activée sur chaque table**. Le public lit seulement ce qui est publié ;
  il insère des demandes sans pouvoir les relire ; les rôles admin lisent et
  écrivent tout.
- Rôles dans une table `profiles` (`role in ('admin','agent')`) liée à
  `auth.users` ; politiques RLS écrites via une fonction `is_staff()`.
- Photos dans un bucket Storage dédié, lecture publique, écriture réservée au personnel.
- Migrations SQL versionnées dans `supabase/migrations/`, appliquées puis
  vérifiées (`list_tables`, conseils de sécurité de Supabase).
- La clé `service_role` reste côté serveur (Server Actions, route handlers),
  jamais dans un fichier importé par un composant client.

## Formulaires publics

- Un schéma zod par formulaire dans `src/lib/schemas/`, utilisé par
  react-hook-form côté client et par la Server Action côté serveur.
- Anti-spam : champ piège caché, jeton Turnstile vérifié côté serveur, limite
  de débit par IP, temps minimal de remplissage.
- Après enregistrement : notification (email via Resend, ou canal choisi par le
  client), message de confirmation à l'écran, toast `sonner`.
- Messages d'erreur en français, sous le champ concerné, `aria-describedby`.

## Espace admin

- Route `/admin` protégée par le middleware Next (session Supabase) **et** par
  la RLS ; `noindex` et exclue du sitemap.
- Conçu d'abord pour le téléphone : listes en cartes empilées sous 768 px,
  tableau au-delà ; actions principales accessibles au pouce.
- **Demandes** : boîte de réception (type, statut, date), fiche avec
  coordonnées, contenu, notes internes, historique des changements de statut,
  boutons appeler / écrire.
- **Contenus** (annonces, réalisations…) : brouillon / publié, formulaire
  validé par zod, aperçu avant publication, slug généré depuis le titre.
- **Photos** : glisser-déposer, compression WebP dans le navigateur avant envoi
  (≤ 2000 px), réordonnancement, `alt` obligatoire, première = couverture.
- **Avis** : saisie ou import avec source et lien, modération avant affichage.
- Chaque écran de liste a son `Skeleton` et son état vide (`empty`).
- Migration des contenus de l'ancien site par script depuis `scrape/content/`.
