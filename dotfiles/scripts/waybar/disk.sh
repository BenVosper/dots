#!/usr/bin/env bash
# Waybar custom module: free space on /home, tooltip with /home and / details.

# df -h prints e.g. "471G"; add a B so it reads "471GB".
units() { sed -E 's/([KMGTP])\b/\1B/g'; }

line() {
    df -h --output=size,used,avail,pcent "$1" | tail -1 | {
        read -r size used avail pcent
        printf '%-6s %5s / %5s used (%4s)  %5s free' "$2" "$used" "$size" "$pcent" "$avail"
    } | units
}

home_free=$(df -h --output=avail /home | tail -1 | tr -d ' ' | units)
home_pct=$(df --output=pcent /home | tail -1 | tr -d ' %')
tooltip="<tt>$(line /home /home)\n$(line / /)</tt>"

class=normal
((home_pct >= 90)) && class=critical

printf '{"text": "%s", "tooltip": "%s", "class": "%s", "percentage": %d}\n' \
    "$home_free" "$tooltip" "$class" "$home_pct"
