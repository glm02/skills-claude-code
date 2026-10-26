---
name: orca-agents
description: Piloter les sous-agents Codex et Claude dans Orca — découper un chantier en workers parallèles, suivre leurs messages, récupérer et fusionner leur travail, puis trier et fermer ceux qui ne servent plus. À utiliser pour « lance des sous-agents Codex », « délègue tout », « trie les sous-agents, garde l'essentiel », « ferme ceux qui servent plus », ou « You have N orchestration messages ».
---

# Sous-agents Orca

La méthode complète d'Orca est dans son propre skill : `orca skills get
orchestration` (version alignée sur la CLI installée). La lire avant de
lancer des workers. Ce skill-ci couvre ce qui revient chez Rafaël.

## Lancer un chantier en parallèle

1. Découper en tâches **indépendantes** (fichiers différents) : deux workers
   sur le même fichier = conflit à la fusion.
2. Chaque consigne de worker contient : le but, les fichiers concernés, la
   boucle de vérification du dépôt (`AGENTS.md`), « réponds en français »,
   et ce qu'il ne doit pas toucher. Un worker ne pousse pas sur `main`.
3. Suivre avec `orca orchestration check` ; répondre aux questions avec
   `reply`. Avant d'envoyer un message, vérifier le worktree du destinataire
   (`worker-show`) : l'ordre affiché trompe.

## Trier les workers (« garde l'essentiel »)

1. Inventaire : `orca orchestration worker-list --terminal-state active --json`
   puis `reclaimable` et `retained`. Pour chacun : tâche, run, worktree.
2. Pour chaque worker, décider en lisant son travail (`worker-read`
   et, dans son worktree, `git log main..HEAD --oneline` + `git status`) :
   - **à récupérer** : commits utiles non fusionnés → relire le diff,
     lancer les tests, fusionner dans la branche principale ;
   - **fini et fusionné** : rien d'unique → `worker-release` ;
   - **en cours et utile** : le laisser tourner ;
   - **inutile / bloqué / doublon** : `worker-stop`.
3. Ne supprimer un worktree qu'après avoir vérifié qu'il n'a ni commit
   unique ni fichier modifié ; `worker-stop` ne supprime jamais de worktree.
4. Rendre un tableau : worker, tâche, décision, ce qui a été fusionné.

Fini quand chaque worker actif a une décision appliquée, et qu'aucun commit
utile n'est resté dans un worktree non fusionné.

## Limites

Quand les agents atteignent leur quota (« ont tapé leur limite »), ne pas
relancer en boucle : noter où chacun s'est arrêté et reprendre plus tard.
