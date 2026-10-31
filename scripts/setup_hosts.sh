#!/usr/bin/env bash
# Write the pi-cluster hostname map on this node.
#
#   sudo bash setup_hosts.sh
#
# Edit the BLOCK below to match your network first; it must be identical on every node.
#
# What it does:
#   - replaces any previous "# pi-cluster network" block with BLOCK
#   - removes the "127.0.1.1 <hostname>" line, which would make Hadoop listen
#     on loopback only, so other nodes couldn't reach it
#   - updates /etc/hosts AND, when present, cloud-init's hosts template.
#     Current Raspberry Pi OS (cloud-init with manage_etc_hosts: true)
#     rebuilds /etc/hosts from that template on every boot, so editing
#     /etc/hosts alone would be undone by the next reboot.
# Running it again is safe. The first run keeps a .bak copy of each file.
set -euo pipefail

BLOCK='# pi-cluster network
192.168.0.100    master
192.168.0.101    worker1
192.168.0.102    worker2
192.168.0.103    worker3
192.168.0.104    worker4
# end pi-cluster network'

FILES=(/etc/hosts)
for template in /etc/cloud/templates/hosts.debian.tmpl /etc/cloud/templates/hosts.tmpl; do
  [[ -f "$template" ]] && FILES+=("$template")
done

if [[ $EUID -ne 0 ]]; then
  echo "run with sudo: sudo bash $0" >&2
  exit 1
fi

for file in "${FILES[@]}"; do
  [[ -f "$file.bak" ]] || cp -p "$file" "$file.bak"
  # drop the old block and any 127.0.1.1 line, keep everything else
  # ($(...) also trims trailing blank lines, so repeated runs don't add any)
  kept="$(awk '/^# pi-cluster network/{skip=1} !skip && !/^127\.0\.1\.1[[:space:]]/ {print} /^# end pi-cluster network/{skip=0}' "$file")"
  printf '%s\n\n%s\n' "$kept" "$BLOCK" > "$file"
  echo "updated $file"
done

me="$(hostname)"
if getent hosts "$me" | grep -qv '^127\.'; then
  echo "ok: $me resolves to $(getent hosts "$me" | awk '{print $1}')"
else
  echo "warning: $me is not in the block above; check the hostname and the BLOCK" >&2
fi
