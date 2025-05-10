#!/bin/bash
#feh --bg-scale /home/galym/KorlanScreenshots/Screenshot_20250206_060737.png 
feh --bg-scale "/home/galym/KorlanScreenshots/scrot-2025-04-01-18:16_000.jpg"

/home/galym/bin/Telegram/Telegram &
~/bin/firefox/firefox-bin &
hp-systray &
copyq &
kbdd &
mpd &
heroic-run &
setxkbmap -layout "us,ru" -option "grp:alt_shift_toggle,grp_led:scroll"
xrdb ~/.config/qtile/Xresources
# ~/bin/pycharm.sh &
# cherrytree &
