---
name: reprendre-projet
description: Reprendre un projet là où il s'était arrêté et dire ce qu'il reste à faire. À utiliser quand Rafaël écrit « continue », « il reste quoi à faire ? », « on en est où ? », « reprends le projet », ou ouvre une session sur un projet déjà commencé.
---

# Reprendre un projet

Rafaël enchaîne les sessions courtes et les « continue ». Le but : repartir du
vrai état du projet, pas d'un souvenir.

## Étapes

1. **État réel** — dans le dépôt :
   - `git status`, `git log --oneline -15`, `git branch -a`, `git stash list` ;
   - fichiers modifiés par une autre session : les relire avant d'y toucher ;
   - `CLAUDE.md`, `AGENTS.md`, et tout fichier `TODO*`, `PLAN*`, `RESTE*`,
     `ROADMAP*`, `docs/*.md` récent (`git log -5 --name-only -- '*.md'`).
2. **Dernière session** — retrouver la fin de la session précédente sur ce
   projet : `~/.claude/projects/<dossier-du-projet>/*.jsonl` le plus récent,
   lire les derniers messages de Rafaël et le dernier compte rendu.
3. **En ligne** — si le projet est déployé : comparer le dernier commit poussé
   et le dernier déploiement de production (`vercel ls <projet> --prod`).
   Un commit non déployé ou un déploiement en erreur est la première tâche.
4. **Liste « reste à faire »** — fusionner : demandes non terminées de la
   dernière session, TODO du dépôt, écarts trouvés en 1 et 3. Classer :
   bloquant / important / confort. Chaque ligne dit qui agit : moi ou Rafaël
   (accès, paiement, DNS, validation cliente).
5. **Agir** — si Rafaël a dit « continue » : enchaîner sur le premier point
   bloquant qui dépend de moi, sans redemander. S'il a demandé « il reste
   quoi ? » : rendre la liste et s'arrêter.

L'étape 4 est finie quand chaque demande de la dernière session est soit
faite (preuve : commit ou vérification en ligne), soit dans la liste.

## Fin de session

Avant de rendre la main sur un gros chantier, écrire ou mettre à jour
`RESTE-A-FAIRE.md` à la racine (court, daté, sans secret ni donnée perso),
pour que la prochaine reprise parte de là.
