---
name: devis-freelance
description: Chiffrer et rédiger un devis ou une facture de Rafaël développeur (site, admin, agent IA, maintenance mensuelle), estimer le temps passé et le taux horaire. À utiliser pour « fais-moi un devis », « combien je lui fais payer », « on a passé combien de temps », « facture », « forfait mensuel ».
---

# Devis et facture freelance

## Repères de prix (précédent réel)

Un projet livré (site vitrine + admin sur mesure + agent IA multi-profils,
puis un forfait mensuel couvrant abonnement IA, serveur, envois email/SMS de
base, maintenance et petites évolutions) sert d'ancrage. Ses montants restent
dans les notes privées ; les prix publics sont ceux de la page tarifs.
S'en servir comme ancrage, ajusté à l'ampleur du nouveau projet.

## Estimer le temps passé

Sessions Claude du projet : `~/.claude/projects/<dossier-du-projet>/*.jsonl`
(horodatages des messages) + `git log --format='%ad' --date=iso`. Compter des
plages de travail (écart < 45 min = même plage), sommer, arrondir à l'heure.
Donner une fourchette, et le taux horaire obtenu = prix / heures.

## Étapes

1. **Émetteur** : lire `~/.claude/skills/devis-freelance/emetteur.local.json`
   (nom commercial, statut, SIRET, adresse pro, IBAN, mention TVA). S'il
   n'existe pas, demander les valeurs à Rafaël et le créer. Ce fichier reste
   local : jamais dans un dépôt git ni une page publiée.
2. **Lignes** : une ligne par livrable compréhensible par le client (« Espace
   administrateur : devis, rappels, campagnes SMS/email »), quantité, prix
   unitaire HT, total. Abonnement mensuel sur une ligne à part avec ce qu'il
   inclut et ce qu'il n'inclut pas (gros développements = devis séparé).
3. **Mentions obligatoires** : numéro (AAAA-NNN), date, durée de validité
   (30 jours), identité des deux parties, total HT, TVA ou « TVA non
   applicable, art. 293 B du CGI » selon le statut, conditions de paiement,
   acompte, pénalités de retard et indemnité forfaitaire de 40 € (client pro).
   Facture : en plus, date de la prestation et date d'échéance.
4. **Produire** un HTML propre (bleu sobre, A4) dans le dossier du projet
   hors git ou sur le Bureau, puis le PDF :
   `msedge --headless --print-to-pdf="<sortie>.pdf" "<fichier>.html"`.
   Ouvrir le PDF et vérifier les totaux (somme des lignes = total).
5. Proposer le message d'accompagnement avec le skill `message-client`.

Fini quand le PDF existe, que chaque total est recalculé juste, et que les
mentions de l'étape 3 y figurent toutes.
