import requests
import json
import tempfile
import webbrowser
import os

ASCII_ART = r"""
   ____   ____  ____           |  |   ____   ____ _____ _/  |_  ___________
  / ___\_/ __ \/  _ \   ______ |  |  /  _ \_/ ___\\__  \\   __\/  _ \_  __ \
 / /_/  >  ___(  <_> ) /_____/ |  |_(  <_> )  \___ / __ \|  | (  <_> )  | \/
 \___  / \___  >____/          |____/\____/ \___  >____  /__|  \____/|__|
/_____/      \/                                 \/     \/
                                  by beat
"""
FOOTER = "by beat"

RED = "\033[31m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    clear_screen()
    lines = ASCII_ART.strip("\n").splitlines()
    maxw = max(len(l) for l in lines)
    centered_footer = FOOTER.center(maxw)
    print(RED + "\n".join(lines) + "\n" + centered_footer + RESET)

def lookup_ip(ip):
    try:
        if not ip or ip.strip() == "":
            raise ValueError("Invalid IP: input required.")
        url = f"http://ip-api.com/json/{ip}?fields=status,message,query,country,regionName,city,lat,lon,org,timezone"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "success":
            raise ValueError("Invalid IP or query.")
        return data
    except Exception as e:
        print(RED + f"Error looking up IP: {e}" + RESET)
        return None

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>IP Geo Locator</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    html, body, #map {{ height: 100%; margin: 0; padding: 0; }}
    #info {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: white;
      padding: 10px;
      font-family: sans-serif;
      border-radius: 6px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
      z-index: 999;
    }}
  </style>
</head>
<body>
  <div id="info">
    <strong>IP:</strong> {ip}<br/>
    <strong>Location:</strong> {location}<br/>
    <strong>Org:</strong> {org}<br/>
    <strong>Timezone:</strong> {timezone}<br/>
    <strong>Coords:</strong> {lat}, {lon}
  </div>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    var map = L.map('map').setView([{lat}, {lon}], 10);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap contributors'
    }}).addTo(map);
    L.marker([{lat}, {lon}]).addTo(map)
      .bindPopup("<b>{ip}</b><br>{location}")
      .openPopup();
  </script>
</body>
</html>
"""

def generate_map_html(data):
    try:
        ip = data.get("query", "")
        city = data.get("city", "")
        region = data.get("regionName", "")
        country = data.get("country", "")
        lat = data.get("lat", 0)
        lon = data.get("lon", 0)
        org = data.get("org", "—")
        timezone = data.get("timezone", "—")
        location = ", ".join(filter(None, [city, region, country]))
        return HTML_TEMPLATE.format(
            ip=ip,
            location=location or "—",
            org=org,
            timezone=timezone,
            lat=lat,
            lon=lon
        )
    except Exception as e:
        print(RED + f"Error generating map HTML: {e}" + RESET)
        return None

def open_map_for_ip(ip_input):
    try:
        data = lookup_ip(ip_input)
        if data is None:
            return
        lat = data.get("lat")
        lon = data.get("lon")
        if not lat or not lon:
            print(RED + "Error: No coordinates found." + RESET)
            print(json.dumps(data, indent=2))
            return
        html = generate_map_html(data)
        if html is None:
            return
        tmpdir = tempfile.mkdtemp(prefix="ip_map_")
        html_path = os.path.join(tmpdir, "ip_map.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open(f"file://{html_path}")
        print("Map opened in your browser.")
    except Exception as e:
        print(RED + f"Error opening map: {e}" + RESET)

def main():
    try:
        while True:
            print_ascii()
            user = input("Enter IP to locate (or 'q' to quit): ").strip()
            if user.lower() in ('q', 'quit', 'exit'):
                break
            if not user:
                print(RED + "Error: You must enter an IP address." + RESET)
                input("Press Enter to continue...")
                continue
            print(f"Looking up IP: {user}...")
            open_map_for_ip(user)
            input("Press Enter to continue...")
    except Exception as e:
        print(RED + f"Error in main loop: {e}" + RESET)

if __name__ == "__main__":
    main()
