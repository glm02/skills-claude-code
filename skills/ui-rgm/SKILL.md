---
name: ui-rgm
description: Reproduire l'interface du site RGM Dev (rgm-dev.site) dans un autre projet — même style bleu et blanc, mêmes composants (Appica UI, shadcn/ui sur Base UI), mêmes effets (nappe de points 3D en fond, halo bleu, comètes sur les contours, surlignage animé, texte qui se décode, apparition au défilement, orbite de logos, verre dépoli et verre liquide). À utiliser pour « copie l'UI de mon site », « même style que rgm-dev », « fais-le avec mon design », « ajoute le fond animé / l'effet verre / liquid glass », ou pour démarrer un site client avec une base soignée.
---

# Interface RGM

La référence vivante est le dépôt `rgm dev master` (site rgm-dev.site). Les
fichiers de `references/` en sont une copie : les relire avant d'écrire, et
recopier les recettes plutôt que de les réinventer.

## 1. Les bibliothèques

| Rôle | Bibliothèque | Notes |
|---|---|---|
| Composants principaux | **Appica UI** (`@appica/ui-react`) | Button, Badge, BorderBeam, GradientGlow, BackgroundPattern, TextAnimate, Tooltip, Tabs, Accordion, Sparkline… Import par composant : `@appica/ui-react/button`. Tailwind doit scanner ses fichiers : lignes `@source "../../node_modules/@appica/ui-react/dist/components/<nom>"` dans globals.css. |
| Base de composants | **shadcn/ui** style `base-nova`, sur **Base UI** et **Radix** | Dialog, Sheet, Select, Field… dans `src/components/ui`. On les possède, on les modifie. |
| Effets ponctuels | **Spell UI** (registry `@spell` : `https://spell.sh/r/{name}.json`) | blur-reveal, words-stagger, shimmer-text, marquee, tilt-card, pop-button, flow-button. |
| Animation | **Motion**, CSS (`animation-timeline: view()`), `tw-animate-css` | Pas d'IntersectionObserver pour faire apparaître du contenu. |
| 3D | **Three.js**, chargé à la demande | Nappe de points (`toile-maillage.tsx`), objets 3D des réalisations. |
| Logos | **simple-icons** | Rendus côté serveur : seul le `<path>` part au navigateur. |
| Icônes | **lucide-react** | `strokeWidth={1.75}` dans les pastilles. |
| Style | **Tailwind CSS v4**, jetons OKLCH dans `:root` / `.dark` | Police **Geist** et Geist Mono via `next/font`. |

## 2. Poser la base

```bash
bash ~/.claude/skills/ui-rgm/scripts/installer.sh <dossier-du-projet>
```

Puis, à la main :
1. **Jetons** : recopier de `references/globals.css` les blocs `:root` et `.dark`
   (échelle `--bleu-50` → `--bleu-950`, `--background`, `--foreground`,
   `--border`, `--radius: 0.75rem`…), les `@source` d'Appica, `@property
   --border-beam-angle` et les utilitaires `animate-border-beam`,
   `animate-gradient-glow`. Importer `rgm-effets.css`.
2. **Police** : Geist en `--font-sans`, Geist Mono en `--font-mono`.
3. Adapter les imports des composants copiés et remplacer `@/lib/site` par les
   données du projet. Ne jamais recopier les coordonnées de Rafaël dans le
   projet d'un client.

## 3. Les règles du style

- **Bleu et blanc.** Fond blanc, bleu seule couleur d'accent, **texte noir**,
  y compris le secondaire (pas de gris qui ne se lit pas). Hiérarchie par la
  taille et la graisse.
- **Titres** : `font-semibold`, `tracking-[-0.03em]` sur le h1, `text-balance`.
  Surtitre : `text-sm font-semibold tracking-wider uppercase text-bleu-600`.
- **Cartes** : `rounded-3xl border border-border/70 bg-background p-6`,
  survol `hover:-translate-y-0.5 hover:border-bleu-300
  hover:shadow-[0_14px_40px_-20px_var(--bleu-600)]`.
- **Bouton principal** : Appica `Button variant="primary"`, `h-13 rounded-2xl`,
  ombre `0_14px_40px_-16px_var(--bleu-600)`, comète blanche `BorderBeam
  revealOn={["hover","press"]}`. Secondaire : `variant="soft"`.
- **Pastilles d'icône** : `size-11 rounded-2xl bg-bleu-50 text-bleu-700`.
- **Mouvement** : 150–300 ms, `ease-out`, `active:scale-96` sur ce qui se
  clique, défilements continus en `linear`. `prefers-reduced-motion` respecté
  partout : image fixe, jamais un trou.
- **Un seul élément vivant par zone** (badge à comète, ou halo, ou orbite).
  Si tout bouge, plus rien ne ressort.

## 4. Les effets (fichier de référence)

| Effet | Où le prendre | Usage |
|---|---|---|
| Nappe de points 3D en fond | `composants/toile-maillage.tsx` | `<ToileMaillage fixe />` en fond de l'accueil ; shaders, pause hors écran, masque central pour garder le texte lisible. |
| Halo bleu | `effets.css` → `halo-bleu` | Derrière le titre d'une page, un seul par écran. |
| Comète sur un contour | Appica `BorderBeam` (`hero.tsx`, `appel-action.tsx`) | Badge « disponible », bloc d'appel à l'action (deux comètes décalées). |
| Trame qui s'éclaire sous le pointeur | Appica `BackgroundPattern spotlight` | Fond du bloc d'appel à l'action. |
| Surlignage animé | `composants/surligne.tsx` | Les mots clés du h1. |
| Texte qui se décode / mots qui s'allument | `composants/texte-anime.tsx` (Appica TextAnimate) | Surtitres (`scramble`), chapeau (`highlight`). |
| Apparition au défilement | `effets.css` → `.apparait`, `composants/apparait.tsx` | Sections et cartes ; décalage par `delai`. |
| Défilement de logos | `composants/marquee.tsx` + `tuile-logo.tsx` | Bandes de logos, pause au survol, fondu aux bords. |
| Orbite de logos | `composants/orbite-stack.tsx` + `effets.css` | Visuel de hero, 100 % CSS. |
| Schéma animé | `composants/schema-hermes.tsx` | Flux entrée → agent → sorties, points en `animateMotion`, version verticale sur téléphone. |
| Verre dépoli | `effets.css` (section 1) | En-tête au défilement, badges, bandeaux posés sur un fond animé. |
| Verre liquide | `effets.css` → `verre-liquide` | Carte ou bouton phare, une fois par écran ; repli en fond plein sans `backdrop-filter`. Pas encore utilisé sur rgm-dev.site. |
| Panneau opaque | `composants/panneau.tsx` | Une section posée sur la nappe de points. |

## 5. Vérifier

Captures téléphone (390 px) et ordinateur (1440 px), thème clair et sombre,
avec et sans « réduire les animations » (skill `audit-mobile`). Pas de
débordement horizontal, contrastes AA, focus visibles au clavier. Le verre et
la nappe ne doivent jamais rendre un texte illisible.
