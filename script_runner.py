import multiprocessing
import log

class ScriptRunner():

  def __init__(self, script, on_finished_listener):
    self.script = script
    self.on_finished_listener = on_finished_listener
    self.runner_process = multiprocessing.Process(target=self.run_helper)

  def run(self, *gtk_args):
    self.runner_process.start()

  def run_helper(self):
    self.script()
    self.on_finished_listener(self)

  def kill(self):
    log.warning("Graceful termination not implemented, killing forcefully...")
    self.runner_process.terminate()
