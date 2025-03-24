import subprocess
import time
import os


def is_connected():
    result = subprocess.run(["nmcli", "-t", "-f", "STATE", "networking"], capture_output=True, text=True)
    return "connected" in result.stdout.strip()


while True:
    if not is_connected():
        print("Wi-Fi disconnected! Starting setup server...")
        os.system("python3 wifi_setup.py")
    time.sleep(10)  # Check every 10 seconds
