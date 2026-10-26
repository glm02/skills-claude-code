---
name: vps-sante
description: Bilan de santé et dépannage du VPS Contabo (ssh contabo-vps) — serveur injoignable, service Hermes ou Atout en échec, disque plein, ports exposés, mises à jour, CrowdSec. À utiliser pour « le serveur est down ? », « Hermes répond plus », « vérifie le VPS », après une mise à jour ou un redémarrage, et en routine hebdomadaire.
---

# Santé du VPS

## Outil

```
ssh contabo-vps 'bash -s' < ~/.claude/skills/vps-sante/bilan.sh
```
Lecture seule. Chaque ligne commence par OK / ATTENTION / ALERTE.
Le contexte de l'infrastructure est dans la mémoire `vps-contabo-infra.md`,
les règles d'exploitation dans `/root/.hermes/AGENTS.md` (§1).

## Étapes

1. **Joignable ?** Si `ssh` échoue : `Test-NetConnection <ip-du-vps> -Port 22`
   puis `-Port 443`. Injoignable sur les deux : panne ou arrêt chez Contabo →
   regarder https://contabo-status.com et le panneau client ; préparer pour
   Rafaël le message au support (date, heure, symptôme). Ne pas insister en
   boucle : CrowdSec bannit l'IP du poste après trop d'échecs SSH.
2. **Bilan** : lancer l'outil.
3. **Chaque ALERTE** : `systemctl status <unité>` et
   `journalctl -u <unité> -n 50 --no-pager`, trouver la cause. Distinguer :
   - une panne (service planté, dépendance cassée) → corriger, puis
     `systemctl restart <unité>` (jamais `pkill` ni relance à la main) ;
   - un réglage métier manquant (ex. destinataire non configuré dans l'admin
     Atout) → le signaler à Rafaël, ne rien inventer ;
   - une source externe cassée (flux tiers) → rendre le script tolérant.
   Le code des services Atout vit dans le dépôt `Atout-travaux` (PC) et se
   déploie par `git pull` dans `/root/projets/atout-travaux` : corriger côté
   PC, pousser, puis tirer sur le VPS.
4. **Chaque ATTENTION** : port Docker public, paquets de sécurité, disque
   > 80 % → proposer l'action ; mises à jour de sécurité : `apt upgrade`
   autorisé, redémarrage du serveur seulement avec l'accord de Rafaël.
5. Relancer l'outil : plus d'ALERTE, ou chacune expliquée.

Fini quand chaque ALERTE est corrigée (preuve : `is-active`, ou une
exécution réussie de l'unité) ou remise à Rafaël avec sa cause exacte.

## Règles

- Avant de modifier un fichier verrouillé (`lsattr` montre `i`) : il l'est
  exprès ; `chattr -i`, modifier, `chattr +i`, garder une copie datée.
- Aucun secret affiché : `/etc/hermes-secrets/*.env` se lit par noms de clés.
