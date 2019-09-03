from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget
from libqtile import hook
import os
import socket
import subprocess
import json
import time
import pywal

mod = "mod4"

HOMEDIR = os.path.expanduser('~')

# Autostart hook
@hook.subscribe.startup_once
def autostart():
	home = os.path.expanduser('~/.config/qtile/autostart.sh')
	subprocess.call([home])

'''
### MONITORS
'''
os.system('mons --primary DP-1')
os.system('mons -e right')

'''
### COLORS
'''
def pallete_init():
	image = pywal.image.get(f"{HOMEDIR}/Pictures/wallpapers")
	colors = pywal.colors.get(image, sat=0.65)
	pywal.sequences.send(colors)
	pywal.export.every(colors)
	pywal.reload.env()
	pywal.wallpaper.change(image)
	clist = []
	for color in list(colors['colors'].values()):
		clist.append(color)
	return clist

colors = pallete_init()

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
	Key([mod, "shift"], "k", lazy.layout.grow()),
	Key([mod, "shift"], "j", lazy.layout.shrink()),
	Key([mod], "Up", lazy.layout.grow()),
	Key([mod], "Down", lazy.layout.shrink()),
	
	# Switch window focus to other pane(s) of stack
	Key([mod], "space", lazy.layout.next()),
	
	# Swap panes of split stack
	Key([mod, "shift"], "space", lazy.layout.rotate()),
	
	# Toggle between split and unsplit sides of stack.
	Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
	
	# Toggle between different layouts as defined below
	Key([mod], "Tab", lazy.next_layout()),
	Key([mod, "shift"], "Tab", lazy.prev_layout()),
	Key([mod], "c", lazy.window.kill()),
	
	Key([mod, "control"], "r", lazy.restart()),
	Key([mod, "control"], "q", lazy.shutdown()),
	Key([mod], "r", lazy.spawncmd()),
	Key([mod], "l",lazy.spawn("light-locker-command -l")),
	
	# Display control
	Key([mod, "control"], "Tab", lazy.spawn("mons -n left")),
	]
	
	
	# Program Shortcuts
keys.extend([
	Key([mod], "t", lazy.spawn(f"import {HOMEDIR}/Pictures/screenshots/{int(time.time())}.png")),
	Key([mod], "h", lazy.spawn("urxvtc -e htop")),
	Key([mod], "d", lazy.spawn("discord")),
	Key([mod], "f", lazy.spawn("firefox")),
	Key([mod, "shift"], "f", lazy.spawn("chromium")),
	Key([mod], "a", lazy.spawn("urxvtc -e alsamixer")),
	Key([mod], "Return", lazy.spawn("urxvt")),
	Key([mod], "e", lazy.spawn("urxvtc -e ranger %s" % (HOMEDIR))),
	])
	
	# Multimedia Keys
keys.extend([
	Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
	Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 10+")),
	Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 10-")),
	Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
	Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10"))
	])
	

'''
### LAYOUTS 
''' 

layout_theme = {"border_width": 1,
	"margin": 5,
	"single_margin": 5,
	"border_focus": colors[11],
	"border_normal": colors[1]}

layouts = [
	layout.Max(**layout_theme),
	layout.MonadTall(**layout_theme),
	layout.MonadWide(**layout_theme),
	layout.Columns(**layout_theme),
	#	layout.Matrix(**layout_theme,
	#					columns=3),	
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
		  {'name':"WWW", 'layout':'max'},
		{'name':"TOR", 'layout':'max', 'matches':[Match(wm_class=['disbord'])]},
		{'name':"ETC", 'layout':'columns'}]

groups = [Group(**kwargs) for kwargs in group_names]

for i, group in enumerate(groups, 1):
	keys.append(Key([mod], str(i), lazy.group[group.name].toscreen()))		#switch view to another group
	keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(group.name)))	#move window to another group


'''
### WIDGETS
'''

widget_defaults = dict(
	#font = "ShureTechMono Nerd Font",
	font = "UbuntuMono Nerd Font",
	fontsize = 15,
	padding = 2,
	background = colors[0],
	)

def init_widgets_list():
	prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
	widgets_list = [widget.Sep(linewidth=0, 
								padding=6, 
								foreground=colors[1], 
								background=colors[0]),
					widget.GroupBox(font='ShureTechMono Nerd Font',
								fontsize=12,
								margin_y=0,
								margin_x=0,
								padding_y=5,
								padding_x=10,
								borderwitdh=1,
								active=colors[1],
								inactive=colors[1],
								rounded=False,
								highlight_method='block',
								this_current_screen_border=colors[3],
								this_screen_border=colors[3],
								other_current_screen_border=colors[0],
								other_screen_border=colors[0],
								background=colors[0]),
					widget.Sep(linewidth=0,
								padding=6,
								foreground=colors[1],
								background=colors[0]),
					widget.Prompt(prompt=prompt,
								background=colors[4],
								foreground=colors[15]),
					widget.WindowName(foreground=colors[7]),
					widget.Systray(padding=9,
								icon_size=20),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.CPUGraph(graph_color=colors[5],
									border_color=colors[1],
									fill_color=colors[5],
									border_width=1),
					widget.MemoryGraph(graph_color=colors[3],
									border_color=colors[1],
									fill_color=colors[3],
									border_width=1),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.CurrentLayout(font="ShureTechMono Nerd Font"),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.Image(filename=HOMEDIR+"/Pictures/icons/whitepng/wifi.png", 
							background=colors[0]),
					widget.Sep(linewidth=0,
								padding=5,
								foreground=colors[1],
								background=colors[0]),
					widget.Wlan(interface='wlp58s0',
							font="ShureTechMono Nerd Font",
							format="{quality}/70"),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.Volume(theme_path=HOMEDIR+"/Pictures/icons/whitepng/volume",
								volume_app="amixer",
								mute_command="Master toggle",
								volume_down_command="set Master 2%-",
								volume_up_command="set Master 2%+"),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.BatteryIcon(theme_path=HOMEDIR+'/Pictures/icons/battery/',
									background=colors[0]),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.KeyboardLayout(configured_keyboards=['us', 'us alt-intl']),
					widget.Sep(linewidth=0,
								padding=20,
								foreground=colors[1],
								background=colors[0]),
					widget.Image(filename=HOMEDIR+"/Pictures/icons/whitepng/clock.png", 
								background=colors[0]),
					widget.Clock(format='%d-%b %a %H:%M'),
					widget.Sep(linewidth=0,
								padding=10,
								foreground=colors[1],
								background=colors[0]),]
	return widgets_list

def init_screens():
	return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=24)),
			Screen(top=bar.Bar(widgets=init_widgets_list(), size=24))]

screens = init_screens()

'''
### OTHER
'''

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False

auto_fullscreen = True
#focus_on_window_activation = "smart"

wmname = "qtile"
