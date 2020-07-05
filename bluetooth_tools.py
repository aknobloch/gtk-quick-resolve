import subprocess
import log
import time

def fix_device(device_mac_address, scan_timeout_in_seconds):
    
  subprocess.run(["bluetoothctl", "remove", device_mac_address])
  scan_for_device(device_mac_address, scan_timeout_in_seconds)
  subprocess.run(["bluetoothctl", "connect", device_mac_address])


def scan_for_device(mac_address, timeout):

  bluetooth_device_scan = subprocess.Popen(
      ["bluetoothctl", "scan", "on"],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT
  )

  log.info("Bluetooth device scan for {} initiated!".format(mac_address))
  time.sleep(timeout)
  bluetooth_device_scan.terminate()
  log.info("Device scan is complete.")

  while bluetooth_device_scan.stdout.peek():

    scan_result = bluetooth_device_scan.stdout.readline().decode("UTF-8")
    
    if mac_address in scan_result:
      log.info("Found device {} while scanning.".format(mac_address))
      return True

  log.error("Could not located device {} while scanning!".format(mac_address))
  return False