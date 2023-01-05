#!/usr/bin/env python3

import signal
import subprocess

from PySide6.QtGui import QIcon, QAction, QActionGroup
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

# target should be either '-p' for performance or '-b' for battery
def set_mode(target: str, mode: str):
    try:
        subprocess.run(['ideapad-perf', target, mode])
    except subprocess.CalledProcessError:
        pass

# flag should either be '-spc' for performance or '-sbc' for battery
def update_action(action_map: dict[str, QAction], flag: str):
    try:
        mode = subprocess.check_output(['ideapad-perf', flag]).decode('ascii').strip()
        if not mode in action_map:
            return # yikes
        action_map[mode].setChecked(True)
    except subprocess.CalledProcessError:
        pass

def update(perf_action: dict[str, QAction], bat_action: dict[str, QAction]):
    update_action(perf_action, '-spc')
    update_action(bat_action, '-sbc')


app = QApplication([])
app.setQuitOnLastWindowClosed(False)
icon = QIcon.fromTheme("preferences-system-power")
#icon = QIcon.fromTheme("gnome-power-manager-symbolic")
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setToolTip("Performance Menu")

# Create the menu
menu = QMenu()
menu.mouseReleaseEvent

# Create performance actions
perf_mode = QAction("Performance Mode")
perf_mode.setDisabled(True)
perf_per = QAction("Extreme Performance")
perf_bat = QAction("Battery Saving")
perf_int = QAction("Intelligent Cooling")
perf_per.triggered.connect(lambda _: set_mode('-p', 'ep'))
perf_bat.triggered.connect(lambda _: set_mode('-p', 'bs'))
perf_int.triggered.connect(lambda _: set_mode('-p', 'ic'))

# Create action group for performance
perf_group = QActionGroup(menu)
perf_per.setActionGroup(perf_group)
perf_bat.setActionGroup(perf_group)
perf_int.setActionGroup(perf_group)
perf_per.setCheckable(True)
perf_bat.setCheckable(True)
perf_int.setCheckable(True)

# Create battery actions
bat_mode = QAction("Battery Mode")
bat_mode.setDisabled(True)
bat_rap = QAction("Rapid Charge")
bat_con = QAction("Battery Conservation")
bat_non = QAction("Off")
bat_rap.triggered.connect(lambda _: set_mode('-b', 'rc'))
bat_con.triggered.connect(lambda _: set_mode('-b', 'bc'))
bat_non.triggered.connect(lambda _: set_mode('-b', 'off'))

# Create action group for battery
bat_group = QActionGroup(menu)
bat_rap.setActionGroup(bat_group)
bat_con.setActionGroup(bat_group)
bat_non.setActionGroup(bat_group)
bat_rap.setCheckable(True)
bat_con.setCheckable(True)
bat_non.setCheckable(True)

# Create action to exit
quit = QAction("Exit")
quit.triggered.connect(app.quit)

# Populate menu
menu.addAction(perf_mode)
menu.addActions(perf_group.actions())
menu.addSeparator()
menu.addAction(bat_mode)
menu.addActions(bat_group.actions())
menu.addSeparator()
menu.addAction(quit)

# Create action maps
perf_action = {"Extreme Performance": perf_per, "Battery Saving": perf_bat, "Intelligent Cooling": perf_int}
bat_action = {"Rapid Charge": bat_rap, "Battery Conservation": bat_con, "Off": bat_non}
#check_all(perf_action, bat_action)

# Update menu items to show current state when the menu is opened 
menu.aboutToShow.connect(lambda: update(perf_action, bat_action))

# Set trays contex menu and make visible
tray.setContextMenu(menu)
tray.setToolTip("Batery and Performance")
tray.setVisible(True)


# Exit on SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal.SIG_DFL)


app.exec()
