---
name: poser-secret
description: Faire poser une clé d'API, un jeton ou un mot de passe par Rafaël sans qu'il passe par la conversation — sur le VPS, dans Vercel ou dans un .env.local — avec vérification de la clé avant écriture. À utiliser pour « donne-moi le script pour mettre la clé », « j'ai la clé API », « mets le mot de passe admin », ou dès qu'un service a besoin d'un secret.
---

# Poser un secret

Un secret ne passe jamais par la conversation, un commit, un journal ou une
note. Rafaël le saisit lui-même, en saisie masquée ; le script vérifie la clé
auprès du service avant de l'écrire.

## Où le mettre

| Usage | Emplacement |
|---|---|
| Service sur le VPS | `/etc/hermes-secrets/<service>.env`, `root:root`, `chmod 600` (ou `root:<groupe>` 640 si un compte de service doit le lire) |
| Hermes | `/root/.hermes/.env` (600) |
| Site Vercel | variable d'environnement du projet (`production`, et `preview` si utile) |
| Développement local | `.env.local` à la racine du projet, ignoré par git |

## Étapes

1. **Écrire le script** dans le dossier scratchpad (jamais dans le dépôt
   s'il contient autre chose que la logique) :
   - VPS : bash, `read -rsp "Clé <SERVICE> : " CLE`, puis un appel de test
     (`curl -s -o /dev/null -w '%{http_code}'` sur un point d'accès en
     lecture du service) ; écrire seulement si 200, sinon afficher le code et
     s'arrêter. Écriture : `install -m 600 /dev/null <fichier>` puis ajout de
     `NOM=valeur` en remplaçant une ancienne ligne `NOM=` ; ne jamais faire
     `echo $CLE` ni l'afficher ; redémarrer le service qui la lit.
   - Vercel : `vercel env add <NOM> production` (saisie masquée par la CLI),
     puis redéployer.
   - Windows : PowerShell avec `Read-Host -AsSecureString`, converti au
     moment de l'écriture seulement.
2. **Donner la commande exacte** à Rafaël, à taper avec le préfixe `!` dans
   Claude Code ou dans son terminal. Pour le VPS :
   `ssh -t contabo-vps 'bash -s' < <script>` ne permet pas la saisie : copier
   d'abord le script (`scp`) puis `ssh -t contabo-vps bash /root/<script>`,
   et le supprimer après.
3. **Vérifier** sans voir la valeur : présence du nom (`grep -c '^NOM=' <fichier>`),
   longueur, droits (`stat -c '%a %U:%G'`), et un appel réel du service qui
   l'utilise (code HTTP).

Fini quand l'étape 3 montre le bon nom, les bons droits et un appel réussi.

## Rappels

- Une clé collée par erreur dans la conversation est compromise : la
  révoquer chez le fournisseur et en poser une nouvelle.
- `NEXT_PUBLIC_*` et tout ce qui part au navigateur n'est pas secret.
