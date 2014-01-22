#!/bin/bash
####
# add terminal over desktop wallpaper
#
# use xfce4-terminal & wmctrl
####

xfce4-terminal --hide-borders --hide-menubar --title=desktopconsole &
sleep 1
wmctrl -r desktopconsole -b add,below,sticky
wmctrl -r desktopconsole -b add,skip_taskbar,skip_pager
wmctrl -r desktopconsole -e 0,5,30,1000,900
