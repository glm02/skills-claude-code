# Skills Claude Code — RGM Dev

Les 39 skills que j'ai écrites pour travailler avec des agents IA au quotidien :
livrer des sites, brancher des automatisations, sécuriser, et garder la main
sur ce que font les agents.

Rafael — développeur full-stack freelance à Lyon · [rgm-dev.site](https://rgm-dev.site) · [la page qui présente cette stack](https://rgm-dev.site/stack)

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

## Installer

Copier un dossier de `skills/` dans `~/.claude/skills/`. Les scripts lisent
leurs clés dans `~/.secrets/` ou dans l'environnement : aucune n'est dans ce
dépôt. Les chemins (`~/Documents/GitHub/...`) sont ceux de mon poste, à
adapter.

Les logos de `video-rgm/logos` viennent de [Simple Icons](https://simpleicons.org)
(CC0) et restent la propriété de leurs marques.
