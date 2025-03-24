from flask import Flask, render_template, request, redirect
import subprocess
import platform

app = Flask(__name__, template_folder='templates')

# Detect OS
OS_TYPE = platform.system()


# Function to scan available Wi-Fi networks
def scan_wifi():
    networks = []

    if OS_TYPE == "Linux":
        # Using nmcli for Raspberry Pi/Linux
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
        networks = list(set(result.stdout.strip().split("\n")))  # Remove duplicates
    elif OS_TYPE == "Windows":
        # Using netsh for Windows
        result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        for line in lines:
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                if ssid and ssid not in networks:
                    networks.append(ssid)

    print(f"Scanned Networks ({OS_TYPE}): {networks}")
    return networks


# Function to connect to Wi-Fi (only works on Linux/Raspberry Pi)
def connect_wifi(ssid, password):
    if OS_TYPE == "Linux":
        command = ["nmcli", "dev", "wifi", "connect", ssid, "password", password]
        subprocess.run(command)
    else:
        print(f"Windows detected: Cannot connect to Wi-Fi automatically.")


@app.route("/", methods=["GET", "POST"])
def wifi_setup():
    if request.method == "POST":
        ssid = request.form.get("ssid")
        password = request.form.get("password")
        connect_wifi(ssid, password)
        return redirect("/success")

    networks = scan_wifi()
    return render_template("wifi.html", networks=networks)


@app.route("/success")
def success():
    return "<h2>Wi-Fi connection initiated (Linux only). Please wait...</h2>"


# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
