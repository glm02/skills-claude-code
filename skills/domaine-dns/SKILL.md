---
name: domaine-dns
description: Brancher ou dépanner un nom de domaine — Vercel, Resend (envoi et réception), Cloudflare, Gandi, Namecheap, Google Search Console, Bing — et vérifier la propagation. À utiliser pour « branche le domaine », « Invalid Configuration », « Resend ne valide pas », « enregistrement CNAME refusé », « les mails arrivent en spam », ou une zone DNS collée.
---

# Domaine et DNS

Rafaël colle souvent la zone DNS ou l'écran d'erreur du registrar : partir de
là, puis vérifier soi-même sur Internet.

## Étapes

1. **Lire l'état réel**, depuis Internet et non depuis l'interface :
   `nslookup -type=A <domaine> 1.1.1.1`, puis `-type=CNAME www.<domaine>`,
   `-type=MX`, `-type=TXT`, `-type=TXT resend._domainkey.<domaine>`,
   `-type=TXT _dmarc.<domaine>`. Noter le TTL.
2. **Comparer** avec ce que demande chaque service :
   - Vercel : `A @ 216.198.79.1` (valeur actuelle à relire dans Vercel →
     Domains) et `CNAME www → <valeur donnée par Vercel>` ; un seul CNAME
     par nom ;
   - Resend : enregistrements DKIM, SPF (`send.` MX + TXT) et, pour recevoir,
     le MX indiqué ; DMARC au minimum `p=none` puis durcir ;
   - Search Console / Bing : TXT de vérification à la racine.
3. **Donner les changements** sous forme de tableau Type / Nom / Valeur / TTL,
   avec ce qu'il faut **supprimer** d'abord. Pièges :
   - Gandi : nom relatif (`www`, pas `www.domaine.fr`), point final sur les
     cibles CNAME, une seule valeur par CNAME ;
   - Cloudflare : nuage gris (DNS seul) pour les enregistrements de Resend et
     de vérification Vercel ;
   - un domaine sans emails : `TXT @ "v=spf1 -all"` et DMARC `p=reject` ;
   - un domaine qui reçoit déjà des emails (MX existants) : ne jamais
     supprimer ses MX ni son SPF sans l'accord de la cliente.
4. **Avant de toucher** une zone existante : exporter ou copier l'ancienne
   zone dans le dossier du projet (hors git si elle contient des données
   perso), pour pouvoir revenir en arrière.
5. **Vérifier la propagation** avec les commandes de l'étape 1 jusqu'à voir
   les nouvelles valeurs ; baisser le TTL à 300 avant un changement prévu.
   Puis cliquer « Verify / Refresh » côté service.

Fini quand chaque service affiche « Valid / Verified » et que l'étape 1 renvoie
les valeurs attendues depuis 1.1.1.1.
