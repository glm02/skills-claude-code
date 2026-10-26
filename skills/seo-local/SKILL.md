---
name: seo-local
description: Audit et campagne SEO / GEO d'un site d'artisan ou de commerce local, mesurés sur les vraies données (Search Console, Bing, GA4). À utiliser pour « améliore le SEO », « on doit être premier », « pourquoi on a chuté », « plus de demandes », « Bing / IndexNow », « être cité par les IA », ou un rapport de référencement.
---

# SEO local, mesuré

Rafaël veut « être premier partout ». La méthode qui a marché sur Atout
Travaux : partir des recherches réellement tapées, une page par intention,
mesurer, recommencer. Pas de promesse de position : on montre des chiffres.

## Outils déjà écrits (Atout Travaux, à copier pour un autre site)

Dans `~/Documents/GitHub/Atout-travaux` :
- `hermes/technique/vps/seo/insights.py` — Search Console + GA4 + Bing → résumé ;
- `hermes/technique/vps/seo/etat-indexation.py` — indexation Google page par page ;
- `hermes/technique/vps/seo/soumettre-bing.py` et `tools/seo/bing.mjs` — Bing / IndexNow ;
- `docs/seo/` et `docs/geo/journal.md` — rapports et journal des actions passées.
Les clés sont sur le VPS dans `/etc/hermes-secrets/seo.env` (root). Les
scripts tournent là-bas ; ne jamais rapatrier les clés sur le PC.

## Étapes

1. **Mesurer avant** (28 derniers jours, et la période de comparaison) :
   requêtes, impressions, clics, position moyenne par page ; pages non
   indexées ; état Bing. Sans accès aux données : le dire et demander les
   accès (Search Console « propriétaire », Bing Webmaster, GA4 lecteur).
2. **Trouver les écarts**, par ordre de gain :
   - requête avec beaucoup d'impressions, position 4–15, 0 clic → la page
     visée n'a pas le mot exact dans `<title>`, `<h1>` et première phrase ;
   - Google montre l'accueil au lieu de la page service → maillage interne
     et page service plus spécifique ;
   - page commune/service non indexée → la soumettre, la rendre unique
     (pas de copier-coller entre communes) ;
   - fiche Google Business, avis, NAP identique partout (nom, adresse, tél.).
3. **Technique** : `sitemap.xml` à jour et soumis, `robots.txt`, canonical,
   données structurées `LocalBusiness`/`Service`/`FAQPage` valides, pages
   rapides sur téléphone (LCP < 2,5 s), liens `tel:` cliquables.
4. **GEO (réponses des IA)** : réponses courtes et factuelles en tête de page
   (prix indicatifs, zone, délais), FAQ, présence dans Bing (ChatGPT/Copilot
   s'en servent), annuaires sérieux (Pages Jaunes, Apple Plans, Bing Places).
5. **Appliquer**, puis soumettre les pages changées (IndexNow / Bing, et
   inspection d'URL Google) et noter l'action datée dans le journal du projet.
6. **Rapport** : ce qui a été changé, chiffres avant, date de la prochaine
   mesure (2 à 4 semaines). Les positions ne bougent pas en un jour : le dire.

L'audit est fini quand chaque requête à plus de 50 impressions a une page
cible désignée et une action ou un « rien à faire » justifié.

## Règles

- Pas de contenu de remplissage, pas de pages communes clonées, pas de faux
  avis : Google les déclasse et la cliente y perd.
- Un rapport destiné à la cliente parle de demandes et d'appels, pas de jargon.
