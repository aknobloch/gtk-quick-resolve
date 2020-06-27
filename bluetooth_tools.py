import subprocess
import log

def fix_device(device_mac_address):
    
    reconnect = subprocess.run(["bluetoothctl", "connect", device_mac_address])
    
    if(reconnect.returncode != 0):
      log.error("Reconnecting to device {} failed!".format(device_mac_address))