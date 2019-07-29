### Some of the tweaks I had to make to the XPS 13 (9350) to run Arch

* Enabled touchpad 'tapping' using an Xorg config file (below)
* Used `xev | awk -F'[ )]+' '/^KeyPress/ { a[NR+2] } NR in a { printf "%-3s %s\n", $5, $8 }'` to track multimedia keys that were not working
* Had to install `xf86-input-libinput`
* Used `xmodmap` and `.xmodmap` to map those missing commands (mainly audio controls)
* Running `dhcpcd.service` and `wpa_supplicant@interfacename.service` as network managers for WiFi
..* Had to create a custom service item to enable my wifi card during boot (associated to a [Kernel bug](http://bugzilla.kernel.org/show_bug.cgi?id=201853))

##### Custom systemctl service
```
[Unit]
Description=Disable Wifi Power Management
After=suspend.target

[Service]
Type=simple
ExecStartPre= /bin/sleep 10
ExecStart= /usr/bin/iw dev wlp3s0 set power_save off

[Install]
WantedBy=suspend.target
```

##### Xorg config for keypad 'tapping' (saved at `/etc/X11/xorg.conf.d/`)
```
Section "InputClass"
    Identifier "touchpad"
    Driver "libinput"
    MatchIsTouchpad "on"
    Option "Tapping" "on"
EndSection
```

