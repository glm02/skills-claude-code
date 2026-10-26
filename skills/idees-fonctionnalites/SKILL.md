---
name: idees-fonctionnalites
description: Trouver et classer des idées de fonctionnalités, d'améliorations ou d'effets pour un site, une admin ou une app — inspirées des meilleurs produits du domaine, notées par utilité et effort — puis construire celles retenues. À utiliser pour « trouve-moi 20 idées », « quelles fonctionnalités rajouter », « fais un truc à 10k », « qu'est-ce qu'on pourrait automatiser », « trouve encore mieux ».
---

# Idées de fonctionnalités

Rafaël demande souvent « 20 idées » : il en veut beaucoup pour choisir vite,
mais chacune doit être concrète et classée.

## Étapes

1. **Comprendre l'usage réel** avant d'imaginer : qui utilise quoi, chaque
   jour (lire le code des pages, l'admin, les retours des utilisateurs, les
   données d'usage s'il y en a). Noter ce qui existe déjà pour ne pas le
   reproposer.
2. **S'inspirer** de 3 à 5 produits de référence du domaine (logiciels
   métier, SaaS connus, concurrents directs) : ce qu'ils font qui manque ici.
   Citer la source de chaque inspiration.
3. **Lister** le nombre demandé (20 par défaut), chaque idée en 3 lignes :
   - ce que l'utilisateur peut faire (une phrase, pas de jargon) ;
   - le gain : temps gagné, client en plus, erreur évitée ;
   - l'effort : S (< 1 h), M (une demi-journée), L (plus), et le coût
     mensuel s'il y a un service payant.
4. **Classer** avec le skill `jev` : score d'utilité en %, tri par
   utilité ÷ effort. Mettre en tête les gratuites à fort impact.
5. **Écrire** le tableau dans `IDEES.md` du projet (date, idée, gain, effort,
   score, statut) pour que les prochaines demandes partent de là et ne
   reproposent pas les mêmes.
6. Si Rafaël dit « fais tout » ou « fais les meilleures » : construire dans
   l'ordre du classement, une idée = un commit vérifié ; au-delà de 3 idées
   indépendantes, paralléliser avec le skill `orca-agents`.

Fini quand chaque idée a gain, effort et score, que `IDEES.md` est à jour,
et — si la construction a été demandée — que chaque idée faite est vérifiée.

## Filtre

Écarter : ce qui ajoute du texte ou des écrans sans gain clair (Rafaël veut
épuré), ce qui contredit une règle du projet (`AGENTS.md`), les gadgets.
