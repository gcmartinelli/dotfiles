#!/bin/sh
light-locker &			#Screen locker
compton -b &			#Compton (solve screen tearing issues)
urxvtd -q -f -o &		#URXVT daemon
