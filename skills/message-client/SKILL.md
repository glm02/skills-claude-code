---
name: message-client
description: Rédiger un message de Rafaël à un client (email, WhatsApp, SMS) — compte rendu de ce qui a été fait, réponse à une demande, relance de paiement, annonce d'une nouveauté, consignes. À utiliser pour « fais-moi le mail pour Valérie », « récapitule ce qu'on a fait », « brouillon pour qu'elle me paye », « réponds à ce mail ».
---

# Message à un client

Rafaël est développeur indépendant (sites, admin, agents IA). Ses clients ne
sont pas techniques : ils veulent savoir ce qui change pour eux.

## Étapes

1. **Rassembler les faits** — ce qui a vraiment été livré depuis le dernier
   message : `git log --since=<date> --oneline` du projet, déploiements en
   ligne, demandes du client restées ouvertes. Ne citer que ce qui est en
   ligne et vérifié.
2. **Écrire** selon le type :
   - *compte rendu* : 3 à 6 points « ce que vous pouvez faire maintenant »,
     chacun en une phrase concrète (« Dans l'admin, onglet Rappels, un clic
     envoie le SMS de rappel »), puis ce qui reste et qui le fait ;
   - *réponse* : reprendre chaque question du client, une réponse par question ;
   - *relance de paiement* : rappeler la valeur livrée (application sur mesure,
     pas un simple site), puis le montant exact, ce qui a déjà été payé, ce
     qui reste, l'échéance. Ton cordial et ferme, pas d'excuse ;
   - *consignes* : étapes numérotées, une action par étape, où cliquer.
3. **Relire** : chaque montant et chaque date recoupés avec la source
   (devis, échange précédent) ; aucun mot technique sans traduction.
4. **Livrer en brouillon** dans la conversation, prêt à copier. Ne jamais
   l'envoyer soi-même : l'envoi est fait par Rafaël.

## Style

- Français, **vouvoiement**, phrases courtes, chaleureux mais professionnel.
- Objet d'email court et précis. Signature « Rafaël ».
- WhatsApp/SMS : 2 à 5 lignes, pas de mise en forme lourde.
- Pas de position Google ni de chiffre gênant non demandé ; parler des
  résultats en demandes reçues et en temps gagné.
- Jamais de mot de passe dans un message : indiquer comment il sera transmis.
