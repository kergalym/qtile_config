#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import stat
import subprocess
from libqtile.config import Key, Screen, Drag, Click
from libqtile.config import Group, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook
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
    Group("DEV " + u"\u2713", matches=[Match(wm_class=["urxvt"]),
                                       Match(wm_class=["PyCharm"])]),
    Group("MEDIA " + u"\u266B", matches=[Match(wm_class=["ncmpcpp"]),
                                         Match(wm_class=["mpv"]),
                                         Match(wm_class=["urxvt"])]),
    Group("GRAPHICS " + u"\U0001F58C", matches=[Match(wm_class=["feh"]),
                                                Match(wm_class=["mupdf"]),
                                                Match(wm_class=["GNU Image \
                                                                Manipulation \
                                                                Program"]),
                                                Match(wm_class=["Krita"])]),
    Group("3D " + u"\U0001F4BB", matches=[Match(wm_class=["Blender"])]),
    Group("TORRENTS " + u"\U0001F572", matches=[Match(wm_class=["rtorrent"]),
                                                Match(wm_class=["Ktorrent"])]),
    Group("GAMES " + u"\U0001F3AE", matches=[Match(wm_class=["wine"])]),
    Group("TALKING " + u"\U0001F4AC", matches=[Match(wm_class=["HexChat"]),
                                               Match(wm_class=["Skype"])]),
    Group("WEB " + u"\U0001F578", matches=[Match(wm_class=["Chromium"]),
                                           Match(wm_class=["Firefox"]),
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


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(background='#000000',
                                foreground='#ffffff',
                                active='#ffffff',
                                this_current_screen_border="#470000",
                                borderwidth=1,
                                highlight_method='block',
                                font='Open Sans',
                                fontsize=12),
                widget.WindowName(foreground='#ffffff'),
                widget.Net(background='#470000', foreground='#ffffff',
                           interface='eth0'),
                widget.TextBox(u"\U0001F5AE", foreground='#ffffff',
                               font='Open Sans'),
                widget.KeyboardKbdd(configured_keyboards=['us', 'ru', 'kz'],
                                    update_interval=1,
                                    background='#470000'),
                widget.TextBox(u"\U0001F50A", foreground='#ffffff',
                               font='Open Sans'),
                widget.Volume(foreground='#ffffff'),

                widget.Systray(),
                widget.Clock(foreground='#ffffff',
                             format='%A, %d.%m.%Y, %H:%M %p'),
            ],
            24,
        ),
        bottom=bar.Bar(
            [
                widget.Prompt(),
                widget.Spacer(),

                widget.TextBox("ROOT SPACE:", foreground='#ffffff'),
                widget.HDDGraph(background='#000000', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#470000",
                                path="/"),
                widget.TextBox("ST3 SPACE:", foreground='#ffffff'),
                widget.HDDGraph(background='#000000', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#470000",
                                path="/media/ST3"),
                widget.TextBox("WDBL SPACE:", foreground='#ffffff'),
                widget.HDDGraph(background='#000000', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#470000",
                                path="/media/WDBL"),
                widget.TextBox("WDBL2 SPACE:", foreground='#ffffff'),
                widget.HDDGraph(background='#000000', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#470000",
                                path="/media/WDBL2"),

                widget.TextBox("i7 3770:", foreground='#ffffff'),
                widget.ChThermalSensor(chip='coretemp-isa-0000',
                                       background='#470000',
                                       foreground='#ffffff'),

                widget.TextBox("GTX 1050 Ti:", foreground='#ffffff'),
                widget.GenPollText(func=get_my_gpu_temp, update_interval=1,
                                   background='#470000',
                                   foreground='#ffffff'),
                widget.TextBox("SSD:", foreground='#ffffff'),
                widget.HDThermalSensor(drive_name='/dev/sda',
                                       background='#470000',
                                       foreground='#ffffff'),
                widget.TextBox("HD0:", foreground='#ffffff'),
                widget.HDThermalSensor(drive_name='/dev/sdb',
                                       background='#470000',
                                       foreground='#ffffff'),
                widget.TextBox("HD1:", foreground='#ffffff'),
                widget.HDThermalSensor(drive_name='/dev/sdc',
                                       background='#470000',
                                       foreground='#ffffff'),

                widget.TextBox("CPU USAGE:", foreground='#ffffff'),
                widget.CPUGraph(background='#000000', foreground='#000000',
                                core='all', border_color="#470000",
                                fill_color="#470000"),
                widget.TextBox("MEM USAGE:", foreground='#ffffff'),
                widget.MemoryGraph(background='#000000', foreground='#000000',
                                   type='box', border_color="#470000",
                                   fill_color="#470000"),
                widget.TextBox("HD IO:", foreground='#ffffff'),
                widget.HDDBusyGraph(background='#000000', foreground='#000000',
                                    fill_color="#470000"),
                widget.TextBox("NET USAGE:", foreground='#ffffff'),
                widget.NetGraph(background='#000000', foreground='#000000',
                                fill_color="#470000"),
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
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

groups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
], border_focus='#ffd700', border_normal='#881111')


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
focus_on_window_activation = "urgent"

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
