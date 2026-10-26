---
name: audit-securite-site
description: Test de sécurité (pentest léger) d'un site ou d'une application web de Rafaël — admin, API, Supabase, Vercel, en-têtes, secrets — avec preuve et correction. À utiliser pour « fais un pentest », « review sécurité », « corrige les failles », « rends-le imprenable », ou avant de livrer un site avec espace admin ou compte client.
---

# Audit de sécurité d'un site

Seulement sur les sites de Rafaël ou de ses clients. Tests non destructifs :
pas de déni de service, pas de modification de vraies données de production.

## Étapes

1. **Cartographier** : pages publiques, routes API (`api/`, `app/api/`,
   server actions), espace admin, compte client, webhooks, tâches planifiées.
   Pour chaque route : qui a le droit de l'appeler ?
2. **Contrôler, point par point** (noter OK / faille / non applicable) :
   - **Admin** : mot de passe dans une variable d'environnement, comparaison
     en temps constant, limite d'essais par IP (429), cookie `HttpOnly;
     Secure; SameSite`, chaque route admin vérifie la session côté serveur ;
   - **API** : appeler chaque route sans authentification et avec un mauvais
     jeton (`curl -i`) → doit répondre 401/403, jamais de données ;
   - **Supabase** : RLS active sur **toutes** les tables (`select relname,
     relrowsecurity from pg_class …`), politiques qui ne laissent pas `anon`
     lire les données d'autrui, aucune clé `service_role` côté navigateur ;
   - **Entrées** : validation côté serveur, échappement HTML des contenus
     affichés (XSS), requêtes paramétrées, taille max des envois et fichiers ;
   - **Webhooks** (Resend, Stripe…) : signature vérifiée ;
   - **En-têtes** : CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`,
     `frame-ancestors` ; `curl -sI https://<site>` ;
   - **Fuites** : `/.env`, `/.git/`, `/docs/`, source maps, messages d'erreur
     détaillés, secrets dans le dépôt (skill `audit-projets`) ;
   - **Dépendances** : `npm audit --omit=dev` (critiques et hautes).
3. **Prouver** chaque faille par la requête qui la montre (sans afficher de
   donnée personnelle ni de secret dans le rapport : codes HTTP et tailles).
4. **Corriger** par gravité, ajouter un test automatique quand le projet en
   a (une route refuse sans auth), redéployer, rejouer la preuve → elle doit
   échouer.
5. Rapport dans `docs/securite/checkup-<date>.md` du projet : trouvé,
   corrigé, reste à faire.

Fini quand chaque ligne de l'étape 2 a un verdict et que chaque faille
corrigée a sa preuve rejouée en ligne.

## Préférences

Admin = mot de passe classique posé par Rafaël dans les variables Vercel,
pas de lien magique par email. Le dépôt `0xSteph/pentest-ai-agents` peut
servir de complément, ses agents restent bornés au site testé.
