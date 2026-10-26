# Skills Claude Code — RGM Dev

Les 40 skills que j'ai écrites pour travailler avec des agents IA au quotidien :
livrer des sites, brancher des automatisations, sécuriser, et garder la main
sur ce que font les agents.

Rafael — étudiant en BUT GEII et développeur freelance à Lyon · [rgm-dev.site](https://rgm-dev.site) · [portfolio](https://www.rafaelgmille.site) · [la page qui présente cette stack](https://www.rafaelgmille.site/stack)

**Installer une skill en deux minutes :** voir [Installer](#installer) plus bas, ou le
[tuto illustré pour Claude Code, Codex, l'application Claude et les autres agents](https://www.rafaelgmille.site/stack#installer).

## Pourquoi des skills

Un agent IA sans consignes refait les mêmes erreurs à chaque session. Une
skill, c'est une procédure écrite une fois, que l'agent charge quand la tâche
s'y prête : les étapes, les pièges déjà rencontrés, et surtout **la preuve
attendue** avant de dire « c'est fait ». Chaque fois qu'un problème a coûté du
temps, la leçon finit dans une skill — c'est ce qui rend les agents fiables
d'un projet à l'autre.

Trois principes reviennent partout :

- **Vérifier avant d'annoncer.** Une skill se termine sur une preuve (capture
  ordinateur et téléphone, code HTTP, test vert, mesure), jamais sur une
  promesse.
- **Aucun secret dans la conversation.** Les clés se posent par un script à
  saisie masquée qui teste la clé avant de l'écrire (`poser-secret`).
- **L'humain décide de ce qui sort.** Envoi à un client, dépense, suppression :
  l'agent prépare, Rafael valide.

## Les skills

### Agents et organisation
| Skill | Rôle |
|---|---|
| [`orca-agents`](skills/orca-agents) | Piloter des sous-agents Codex et Claude en parallèle dans Orca, trier et fusionner leur travail |
| [`reprendre-projet`](skills/reprendre-projet) | Reprendre un projet là où il s'était arrêté et dire ce qui reste |
| [`bilan-activite`](skills/bilan-activite) | Temps passé par projet, à partir des sessions et des commits |
| [`idees-fonctionnalites`](skills/idees-fonctionnalites) | Trouver et classer des idées par utilité et effort, puis les construire |
| [`jev`](skills/jev) | Noter des options en pourcentage pour trancher vite |
| [`prof-code`](skills/prof-code) | Mode apprentissage : l'agent explique au lieu d'écrire |

### Développement web
| Skill | Rôle |
|---|---|
| [`site-a-z`](skills/site-a-z) | Livrer un site Next.js de A à Z : admin, SEO, checklist de lancement |
| [`demarrer-projet`](skills/demarrer-projet) | Dépôt, `.env.example`, `AGENTS.md`, premier déploiement en quelques minutes |
| [`supabase-projet`](skills/supabase-projet) | Tables, migrations, RLS et connexion sur un site Next.js |
| [`vercel-prod`](skills/vercel-prod) | Mettre en production et prouver que c'est en ligne |
| [`domaine-dns`](skills/domaine-dns) | Brancher un domaine : Vercel, Resend, Cloudflare, Search Console |
| [`audit-mobile`](skills/audit-mobile) | Captures Playwright téléphone/ordinateur, débordements, corrections |
| [`seo-local`](skills/seo-local) | Audit et campagne SEO mesurés sur les vraies données |
| [`nettoyer-projet`](skills/nettoyer-projet) | Fichiers, dépendances et composants inutilisés |
| [`portfolio-projet`](skills/portfolio-projet) | Ajouter un projet au portfolio |
| [`photos-web`](skills/photos-web) | Retirer le GPS des photos, redimensionner, WebP |
| [`ui-rgm`](skills/ui-rgm) | Reproduire l'interface de rgm-dev.site : Appica UI, fond animé, verre dépoli et liquide |

### Sécurité
| Skill | Rôle |
|---|---|
| [`analyser-repo`](skills/analyser-repo) | Quarantaine et analyse de tout dépôt externe avant de l'exécuter |
| [`alerte-securite`](skills/alerte-securite) | Une CVE circule : sommes-nous concernés ? |
| [`audit-securite-site`](skills/audit-securite-site) | Pentest léger d'un site : admin, API, Supabase, en-têtes |
| [`audit-projets`](skills/audit-projets) | Travail non poussé, secrets suivis par git, failles npm |
| [`poser-secret`](skills/poser-secret) | Poser une clé sans qu'elle passe par la conversation |
| [`vps-sante`](skills/vps-sante) | Bilan de santé du serveur (services, ports, CrowdSec, mises à jour) |

### Automatisation, bots et vidéo
| Skill | Rôle |
|---|---|
| [`bot-telegram`](skills/bot-telegram) | Créer ou dépanner un bot Telegram (webhook Vercel ou service sur VPS) |
| [`envoyer-telegram`](skills/envoyer-telegram) | L'agent envoie lui-même les livrables sur Telegram |
| [`video-rgm`](skills/video-rgm) | Vidéos TikTok en HyperFrames + composants React + voix ElevenLabs |

### Relation client
| Skill | Rôle |
|---|---|
| [`devis-freelance`](skills/devis-freelance) | Chiffrer un devis ou une facture |
| [`message-client`](skills/message-client) | Rédiger un message client, au vouvoiement |
| [`retours-client`](skills/retours-client) | Transformer des retours en liste de tâches |
| [`signature-mail`](skills/signature-mail) | Signature HTML Gmail / Outlook |
| [`courrier-officiel`](skills/courrier-officiel) | Réclamation, résiliation, demande au support |

### Génie électrique et études (BUT GEII)
| Skill | Rôle |
|---|---|
| [`esp32-arduino`](skills/esp32-arduino) | Compiler et téléverser avec arduino-cli, capteurs, Wi-Fi |
| [`kicad-projet`](skills/kicad-projet) | ERC/DRC et dossier de fabrication JLCPCB |
| [`dimensionnement-pv`](skills/dimensionnement-pv) | Photovoltaïque : PVGIS, onduleur, câbles, rentabilité |
| [`blender-solaire`](skills/blender-solaire) | Modéliser une maison et poser les panneaux à l'échelle |
| [`rapport-tp`](skills/rapport-tp) | Comptes rendus de TP et rapports de SAÉ |
| [`fiche-revision`](skills/fiche-revision) | Fiches, méthodes et QCM à partir d'un cours |
| [`candidature-stage`](skills/candidature-stage) | Recherche d'entreprise, lettre, relance |

### Poste de travail
| Skill | Rôle |
|---|---|
| [`depannage-pc`](skills/depannage-pc) | Diagnostiquer un problème Windows |
| [`menage-disque`](skills/menage-disque) | Libérer de la place sans rien casser |

## Les skills des autres que j'utilise

Elles ne sont pas dans ce dépôt : elles appartiennent à leurs auteurs.

| Collection | Auteur | Pour quoi |
|---|---|---|
| HyperFrames (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) | HeyGen | Vidéos écrites en HTML, rendues en MP4 |
| [brag](https://github.com/latent-spaces/brag) | Latent Spaces | Vidéo de lancement tirée du code d'un projet |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | Leonxlnx | Directions de design, refontes, chartes |
| [Skills de Matt Pocock](https://github.com/mattpocock/skills) | Matt Pocock | Tests d'abord, diagnostic, revue, modélisation |
| [n8n skills](https://github.com/czlonkowski/n8n-skills) | Romuald Członkowski | Workflows n8n sans erreur d'expression ni de nœud |
| [Design engineering](https://github.com/emilkowalski/skills) | Emil Kowalski | Le détail des animations et des composants |
| [Better UI](https://github.com/jakubkrehel/skills) | Jakub Krehel | Rayons, alignement optique, profondeur |
| [Plugins officiels](https://github.com/anthropics/claude-plugins-official) | Anthropic | Sécurité, design, création de skills, documents |
| Figma (`figma-use`, `figma-design-to-code`…) | Figma | De la maquette au code |
| `transitions-dev`, `transitions-polish`, `design-motion-principles`, `motion-design` | transitions.dev et la communauté | Durées, courbes, audit des animations |
| `stripe-projects` | Stripe | Provisionner des services depuis le terminal |
| `bklit-ui` | Bklit | Graphiques des tableaux de bord |

## Installer

```bash
git clone https://github.com/glm02/skills-claude-code.git
cp -r skills-claude-code/skills/site-a-z ~/.claude/skills/   # une skill
cp -r skills-claude-code/skills/* ~/.claude/skills/          # toutes
```

| Agent | Dossier |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.agents/skills/` (ou `.agents/skills/` à la racine d'un dépôt) |
| Application Claude (claude.ai) | dossier de la skill compressé en zip, importé dans les paramètres, rubrique Skills |
| Hermes Agent | `~/.hermes/skills/<catégorie>/` |
| Autre agent | son dossier de skills, ou le contenu de `SKILL.md` dans ses instructions (`AGENTS.md`) |

Relancer l'agent : la skill se charge quand la tâche correspond, ou par son
nom (`/site-a-z` dans Claude Code). Sous Windows, `~` est `%USERPROFILE%`.
Tuto illustré : [rafaelgmille.site/stack#installer](https://www.rafaelgmille.site/stack#installer)
(aussi sur [rgm-dev.site/stack#installer](https://rgm-dev.site/stack#installer)).

Les scripts lisent
leurs clés dans `~/.secrets/` ou dans l'environnement : aucune n'est dans ce
dépôt. Les chemins (`~/Documents/GitHub/...`) sont ceux de mon poste, à
adapter.

Les logos de `video-rgm/logos` viennent de [Simple Icons](https://simpleicons.org)
(CC0) et restent la propriété de leurs marques.
