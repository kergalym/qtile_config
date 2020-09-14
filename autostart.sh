#!/bin/bash
feh --bg-scale /home/galym/.config/qtile/walls/korlan_poster.png  

telegram &
skypeforlinux &
hexchat &
parcellite &
kbdd &
mpd &
setxkbmap -layout "us,ru" -option "grp:alt_shift_toggle,grp_led:scroll"
xrdb ~/.Xresources

