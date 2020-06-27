#!/usr/bin/python
import os
import gi
from bluetooth_tools import fix_device
import log
import functools
import threading

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1") 
from gi.repository import Gtk, AppIndicator3, GLib

class QuickResolve():

  def __init__(self):

    self.APP_ID = "e7b54343-ac80-49d7-ab71-f4921ebc33a0"
    self.IDLE_ICON_SOURCE = "system-run"
    self.BUSY_ICON_SOURCE = "image-loading-symbolic"
    self.HEADPHONE_MAC_ADDRESS = "38:18:4C:49:2E:24"
    
    self.indicator = AppIndicator3.Indicator.new(self.APP_ID, self.IDLE_ICON_SOURCE,
      AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    
    self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    self.indicator.set_menu(self.init_menu())

  def init_menu(self):
  
    self.menu = Gtk.Menu()

    fix_headphones_option = Gtk.MenuItem(label="Fix Headphones")
    fix_headphones_option.connect("activate",
      functools.partial(self.run_script, self.fix_headphones_helper))
    self.menu.append(fix_headphones_option)
    
    quit_option = Gtk.MenuItem(label="Quit")
    quit_option.connect("activate", Gtk.main_quit)
    self.menu.append(quit_option)
    
    self.menu.show_all()
    return self.menu

  def run_script(self, script, *args):

    GLib.idle_add(self.indicator.set_icon_full, self.BUSY_ICON_SOURCE, "Running...")
    threading.Thread(target=script).start()

  def fix_headphones_helper(self):
    fix_device(self.HEADPHONE_MAC_ADDRESS)
    GLib.idle_add(self.indicator.set_icon_full, self.IDLE_ICON_SOURCE, "Quick Resolve")

if __name__ == "__main__":
  main_tray = QuickResolve()
  Gtk.main()