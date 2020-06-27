#!/usr/bin/python
import os
import gi
from bluetooth_tools import fix_device

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1") 
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

APP_ID = "e7b54343-ac80-49d7-ab71-f4921ebc33a0"
ICON_SOURCE = "system-run"
HEADPHONE_MAC_ADDRESS = "38:18:4C:49:2E:24"

def main():
  
  indicator = appindicator.Indicator.new(APP_ID, ICON_SOURCE,
    appindicator.IndicatorCategory.SYSTEM_SERVICES)
  
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(create_tray_menu())

  gtk.main()

def create_tray_menu():
  
  menu = gtk.Menu()

  fix_headphones_option = gtk.MenuItem(label="Fix Headphones")
  fix_headphones_option.connect("activate", fix_headphones_wrapper)
  menu.append(fix_headphones_option)
  
  quit_option = gtk.MenuItem(label="Quit")
  quit_option.connect("activate", gtk.main_quit)
  menu.append(quit_option)
  
  menu.show_all()
  return menu

def fix_headphones_wrapper(*args):
  fix_device(HEADPHONE_MAC_ADDRESS)

if __name__ == "__main__":
  main()