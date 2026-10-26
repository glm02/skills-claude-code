#!/usr/bin/env bash
# Bilan de santé du VPS Contabo, en lecture seule.
#   ssh contabo-vps 'bash -s' < ~/.claude/skills/vps-sante/bilan.sh
# Chaque ligne commence par OK, ATTENTION ou ALERTE pour se lire d'un coup d'œil.
# N'affiche aucun secret : noms de services, chiffres et codes seulement.

ok()  { echo "OK        $*"; }
att() { echo "ATTENTION $*"; }
al()  { echo "ALERTE    $*"; }

echo "== Système ($(hostname), $(date '+%F %H:%M %Z'))"
echo "          en marche depuis $(uptime -p | sed 's/up //'), charge $(cut -d' ' -f1-3 /proc/loadavg)"
[ -f /var/run/reboot-required ] && att "redémarrage requis (noyau ou libc mis à jour)" || ok "pas de redémarrage requis"

disque=$(df --output=pcent / | tail -1 | tr -dc '0-9')
if [ "$disque" -ge 90 ]; then al "disque / à ${disque}%"; elif [ "$disque" -ge 80 ]; then att "disque / à ${disque}%"; else ok "disque / à ${disque}%"; fi
mem=$(free | awk '/Mem:/ {printf "%d", ($2-$7)*100/$2}')
[ "$mem" -ge 90 ] && att "mémoire utilisée ${mem}%" || ok "mémoire utilisée ${mem}%"

echo "== Services"
for s in caddy hermes-gateway hermes-dashboard hermes-webui hermes-webui-atout atelier-video atout-sms crowdsec crowdsec-firewall-bouncer fail2ban docker docker-firewall-rules; do
  systemctl list-unit-files "$s.service" >/dev/null 2>&1 || continue
  etat=$(systemctl is-active "$s" 2>/dev/null)
  case "$etat" in active) ok "$s";; inactive) [ "$(systemctl is-enabled "$s" 2>/dev/null)" = enabled ] && al "$s arrêté alors qu'il est activé" || echo "          $s inactif (non activé)";; *) al "$s : $etat";; esac
done
echecs=$(systemctl --failed --no-legend --plain | awk '{print $1}' | tr '\n' ' ')
[ -n "$echecs" ] && al "unités en échec : $echecs" || ok "aucune unité systemd en échec"

echo "== Conteneurs"
if command -v docker >/dev/null; then
  docker ps -a --format '{{.Names}}|{{.Status}}' | while IFS='|' read -r n st; do
    case "$st" in Up*unhealthy*) al "$n : $st";; Up*) ok "$n : $st";; *) att "$n : $st";; esac
  done
fi

echo "== Exposition (ports ouverts hors 127.0.0.1)"
ss -tlnH | awk '{print $4}' | grep -vE '^(127\.|\[::1\]|::1)' | sed 's/.*://' | sort -un | tr '\n' ' ' | sed 's/^/          ports : /'; echo
# Docker publie en amont d'UFW : un port publié en 0.0.0.0 est joignable même si UFW le refuse.
docker ps --format '{{.Names}} {{.Ports}}' 2>/dev/null | grep -E '0\.0\.0\.0:|:::' | while read -r l; do att "port Docker public : $l"; done

echo "== Mises à jour"
maj=$(apt list --upgradable 2>/dev/null | grep -c security)
[ "$maj" -gt 0 ] && att "$maj paquet(s) de sécurité à mettre à jour" || ok "pas de mise à jour de sécurité en attente"

echo "== Sécurité"
command -v cscli >/dev/null && echo "          CrowdSec : $(cscli decisions list -o raw 2>/dev/null | tail -n +2 | wc -l) IP bloquées"
ssh_pw=$(sshd -T 2>/dev/null | awk '/^passwordauthentication/ {print $2}')
[ "$ssh_pw" = "no" ] && ok "SSH par mot de passe désactivé" || al "SSH par mot de passe : $ssh_pw"

echo "== Journaux (24 h)"
for s in hermes-gateway caddy; do
  n=$(journalctl -u "$s" --since "24 hours ago" -p err --no-pager -q 2>/dev/null | wc -l)
  [ "$n" -gt 20 ] && att "$s : $n lignes d'erreur" || ok "$s : $n lignes d'erreur"
done
