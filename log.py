import logging
import logging.handlers

LOGGER_GUID = "6286f8b6-278a-4048-ae6d-94acf7f0b439"
LOG_LOCATION = "/var/log/gtk-quick-resolve.log"

sys_logger = logging.getLogger(LOGGER_GUID)
sys_logger.setLevel(logging.INFO)

handler = logging.handlers.SysLogHandler(address=LOG_LOCATION)
sys_logger.addHandler(handler)

def debug(message):
  sys_logger.debug(message)

def info(message):
  sys_logger.info(message)

def error(message):
  sys_logger.error(message)