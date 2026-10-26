---
name: esp32-arduino
description: Programmer une carte ESP32 ou Arduino depuis le terminal avec arduino-cli — compiler, téléverser, moniteur série, bibliothèques, Wi-Fi, capteurs, envoi vers Telegram ou une page web, dépannage du port COM. À utiliser pour « téléverse sur l'ESP32 », « mon ESP32 ne se connecte pas », « lis le capteur », un sketch .ino ou un projet objet connecté.
---

# ESP32 et Arduino en ligne de commande

`arduino-cli` 1.5 : `~/arduino-cli/arduino-cli.exe` (pas dans le PATH :
l'appeler par son chemin). Cœurs installés : `esp32:esp32`, `arduino:avr`.

## Étapes

1. **Carte et port** : `arduino-cli board list`. Pas de port COM →
   câble USB de charge seule, ou pilote CP210x / CH340 manquant (le dossier
   `~/cp210x_driver` contient le pilote CP210x).
2. **Projet** : un dossier `<nom>/<nom>.ino`. Les secrets (Wi-Fi, jeton de
   bot) vont dans `secrets.h`, listé dans `.gitignore`, avec un
   `secrets.exemple.h` versionné.
3. **Bibliothèques** : `arduino-cli lib search <nom>`, `lib install "<nom>"`.
   Noter les versions dans le README.
4. **Compiler** : `arduino-cli compile --fqbn esp32:esp32:esp32 <dossier>`
   (`arduino-cli board listall esp32` pour le FQBN exact de la carte).
5. **Téléverser** : `arduino-cli upload -p COM<n> --fqbn <fqbn> <dossier>`.
   « Failed to connect » : maintenir BOOT pendant le début du téléversement.
6. **Lire** : `arduino-cli monitor -p COM<n> --config baudrate=115200`.
   Le moniteur bloque le port : le fermer avant un nouveau téléversement.

Fini quand le moniteur série montre le comportement attendu (mesure, Wi-Fi
connecté, message envoyé).

## Repères ESP32

- GPIO 34 à 39 : entrées seulement, sans pull-up. ADC2 inutilisable quand le
  Wi-Fi est actif : lire les capteurs analogiques sur ADC1 (GPIO 32 à 39).
- Logique 3,3 V : pas de 5 V directement sur une broche ; relais ou triac
  par transistor ou optocoupleur.
- Wi-Fi : reconnexion dans `loop()` si `WiFi.status() != WL_CONNECTED`.
- Telegram : HTTPS vers `api.telegram.org` avec `WiFiClientSecure` (certificat
  racine ou `setInsecure()` pour un prototype, à dire) ; un bot par usage.
- Mesure de courant (ex. ACS712 / Allegro) : moyenne efficace sur plusieurs
  périodes de 50 Hz, étalonnage du zéro au démarrage.
