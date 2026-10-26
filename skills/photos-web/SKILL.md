---
name: photos-web
description: Préparer un lot de photos pour un site — retirer les coordonnées GPS et autres métadonnées, redresser, redimensionner, WebP + JPEG, noms propres, flouter visages ou plaques. À utiliser pour « ajoute ces photos », « enlève les coordonnées GPS », « j'ai mis les nouvelles photos », un dossier ou un zip de photos client, ou avant toute publication d'image.
---

# Photos pour le web

## Outil

```
python ~/.claude/skills/photos-web/preparer.py <dossier-source> <dossier-sortie> [--largeur 1600] [--qualite 80]
```
Les originaux ne sont jamais modifiés. Le script annonce combien de photos
avaient du GPS et vérifie qu'aucune sortie ne garde de métadonnées.

## Étapes

1. **Source** : un zip se décompresse dans un dossier neuf (scratchpad),
   jamais directement dans le dépôt.
2. **Préparer** avec l'outil vers un dossier de sortie hors dépôt.
   Largeurs usuelles : 1600 (photo pleine largeur), 1080 (carte, galerie),
   600 (vignette).
3. **Regarder** chaque photo (Read sur le fichier) avant publication :
   - visage d'une personne, plaque d'immatriculation, numéro de rue, nom sur
     une boîte aux lettres, document lisible → flouter :
     `magick in.jpg -region <l>x<h>+<x>+<y> -blur 0x25 out.jpg` ;
   - photo floue, en double ou hors sujet → la mettre de côté et le dire.
4. **Intégrer** dans le projet (`public/…` ou `assets/…`), `<img>` avec
   `width`/`height`, `alt` descriptif en français, `loading="lazy"` sauf la
   première image visible. Préférer `<picture>` WebP + JPEG si le projet
   n'a pas d'optimiseur d'images.
5. Vérifier la page avec le skill `audit-mobile`.

Fini quand chaque photo publiée a été vue, sans métadonnées (ligne
« Métadonnées restantes : aucune ») et sans donnée identifiante visible.

## Règles

- Photos des parents, de la maison familiale, de l'adresse de Rafaël : jamais
  dans un dépôt git ni une page publique.
- Les photos d'un client ne servent qu'à son site, sauf accord écrit pour le
  portfolio de Rafaël.
