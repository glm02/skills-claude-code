---
name: depannage-pc
description: Diagnostiquer et réparer un problème du PC Windows de Rafaël — application qui ne s'installe pas ou a cassé après une mise à jour, fichier « supprimé » au téléchargement, écran noir ou gel, lenteur, disque plein, ménage. À utiliser pour « j'ai un problème sur mon PC », « ça bugue depuis la mise à jour », « j'ai plus de place », ou une capture d'erreur Windows.
---

# Dépannage du PC

Windows 11, PowerShell 5.1 et Git Bash. Antivirus : **Avast** actif en plus de
Defender (Defender passe alors en mode passif). Suivi des écrans noirs :
mémoire `pc-ecrans-noirs-intel-arc.md` et `Desktop\suivi-bugs-pc`.

## Étapes

1. **Faits avant hypothèses** — selon le symptôme :
   - *installation* : journaux de l'installeur (Squirrel :
     `%LOCALAPPDATA%\SquirrelTemp\*.log` et `<app>\*.log` ; MSI :
     `msiexec /l*v`), entrée de désinstallation dans le registre
     (`HKCU/HKLM\…\Uninstall`), dossiers d'installation (`%LOCALAPPDATA%`,
     `%ProgramData%\<user>`), processus encore ouverts ;
   - *fichier qui disparaît* : quarantaine Avast
     (`C:\ProgramData\Avast Software\Avast\log\autosandbox.log`,
     `…\chest\index.xml`) puis Defender (`Get-MpThreatDetection`) ;
   - *gel, écran noir, plantage* : `Get-WinEvent` sur System et Application
     (Kernel-Power 41, LiveKernelEvent, Display, WHEA), pilote graphique,
     `powercfg /sleepstudy` ;
   - *place disque* : taille par dossier de premier niveau, puis les gros
     consommateurs connus (Autodesk, caches npm/pip, `ms-playwright`, Docker,
     anciens SDK, Téléchargements).
2. **Cause** : une phrase, appuyée sur une ligne de journal ou un test.
3. **Réparer**, en gardant une sauvegarde : renommer plutôt que supprimer
   (`<dossier>.casse-AAAAMMJJ`), exporter une clé de registre avant de la
   retirer, copier les données utilisateur (`%APPDATA%\<app>`) avant toute
   réinstallation. Installeur : le télécharger depuis la source officielle,
   vérifier la signature (`Get-AuthenticodeSignature`) et le lancer **une
   seule fois**, sans droits administrateur sauf nécessité.
4. **Vérifier** que le symptôme a disparu (l'appli démarre et retrouve le
   compte, l'espace est libéré, plus d'événement après redémarrage).
5. Ménage final : supprimer les dossiers mis de côté une fois la réparation
   confirmée par Rafaël.

Fini quand l'étape 4 est prouvée ou que le blocage restant dépend d'une
action de Rafaël, décrite clic par clic.

## Pièges connus

- Avast bloque tout seul les exécutables récents (CyberCapture / Sandbox) et
  retient le **nom exact** du fichier mis en quarantaine ; mes scripts ne
  peuvent pas changer ses réglages. Rafaël : Protection → Zone de quarantaine
  → « Restaurer et ajouter une exception », ou Avast désactivé 10 minutes.
- Un installeur lancé plusieurs fois en parallèle casse son propre dossier.
- Dans le bac à sable de Claude Code, un installeur peut sortir en code 0
  sans rien faire : relancer hors bac à sable.
- Suppression de données (AppData orphelins, dossiers d'applis) : lister
  avec les tailles et faire valider avant.
