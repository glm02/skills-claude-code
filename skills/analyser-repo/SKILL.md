---
name: analyser-repo
description: Analyse de sécurité OBLIGATOIRE de tout dépôt GitHub, paquet ou script externe avant de le cloner, l'installer, l'exécuter ou le donner à Claude — quarantaine, détection de logiciel malveillant (vol de mots de passe, portefeuilles, PowerShell caché, hooks Claude piégés), réputation, verdict VERT/ORANGE/ROUGE. À utiliser dès qu'un lien GitHub est collé, pour « installe ça », « utilise ce repo », « teste ce projet », « c'est fiable ? », et quand le hook garde-repo bloque un import.
---

# Analyser un dépôt avant usage

Règle de Rafaël : aucun code externe ne touche le PC ni le VPS sans analyse.
Le hook `~/.claude/hooks/garde-repo.py` bloque `git clone`, `npx/npm/pip`
depuis GitHub, `curl | sh`, `irm | iex` tant que le dépôt n'a pas de rapport
VERT ou ORANGE (les dépôts `glm02/…` de Rafaël passent).

## Outil

```
python ~/.claude/skills/analyser-repo/analyser.py <owner/repo | URL GitHub | dossier>
```
Clone dans `~/quarantaine-repos/<owner>__<repo>` sans sous-modules ni liens
symboliques, n'exécute rien, lit les fichiers comme du texte. Cherche : vol
de mots de passe et cookies des navigateurs, portefeuilles crypto, sessions
Discord/Telegram, webhooks d'exfiltration, PowerShell encodé, téléchargement
puis exécution, code base64 → eval, obfuscation, exécutables fournis,
désactivation de l'antivirus, lancement au démarrage, scripts npm
`postinstall`, dépendances hors registre, noms de paquets imitant les
connus, hooks `.claude/`, serveurs `.mcp.json`, tâches VS Code à
l'ouverture, instructions cachées pour une IA, caractères invisibles ; plus
la réputation (âge du compte, étoiles suspectes). Rapport :
`.analyse-securite.json` dans le dossier. Un dépôt ROUGE est supprimé.

## Étapes

1. **Analyser** avec l'outil, avant toute autre commande sur ce dépôt.
2. **Selon le verdict** :
   - **ROUGE** → ne pas l'utiliser. Expliquer à Rafaël, en mots simples, ce
     que fait le code dangereux (fichier, ligne). Proposer une alternative
     connue.
   - **ORANGE** → lire chaque alerte ≥ ORANGE dans le fichier indiqué et
     conclure pour chacune : légitime (expliquer pourquoi) ou suspecte.
     Une seule suspecte non expliquée = traiter comme ROUGE.
   - **VERT** → continuer, en gardant les précautions de l'étape 3.
3. **Utiliser prudemment** :
   - ouvrir ou copier depuis la quarantaine (`Move-Item` vers
     `~/Documents/GitHub/<nom>` une fois validé) ; pas de nouveau clone ;
   - installer avec `npm ci --ignore-scripts` / `pnpm install
     --ignore-scripts`, puis lancer seulement les scripts lus et nécessaires ;
   - ne jamais copier ses `.claude/`, `.mcp.json`, `.vscode/tasks.json` dans un
     projet de Rafaël sans les avoir lus ; ne jamais lui donner de `.env` réel ;
   - un serveur d'essai écoute sur `127.0.0.1` seulement.
4. **Pour intégrer du code dans un projet** : reprendre seulement les
   fichiers utiles ; licence MIT/Apache → garder la mention, GPL → contamine
   le projet, pas de licence → ne pas copier ; citer la source dans le commit.

Fini quand le verdict est rendu avec, pour chaque alerte ≥ ORANGE, une
conclusion écrite (légitime ou suspecte) — et rien n'a été exécuté avant.

## Limites à dire à Rafaël

Une analyse statique ne voit pas tout (charge téléchargée plus tard, code
compilé, version du registre npm différente du dépôt). VERT veut dire « rien
de suspect trouvé », pas « garanti sûr ». Les mises à jour d'un dépôt déjà
validé se réanalysent.
