---
name: audit-projets
description: Audit de tous les dépôts git de Rafaël (PC) — travail non commité ou non poussé, secrets suivis par git, failles npm critiques. À utiliser pour « audite mes projets », « fais le point sur mes repos », « j'ai rien oublié de pousser ? », ou avant de rendre un dépôt public.
---

# Audit des projets

## Étapes

1. Lancer le script (compter 5 à 10 min avec `--npm`) :
   `python -I ~/.claude/skills/audit-projets/audit.py --npm`
   Sans `--npm` : 30 s, sans les failles npm. `--racine <dossier>` pour un seul dépôt.
2. Pour chaque ligne « Secrets suivis » non nulle, ouvrir le fichier à la ligne
   indiquée et qualifier : vraie clé, clé publique par conception, ou exemple.
   Ne jamais afficher la valeur, seulement le type et l'emplacement.
3. Pour chaque dépôt « à soi » avec failles critiques ou hautes : noter si le
   projet est en ligne (Vercel, VPS) — seuls ceux-là sont urgents.
4. Rendre un rapport court, trié par urgence :
   - **À traiter maintenant** : secret réel dans git, faille critique sur un site en ligne.
   - **À pousser** : dépôts « à soi » avec fichiers modifiés ou commits non poussés.
   - **Ménage possible** : clones tiers jamais modifiés, doublons, dépôts sans remote.

L'audit est fini quand chaque dépôt « à soi » est classé dans une de ces trois
cases ou déclaré sain.

## Règles

- Un secret déjà poussé est compromis même après suppression : il faut le
  **révoquer et le régénérer** chez le fournisseur, pas seulement l'effacer.
  Réécrire l'historique git seulement avec l'accord de Rafaël.
- Clé Supabase `anon` dans le code navigateur : normal, si la RLS est active
  sur toutes les tables. `service_role` dans le code : alerte maximale.
- Les dépôts « tiers » (forks, clones d'outils) ne sont pas audités pour les
  secrets ; ne jamais committer ni pousser dessus.
- Corriger une faille npm : `npm audit fix` (sans `--force`), puis build et
  tests ; un saut de version majeure se propose à Rafaël avant.
