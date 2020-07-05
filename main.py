#!/usr/bin/python
import os
import bluetooth_tools
import log
import functools
from script_runner import ScriptRunner
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1") 
from gi.repository import Gtk, AppIndicator3, GLib

HEADPHONE_MAC_ADDRESS = "38:18:4C:49:2E:24"
BLUETOOTH_SCAN_TIME_SECONDS = 5

class QuickResolve():

  def __init__(self):

    self.APP_ID = "e7b54343-ac80-49d7-ab71-f4921ebc33a0"
    self.IDLE_ICON_SOURCE = "system-run"
    self.BUSY_ICON_SOURCE = "content-loading-symbolic"
    self.running_scripts = set()
    
    self.indicator = AppIndicator3.Indicator.new(self.APP_ID, self.IDLE_ICON_SOURCE,
      AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    
    self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    self.indicator.set_menu(self.init_menu())

  def init_menu(self):
  
    self.menu = Gtk.Menu()

    fix_headphones_option = Gtk.MenuItem(label="Fix Headphones")
    fix_headphones_script = functools.partial(bluetooth_tools.fix_device,
      HEADPHONE_MAC_ADDRESS, BLUETOOTH_SCAN_TIME_SECONDS)
    fix_headphones_option.connect("activate", 
      functools.partial(self.bootstrap_script, fix_headphones_script))
    self.menu.append(fix_headphones_option)
    
    kill_runners_option = Gtk.MenuItem(label="Kill Runners")
    kill_runners_option.connect("activate", self.kill_all_runners)
    self.menu.append(kill_runners_option)
    
    quit_option = Gtk.MenuItem(label="Quit")
    quit_option.connect("activate", Gtk.main_quit)
    self.menu.append(quit_option)
    
    self.menu.show_all()
    return self.menu

  def bootstrap_script(self, script, *gtk_args):

    self.set_busy_icon()
    script_runner = ScriptRunner(script, self.script_finished_listener)
    self.running_scripts.add(script_runner)
    script_runner.run()

  def script_finished_listener(self, runner):

    self.running_scripts.remove(runner)
    count_of_running_scripts = len(self.running_scripts)

    if(count_of_running_scripts == 0):
      self.set_idle_icon()
    else:
      log.debug("Not setting idle icon, {} scripts are still running."
        .format(count_of_running_scripts))

  def kill_all_runners(self, *gtk_args):

    for runner in self.running_scripts:
      runner.kill()
    
    self.running_scripts = set()
    self.set_idle_icon()

  def set_idle_icon(self):
    GLib.idle_add(self.indicator.set_icon_full, self.IDLE_ICON_SOURCE, "Idle.")

  def set_busy_icon(self):
    GLib.idle_add(self.indicator.set_icon_full, self.BUSY_ICON_SOURCE, "Running.")
    
if __name__ == "__main__":
  main_tray = QuickResolve()
  Gtk.main()