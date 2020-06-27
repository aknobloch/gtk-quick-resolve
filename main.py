#!/usr/bin/python
import os
from bluetooth_tools import fix_device
import log
import functools
from script_runner import ScriptRunner
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1") 
from gi.repository import Gtk, AppIndicator3

IDLE_ICON_SOURCE = "system-run"
BUSY_ICON_SOURCE = "image-loading-symbolic"
HEADPHONE_MAC_ADDRESS = "38:18:4C:49:2E:24"

class QuickResolve():

  def __init__(self):

    self.APP_ID = "e7b54343-ac80-49d7-ab71-f4921ebc33a0"
    
    self.indicator = AppIndicator3.Indicator.new(self.APP_ID, IDLE_ICON_SOURCE,
      AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    
    self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    self.indicator.set_menu(self.init_menu())

  def init_menu(self):
  
    self.menu = Gtk.Menu()

    headphones_menu = self.create_headphones_menu()
    self.menu.append(headphones_menu)
    
    quit_option = Gtk.MenuItem(label="Quit")
    quit_option.connect("activate", Gtk.main_quit)
    self.menu.append(quit_option)
    
    self.menu.show_all()
    return self.menu

  def create_headphones_menu(self):

    fix_headphones_option = Gtk.MenuItem(label="Fix Headphones")

    fix_headphones_runner = ScriptRunner(self.indicator,
      BUSY_ICON_SOURCE, IDLE_ICON_SOURCE,
      functools.partial(fix_device, HEADPHONE_MAC_ADDRESS))
    fix_headphones_option.connect("activate", fix_headphones_runner.run)
    
    return fix_headphones_option

if __name__ == "__main__":
  main_tray = QuickResolve()
  Gtk.main()