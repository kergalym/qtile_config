#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import stat
import subprocess
from libqtile.config import Key, Screen, Drag, Click
from libqtile.config import Group, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget
from libqtile import hook
import re
from re import sub

######################################################
#
#            KEY DEFINITIONS
#
######################################################
mod = "mod4"

keys = [
    Key([mod], "z", lazy.spawn("morc_menu")),
    Key([mod], "x", lazy.spawn("rofi -combi-modi drun -show combi")),
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # Grow windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),

    # Normalize windows
    Key([mod], "n", lazy.layout.normalize()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("urxvt")),
    Key([mod], "d", lazy.spawn("rofi -combi-modi window,drun,ssh -show combi -show-icons")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # Qtile system keys
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # Key([], 'Print', lazy.spawn(commands.screenshot)),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("ncmpcpp play")),
    Key([], "XF86AudioPlay", lazy.spawn("ncmpcpp pause")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer -c 0 sset Master 1+ unmute"))
]

######################################################
#
#            LAYOUT GROUPS DEFINITIONS
#
######################################################

groups = [
    Group("DEV " + u"\u2713", matches=[Match(wm_class=["Code"]),
                                       Match(wm_class=["PyCharm"])]),
    Group("MEDIA " + u"\u266B", matches=[Match(wm_class=["ncmpcpp"]),
                                         Match(wm_class=["mpv"])]),
    Group("GRAPHICS " + u"\U0001F58C", matches=[Match(wm_class=["Blender"]),
                                                Match(wm_class=["Krita"])]),
    Group("GAMEDEV " + u"\U0001F4BB", matches=[Match(wm_class=["UE4Editor"])]),
    Group("TORRENTS " + u"\U0001F572", matches=[Match(wm_class=["rtorrent"]),
                                                Match(wm_class=["Ktorrent"])]),
    Group("GAMES " + u"\U0001F3AE", matches=[Match(wm_class=["heroic"])]),
    Group("TALKING " + u"\U0001F4AC", matches=[Match(wm_class=["Telegram"]),
                                               Match(wm_class=["Skype"])]),
    Group("WEB " + u"\U0001F578", matches=[Match(wm_class=["Chromium"]),
                                           Match(wm_class=["Opera"])]),
    Group("OFFICE " + u"\U0001F3E2", matches=[Match(wm_class=["LibreOffice"])]),
]


grplist = []
# Make group list with respective integers
for i in range(len(groups)):
    grplist.append(i)

# Start the integer from one to bind it later
grplist.remove(0)
grplist.append(len(grplist)+1)

# Iterate and bind index as key
for k, v in zip(grplist, groups):
    keys.extend([
        # mod1 + letter of group = switch to grouplazy.group[j].toscreen()
        Key([mod], str(k), lazy.group[v.name].toscreen()),

        # mod1 + shift + letter of group = switch to
        # & move focused window to group
        Key([mod, "shift"], str(k), lazy.window.togroup(v.name)),
    ])

######################################################
#
#            LAYOUT DEFINITIONS
#
######################################################
layouts = [
    layout.Columns(border_focus='#ffd700',
                   border_normal='#881111'),
    layout.Stack(num_stacks=2)
]

######################################################
#
#            WIDGET DEFAULTS
#
######################################################
widget_defaults = dict(
    font='open sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

######################################################
#
#            SCREEN DEFINITIONS
#
######################################################


def get_my_gpu_temp():
    if os.path.isfile("/opt/bin/nvidia-smi"):
        data = subprocess.Popen(["/opt/bin/nvidia-smi",
                                 "--query-gpu=temperature.gpu",
                                 "--format=csv"],
                                stdout=subprocess.PIPE).communicate()
        return "{} °C".format(sub("\D", "", str(data)))

def get_my_gpu_mem():
    if os.path.isfile("/opt/bin/nvidia-smi"):
        data_used = subprocess.Popen(["/opt/bin/nvidia-smi",
                                 "--query-gpu=memory.used",
                                 "--format=csv,noheader,nounits"],
                                stdout=subprocess.PIPE).communicate()
        data_total = subprocess.Popen(["/opt/bin/nvidia-smi",
                                 "--query-gpu=memory.total",
                                 "--format=csv,noheader,nounits"],
                                stdout=subprocess.PIPE).communicate()
        stripped_data_used = ''
        stripped_data_total = ''
        for x, y in zip(data_used, data_total):
            if x is not None:
                stripped_data_used = x.decode("utf-8")
            if y is not None:
                stripped_data_total = y.decode("utf-8")
        used = int(stripped_data_used)  # Convert to integers
        total = int(stripped_data_total)  # Convert to integers
        used_gb = used // 1024  # Convert MiB to GB
        total_gb = total // 1024  # Convert MiB to GB
        return "{0}G/{1}G".format(used_gb, total_gb)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(background='#000000',
                                foreground='#ffffff',
                                active='#ffffff',
                                this_current_screen_border="#2d2d86",
                                borderwidth=1,
                                highlight_method='block',
                                font='Open Sans',
                                fontsize=12),
                widget.TaskList(),
                widget.Net(background='#470000', foreground='#ffffff',
                           interface='eth0'),
                widget.TextBox(u"\U0001F5AE", foreground='#ffffff', background="#801a00",
                               font='Open Sans'),
                widget.KeyboardKbdd(configured_keyboards=['us', 'ru', 'kz'],
                                    update_interval=1,
                                    background="#801a00"),
                widget.TextBox(u"\U0001F50A", foreground='#ffffff', background="#997a00",
                               font='Open Sans'),
                widget.Volume(foreground='#ffffff', background="#997a00"),

                widget.Systray(foreground="#ffffff", background='#4c0080'),
                widget.Clock(foreground='#ffffff',
                             background="#1f7a7a",
                             format='%A, %d.%m.%Y, %H:%M %p'),
            ],
            24,
        ),
        bottom=bar.Bar(
            [
                widget.Prompt(),
                widget.Spacer(),

                widget.TextBox("ROOT SPACE:", foreground='#ffffff', 
                               background="#2d2d86"),
                widget.HDDGraph(background='#2d2d86', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#0099ff",
                                path="/"),
                widget.TextBox("SSD SPACE:", foreground='#ffffff', 
                               background="#2d2d86"),
                widget.HDDGraph(background='#2d2d86', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#0099ff",
                                path="/media/FASTBIG"),
                widget.TextBox("SSD 2 SPACE:", foreground='#ffffff', 
                               background="#2d2d86"),
                widget.HDDGraph(background='#2d2d86', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#0099ff",
                                path="/media/FASTBIG2"),
                widget.TextBox("SSD 4 SPACE:", foreground='#ffffff', background="#2d2d86"),
                widget.HDDGraph(background='#2d2d86', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#0099ff",
                                path="/media/FASTKING"),

                widget.TextBox("i5-10400F:", foreground='#ffffff', 
                               background="#0000b3"),
                widget.ThermalSensor(tag_sensor='Core 0',
                                     background='#0000b3',
                                     foreground='#ffffff'),

                widget.TextBox("RTX 3060:", foreground='#ffffff', 
                               background="#00802b"),
                widget.GenPollText(func=get_my_gpu_temp, update_interval=1,
                                   background='#00802b',
                                   foreground='#ffffff'),

                widget.TextBox("CPU USAGE:", foreground='#ffffff', 
                               background="#801a00"),
                widget.CPU(background='#801a00', foreground='#ffffff', 
                           format="{load_percent}%"),
                widget.TextBox("RAM USAGE:", foreground='#ffffff', 
                               background="#006bb3"),
                widget.Memory(background='#006bb3', foreground='#ffffff',
                             measure_mem='G'),
                widget.TextBox("VRAM USAGE:", foreground='#ffffff', 
                               background="#4c0080"),
                widget.GenPollText(func=get_my_gpu_mem, update_interval=1,
                                   background='#4c0080',
                                   foreground='#ffffff'),
                widget.TextBox("SSD IO:", foreground='#ffffff', background="#1f7a7a"),
                widget.HDD(background='#1f7a7a', foreground='#ffffff', 
                           format="{HDDPercent}%"),
                widget.TextBox("NET USAGE:", foreground='#ffffff', background="#997a00"),
                widget.Net(background='#997a00', foreground='#ffffff'),
            ],
            24,
        ),
    ),
]

######################################################
#
#            MOUSE DRAG DEFINITIONS
#
######################################################
# Drag floating layouts.
mouse = [
   Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
   Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
   Click([mod], "Button2", lazy.window.bring_to_front()),
]
    
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="code"),
        Match(wm_class="UE4Editor"),
        Match(wm_class="heroic"),
        Match(wm_class="PyCharm")
    ]
)


######################################################
#
#            HOOKS & AUTOSTART DEFINITIONS
#
######################################################
@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True

    if window.match(wm_class="UE4Editor"):
        window.floating = True
    if window.match(wm_class="Code"):
        window.floating = True
    if window.match(wm_class="PyCharm"):
        window.floating = True

@hook.subscribe.startup_once
def autostart():
    auto = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([auto])


######################################################
#
#            WINDOW BEHAVIOR DEFINITIONS
#
######################################################
# urgent: urgent flag is set for the window
# focus: automatically focus the window
# smart: automatically focus if the window is in the current group

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

######################################################
#
#            WM NAME DEFINITION
#
######################################################
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
