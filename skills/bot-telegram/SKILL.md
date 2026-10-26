---
name: bot-telegram
description: Créer ou dépanner un bot Telegram — BotFather, jeton, commandes, boutons, notifications, webhook sur Vercel ou service sur le VPS, bot qui ne répond plus. À utiliser pour « fais-moi un bot Telegram », « envoie-moi une notif sur Telegram », « le bot répond plus », « branche Telegram sur mon site ou mon ESP32 ».
---

# Bot Telegram

## Règles

- **Un bot = un usage.** Ne jamais réutiliser le jeton d'un bot existant
  (Hermes, projets clients) : deux programmes qui lisent le même bot se
  volent les messages, et le bot semble ne plus répondre.
- Le jeton est un secret : skill `poser-secret`. Le bot ne répond qu'aux
  identifiants autorisés (liste de `chat_id` en variable d'environnement).

## Étapes

1. **Créer** : Rafaël ouvre @BotFather → `/newbot` → nom et identifiant
   (finit par `bot`) ; il pose le jeton lui-même. `/setcommands` pour le menu.
2. **Récupérer son `chat_id`** : il écrit au bot, puis
   `getUpdates` affiche `message.chat.id` (n'afficher que cet identifiant).
3. **Choisir le mode** :
   - *webhook* sur Vercel (`/api/telegram`) : route qui vérifie l'en-tête
     `X-Telegram-Bot-Api-Secret-Token`, répond 200 vite, puis
     `setWebhook?url=…&secret_token=…` ; ne pas bloquer cette route
     derrière Cloudflare ou une authentification ;
   - *long polling* sur le VPS : service systemd dédié (`Restart=always`,
     utilisateur non root, secret dans `/etc/…/<bot>.env` en 600) ; un seul
     processus par bot ;
   - *notification seule* (script, ESP32, cron) : un simple `sendMessage`,
     pas de serveur.
4. **Coder** : Node `grammy` ou Python `python-telegram-bot` ; messages en
   français, boutons `inline_keyboard` pour les actions, `parse_mode: HTML`
   en échappant le texte variable.
5. **Tester** : `getWebhookInfo` (dernière erreur, messages en attente) ou
   le journal du service, puis un vrai message depuis le téléphone.

Fini quand un message envoyé depuis le téléphone reçoit la réponse attendue
et qu'un identifiant non autorisé est ignoré.

## Bot qui ne répond plus

`getWebhookInfo` : `last_error_message`, `pending_update_count`. Webhook +
polling en même temps = conflit 409 (supprimer le webhook ou arrêter le
polling). Deux instances du même service = messages lus mais sans réponse.
Jeton révoqué dans BotFather = 401.
