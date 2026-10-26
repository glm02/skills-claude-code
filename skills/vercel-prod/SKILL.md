---
name: vercel-prod
description: Mettre un site en production sur Vercel et prouver qu'il est en ligne ; dépanner un déploiement en erreur, une variable d'environnement, un « ça part en preview au lieu de prod » ; vider le stockage de déploiements saturé. À utiliser pour « pousse », « déploie », « mets en ligne », « c'est en ligne ? », « trop de déploiements ».
---

# Production Vercel

Compte CLI : `vercel whoami` (connecté). Lancer cette commande d'abord : elle
rafraîchit aussi le jeton utilisé par le script de nettoyage.

## Mettre en production

1. Avant : `git status` propre, build local OK (`npm run build`), tests verts
   s'il y en a.
2. Vérifier la **branche de production** du projet (Vercel → Settings → Git,
   ou `vercel project inspect <projet>`). Un push sur une autre branche donne
   un déploiement *preview* : c'est la cause de « ça met en preview ».
   Soit fusionner dans la branche de production, soit `vercel --prod` depuis
   le dossier lié (`.vercel/project.json`).
3. Pousser (`git push`) — Rafaël autorise le push sur la branche principale
   quand le travail est fini et vérifié.
4. Suivre : `vercel ls <projet>` jusqu'à `Ready` ; en `Error` :
   `vercel inspect <url> --logs`, corriger la cause, recommencer.
5. **Prouver en ligne** : ouvrir l'URL du domaine (pas l'URL `*.vercel.app`)
   et vérifier la modification elle-même (texte, page, en-tête HTTP) ; pour une
   interface, capture ordinateur et téléphone.

Fini quand le changement est visible sur le domaine de production.

## Variables d'environnement

- Lister : `vercel env ls` (noms seulement). Ajouter : `vercel env add NOM
  production` en saisie masquée par Rafaël, ou le skill `poser-secret`.
- Une variable modifiée n'agit qu'au **prochain** déploiement : redéployer.
- `NEXT_PUBLIC_*` est visible dans le navigateur : jamais de clé secrète dedans.

## Stockage de déploiements saturé

```
node ~/.claude/skills/vercel-prod/nettoyer-deploiements.mjs --projet <nom>              # simulation
node ~/.claude/skills/vercel-prod/nettoyer-deploiements.mjs --projet <nom> --garder 20 --appliquer
```
Le script garde la production en cours, les N plus récents et tout ce qui a
moins de 48 h, et supprime le reste en commençant par les plus anciens.
Montrer la simulation à Rafaël avant `--appliquer`. Ne toucher à rien d'autre
(domaines, variables, projet) pendant un nettoyage.

## Plusieurs sessions sur un même projet

Des worktrees ou des agents parallèles qui poussent chacun leur branche
créent des déploiements concurrents. Une seule branche part en production ;
les autres sont fusionnées dedans après relecture.
