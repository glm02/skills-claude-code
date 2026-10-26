---
name: envoyer-telegram
description: Envoyer à Rafaël sur son Telegram ce qu'il doit voir — vidéo rendue, lien d'aperçu ou de production, capture, PDF, fichier, message de fin de tâche. À utiliser dès qu'un livrable à montrer est prêt (rendu HyperFrames, déploiement Vercel, captures d'audit, devis), et pour « envoie-le-moi sur Telegram », « pousse-moi la vidéo », « mets le lien sur mon Telegram ».
---

# Envoyer sur Telegram

## Outil

```
python ~/.claude/skills/envoyer-telegram/envoyer.py <fichier-ou-url> [...] -m "légende"
python ~/.claude/skills/envoyer-telegram/envoyer.py -m "message seul"
python ~/.claude/skills/envoyer-telegram/envoyer.py --test
```
Type deviné : vidéo lisible directement dans Telegram (recompressée sous
50 Mo si besoin), image, lien avec grand aperçu, sinon document. La légende
s'attache au premier élément. `--essai` montre ce qui partirait sans rien
envoyer.

Configuration : `~/.claude/secrets/telegram.env` (`TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`), posée par Rafaël avec
`powershell -ExecutionPolicy Bypass -File ~/.claude/skills/envoyer-telegram/poser-bot.ps1`.
Si l'outil répond « Bot non configuré », lui donner cette commande (préfixe
`!` dans Claude Code) et continuer la tâche sans attendre.

## Quand envoyer, sans qu'on le demande

Au moment où le livrable est **vérifié** (pas avant) :
- vidéo rendue et contrôlée → le MP4, légende = sujet, durée, format ;
- déploiement → l'URL de production (ou d'aperçu Vercel) avec ce qui a changé ;
- audit visuel → 1 à 3 captures téléphone les plus parlantes ;
- document pour un client ou l'école → le PDF, avec « brouillon à relire ».
Un envoi par livrable, regroupé (plusieurs fichiers dans une commande),
pas un message par étape intermédiaire.

## Légende

Française, 1 à 3 lignes : ce que c'est, ce qu'il doit regarder ou décider.
Ex. « Vidéo stage v2 (31 s, vertical) — dis-moi si le rythme du début te va. »

## Règles

- Ce bot sert uniquement à ces livraisons : jamais le jeton d'Hermes ou d'un
  bot client, jamais ce jeton ailleurs.
- Rien de confidentiel d'un client (données INFast, adresses, numéros) ni
  aucun secret dans un message : Telegram n'est pas chiffré de bout en bout
  pour les bots.
- Le jeton ne s'affiche jamais ; ne pas lire `telegram.env` dans la conversation.
