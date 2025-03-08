#!/bin/bash
feh --bg-scale /media/FASTBIG2/qtile_config/walls/korlan_poster.png

parcellite &
kbdd &
mpd &
setxkbmap -layout "us,ru,kz" -option "grp:alt_shift_toggle,grp_led:scroll"
xrdb ~/.config/qtile/Xresources
