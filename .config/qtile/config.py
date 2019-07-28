from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook
import os
import socket
import subprocess

from typing import List  # noqa: F401

mod = "mod4"

HOMEDIR = os.path.expanduser('~')

# Autostart hook
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


'''
### KEYS
'''

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),
    Key([mod], "Right", lazy.layout.shuffle_down()),
    Key([mod], "Left", lazy.layout.shuffle_up()),
        
    # Change size of focus window
    Key([mod], "Up", lazy.layout.grow()),
    Key([mod], "Down", lazy.layout.shrink()),
    
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "c", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "x",lazy.spawn("light-locker-command -l")),
]
    

# Program Shortcuts
keys.extend([
    Key([mod], "h", lazy.spawn("urxvtc -e htop")),
    Key([mod], "d", lazy.spawn("discord")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "a", lazy.spawn("urxvtc -e alsamixer")),
    Key([mod], "Return", lazy.spawn("urxvtc")),
    Key([mod], "e", lazy.spawn("urxvtc -e ranger %s" % (HOMEDIR))),
])


'''
### COLORS
'''

colors = [
    "1e1c2c", #top bar background
    "26d2bb", #top bar foreground
    "fcfcfc", #group active (leters)
    "fcfcfc", #group inactive (leters)
    "26d2bb", #search background
    "1e1c2c", #search foreground
    ]


'''
### LAYOUTS 
''' 

layout_theme = {"border_width": 1,
        "margin": 5,
        "single_margin": 5,
        "border_focus": colors[1],
        "border_normal": colors[0]}

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
	layout.Matrix(**layout_theme,
					columns=3),    
#    layout.Floating(float_rules=[
#        {'wmclass': 'confirm'},
#        {'wmclass': 'dialog'},
#        {'wmclass': 'download'},
#        {'wmclass': 'error'},
#        {'wmclass': 'file_progress'},
#        {'wmclass': 'notification'},
#        {'wmclass': 'splash'},
#        {'wmclass': 'toolbar'},
#        {'wmclass': 'confirmreset'},  # gitk
#        {'wmclass': 'makebranch'},  # gitk
#        {'wmclass': 'maketag'},  # gitk
#        {'wname': 'branchdialog'},  # gitk
#        {'wname': 'pinentry'},  # GPG key password entry
#        {'wmclass': 'ssh-askpass'},  # ssh-askpass
#        ])
    ]

# Drag control for floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


'''
### GROUPS
'''

group_names = [{'name':"DEV", 'layout':'monadtall'},
              {'name':"WWW", 'layout':'max', 'spawn':'firefox'},
	        {'name':"DISC", 'layout':'max', 'matches':[Match(wm_class=['discord'])]},
			{'name':"ETC", 'layout':'matrix'}]

groups = [Group(**kwargs) for kwargs in group_names]

for i, group in enumerate(groups, 1):
    keys.append(Key([mod], str(i), lazy.group[group.name].toscreen()))        #switch view to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(group.name)))    #move window to another group


'''
### WIDGETS
'''

widget_defaults = dict(
    font = 'iosevka',
    fontsize = 15,
    padding = 2,
    background = colors[0],
)

extension_defaults = widget_defaults.copy()

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
screens = [
    Screen( 
        top=bar.Bar(
            [
        widget.Sep(linewidth = 0,
            padding = 6,
            foreground = colors[1],
            background = colors[0]),
        widget.GroupBox(font='Ubuntu Mono Bold',
            fontsize = 10,
            margin_y = 0,
            margin_x = 0,
            padding_y = 7,
            padding_x = 10,
            borderwitdh = 1,
            active = colors[2],
            inactive = colors[3],
            rounded = False,
            highlight_method = 'block',
            this_current_screen_border = colors[1],
            this_screen_border = colors[3],
            other_current_screen_border = colors[1],
            other_screen_border = colors[3],
            background = colors[0]),
        widget.Sep(linewidth = 0,
            padding = 6,
            foreground = colors[1],
            background = colors[0]),
        widget.Prompt(prompt=prompt,
            background = colors[4],
            foreground = colors[5]),
        widget.WindowName(foreground = colors[1]),
        widget.Systray(padding = 9,
						icon_size = 20),
		widget.Sep(linewidth = 0,
					padding = 20,
					foreground = colors[1],
					background = colors[0]),
        widget.Volume(volume_app="urxvtc -e amixer",
            mute_command="Master toggle",
            volume_down_command="set Master 2%-",
            volume_up_command="set Master 2%+"),
        widget.TextBox(text=" ⌚"),
        widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24)),
]

'''
### OTHER
'''

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "qtile"
