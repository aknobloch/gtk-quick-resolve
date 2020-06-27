import gi
import threading
import log

gi.require_version("AppIndicator3", "0.1") 
from gi.repository import AppIndicator3, GLib

'''
Convenience class to run a script while updating the tray icon
as appropriate. The icon will be updated to the BUSY_ICON_SOURCE
when the script is invoked, and then set to the IDLE_ICON_SOURCE
once the script is finished.

This class is necessary because the script must be run on a
separate thread, or else the GLib.idle_add will not invoke until
the script finishes.
'''
class ScriptRunner():

  total_running_scripts = 0

  def __init__(self, app_indicator, busy_icon, idle_icon, script):
    self.app_indicator = app_indicator
    self.script = script
    self.busy_icon = busy_icon
    self.idle_icon = idle_icon

  '''
  Kicks off the script on a new thread, immediately returning.
  This will take care of setting the icon as appropriate, then
  resetting the icon as appropriate when the script has finished.
  '''
  def run(self, *gtk_args):
    GLib.idle_add(self.app_indicator.set_icon_full, self.busy_icon, "Running.")
    threading.Thread(target=self.run_helper).start()

  '''
  Runs the associated script and then sets the indicator icon back
  to the idle status, if appropriate.
  '''
  def run_helper(self):
    
    self.total_running_scripts = self.total_running_scripts + 1
    self.script()
    self.total_running_scripts = self.total_running_scripts - 1

    if(self.total_running_scripts == 0):
      GLib.idle_add(self.app_indicator.set_icon_full, self.idle_icon, "Idle.")
    else:
      log.info("{} scripts still running, not changing to idle icon.".format(self.total_running_scripts))