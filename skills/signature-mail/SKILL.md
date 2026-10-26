---
name: signature-mail
description: Créer une signature d'email HTML (Gmail, Outlook web et bureau) — pro ou école, avec logo, lien du site, couleurs — et expliquer où la coller. À utiliser pour « fais-moi une signature de mail », « signature Gmail / Outlook », « signature pour RGM Dev ou pour mes candidatures ».
---

# Signature d'email

## Étapes

1. **Contenu** : nom, titre (ex. « Étudiant en génie électrique — BUT GEII »
   ou « Développeur web & agents IA — RGM Dev »), site, éventuellement
   LinkedIn et téléphone pro. Demander quelle variante (école, candidatures,
   pro) : jamais de numéro ou d'adresse personnels non voulus.
2. **HTML compatible messageries** : tableau (`<table>`), styles **en ligne**
   uniquement, polices système (Arial, Helvetica), largeur ≤ 500 px, pas de
   CSS externe ni de SVG (Outlook ne l'affiche pas). Logo en PNG hébergé
   en HTTPS sur le site (ex. `https://www.rafaelgmille.site/logo.png`),
   avec `width`/`height` et `alt` ; 2× la taille affichée pour la netteté.
   Couleurs : celles du site (bleus), texte gris foncé, liens soulignés
   discrets.
3. **Fichier** `signature-<variante>.html` sur le Bureau, ouvert dans le
   navigateur pour vérifier le rendu.
4. **Installer**, expliqué à Rafaël :
   - Gmail : ouvrir le fichier dans Chrome, tout sélectionner (Ctrl+A),
     copier, puis Gmail → Paramètres → Voir tous les paramètres →
     Signature → coller ; « Insérer la signature avant le texte cité » ;
   - Outlook web : Paramètres → Courrier → Composer et répondre → coller ;
   - Outlook bureau : Fichier → Options → Courrier → Signatures → coller.
5. Faire envoyer un email de test vers une autre boîte (téléphone compris).

Fini quand l'email de test s'affiche correctement sur ordinateur et téléphone.
