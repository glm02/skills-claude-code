---
name: jev
description: Noter des options avec un pourcentage pour aider à trancher vite. À utiliser dès que Rafaël hésite entre plusieurs possibilités, demande « c'est bien ou pas », « ça vaut le coup », « lequel je prends », « note-moi ça », « fais un coup de jev », ou présente un plan, une page, un texte, un devis, un prestataire, une refonte ou une dépense à arbitrer. À utiliser aussi quand une réponse se résumerait à « ça dépend » : la skill force à chiffrer au lieu de nuancer. Ne pas l'utiliser pour une question factuelle à réponse unique, ni pour exécuter une tâche déjà décidée.
---

# Jev — mettre un chiffre sur « est-ce que c'est bien »

Le but est de faire gagner trente secondes à quelqu'un qui doit choisir. Pas de
produire une étude. Une note, une phrase, et ce qui ferait changer d'avis.

Le piège de ce genre d'exercice est de sortir un nombre qui a l'air précis et
qui ne repose sur rien. Un « 73 % » inventé est pire qu'un « je ne sais pas » :
il se retient, il se cite, et il oriente une décision qu'il n'a pas méritée.
Tout ce qui suit sert à ce que le chiffre soit mérité — ou annoncé comme faible.

## La sortie

Toujours cette forme, dans cet ordre. Le verdict d'abord : c'est ce qu'on lit.

```
**Option retenue — 78 %** · confiance moyenne
Une phrase qui dit pourquoi, en termes de conséquence réelle.

| Option | Note | Ce qui la porte | Ce qui la plombe |
|---|---|---|---|
| A | 78 % | … | … |
| B | 54 % | … | … |

**Ce qui changerait la réponse :** …
```

Quand il n'y a qu'une seule chose à juger (« ce texte est bien ? »), le tableau
devient la liste des critères au lieu de la liste des options.

## Comment la note se fabrique

Trois à cinq critères, pas plus. Au-delà, la note se dilue et chaque critère
cesse de peser. Chacun reçoit un poids, et le poids se justifie par l'enjeu
réel, pas par l'habitude.

Pour chaque critère : une note sur 100 et **la source de cette note**. Une
mesure, un fait vérifié dans le dossier, ou une appréciation assumée comme
telle. Montre l'arithmétique si elle n'est pas évidente — un lecteur doit
pouvoir contester un poids plutôt que subir un total.

Un critère qu'on ne peut pas évaluer ne vaut pas zéro. Il vaut `n/a`, il sort du
calcul, et **il fait baisser la confiance, pas la note**. Confondre les deux
revient à punir une option parce qu'on manque d'information sur elle.

## La confiance, séparée de la note

Deux choses différentes, et c'est le cœur de la méthode :

- **la note** dit à quel point c'est bien ;
- **la confiance** dit à quel point on peut se fier à la note.

« 85 %, confiance faible » est une information honnête et utile. « 85 % » tout
court, quand trois critères sur cinq sont des impressions, est un mensonge
poli.

| Confiance | Quand |
|---|---|
| forte | tous les critères reposent sur des faits vérifiables, échantillon suffisant |
| moyenne | un critère sur appréciation, ou une mesure à petit effectif |
| faible | deux critères ou plus sans donnée, ou un chiffre invérifiable en l'état |

Sous une trentaine d'observations, dis-le. Un pourcentage calculé sur six cas
peut n'être que du bruit, et l'annoncer vaut mieux qu'une belle flèche verte.

## Le veto n'appartient pas à la note

Une note élevée ne déclenche rien. Elle recommande, elle n'autorise pas.

Restent à l'humain, quelle que soit la note : supprimer, envoyer à de vrais
clients, dépenser, publier, déployer, fusionner, changer une offre. La règle
tient à une raison simple : un modèle qui classe bien peut se tromper d'un cran
sans qu'on le voie, et un cran de trop sur une action irréversible ne se rattrape
pas. Quand un garde-fou peut s'écrire dans le code plutôt que dans une consigne,
écris-le dans le code : une consigne s'oublie, une condition non.

Si l'option la mieux notée implique une de ces actions, la sortie se termine par
la demande explicite, pas par l'exécution.

## Ce qui disqualifie d'office

Avant de noter, écarte ce qui ne peut pas passer, et dis-le en une ligne au lieu
de lui donner une note basse. Une option interdite n'est pas « moins bonne »,
elle est hors jeu, et la noter 12 % laisse croire qu'elle reste discutable.

Sur les projets de Rafaël, cela comprend notamment : écrire « RGE », faire payer
le déplacement, prospecter par email ou SMS sur la climatisation, la pompe à
chaleur, l'installation ou le remplacement de chaudière, la salle de bains PMR
ou l'isolation (article L. 223-8), créer une page satellite par commune, ou
ajouter un fichier dans `api/` du site. Vérifie le `CLAUDE.md` du dossier : il
fait foi, et il évolue.

## Deux exemples

**Choisir entre deux chantiers de référencement**

```
**Repointer les pages métier — 82 %** · confiance moyenne
« plombier la ciotat » fait 79 apparitions en 6e place et zéro clic, parce que
Google montre l'accueil : le gain est identifié et la correction tient en un
titre.

| Option | Note | Ce qui la porte | Ce qui la plombe |
|---|---|---|---|
| Repointer les pages métier | 82 % | cause mesurée, correction d'une heure | effet visible sous 4 à 8 semaines |
| Écrire 10 articles | 41 % | utile à terme | aucune demande mesurée dessus, n/a sur le volume |

**Ce qui changerait la réponse :** un relevé montrant que l'accueil convertit
déjà sur cette requête.
```

**Juger une seule chose**

```
**Le texte tient — 68 %** · confiance faible
Il dit ce qu'il faut, mais rien n'y prouve que le déplacement est offert, et
c'est l'argument qui fait décrocher le téléphone.

| Critère | Poids | Note | Source |
|---|---|---|---|
| Promesse claire | 40 % | 80 | lecture |
| Preuve chiffrée | 30 % | n/a | aucun tarif cité |
| Appel à l'action | 30 % | 55 | lecture |

**Ce qui changerait la réponse :** ajouter le prix de départ et la mention du
déplacement offert.
```

## Le ton

Pas de « il convient de ». Pas de récapitulatif de la méthode avant la réponse.
Le chiffre, la raison, la suite. Si la note est basse, dis-le sans tourner
autour ; si elle est haute mais la confiance faible, c'est la confiance qu'on
lit en premier dans la phrase.
