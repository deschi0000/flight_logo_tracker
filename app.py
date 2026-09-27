import os
from aircraft_data import COMMERCIAL_AIRCRAFT_FAMILIES
from aircraft_icaos import LIVERY_ICAOS
import requests
from flask import Flask, render_template, send_from_directory
from datetime import datetime

# Tell Flask where your local logos folder is located
app = Flask(__name__, static_folder="static")

# Coordinates for Sursee / Central Switzerland and radius in nautical miles
LAT = 47.17
LON = 8.11
RADIUS = 15
ADSB_URL = f"https://api.adsb.lol/v2/point/{LAT}/{LON}/{RADIUS}"


@app.route("/")
def index():

  # Check if it's currently daytime (e.g., between 6:00 AM and 8:00 PM)
  current_hour = datetime.now().hour
  is_daylight = 6 <= current_hour < 20

  raw_data = None
  airline_icao = "N/A"
  aircraft_type = "N/A"
  logo_filename = None
  has_local_logo = False
  pure_type = "N/A"
  livery_png_type_name = "N/A"

  headers = {"User-Agent": "FlightLogoTracker/1.0"}

  try:
    response = requests.get(ADSB_URL, headers=headers)
    if response.status_code == 200:
      data = response.json()
      aircraft_list = data.get("ac", [])
      print(
          f"Successfully fetched {len(aircraft_list)} aircraft within"
          f" {RADIUS}NM of ({LAT}, {LON}).\n"
      )

      if aircraft_list:
        # Pick the first aircraft from the live feed
        raw_data = aircraft_list[0]

        print(f'RAW DATA: {raw_data}')

        print(f'type: {type(aircraft_list)}')
        altitude_check_list = [(i["flight"], i["alt_baro"]) for i in aircraft_list]
        print(altitude_check_list)

        a

        callsign = raw_data.get("flight", "").strip()
        aircraft_type = raw_data.get("t")
        pure_type = COMMERCIAL_AIRCRAFT_FAMILIES[aircraft_type] # Get the type from the dict
        

        # 1. Parse and sanitize callsign to get airline ICAO code (Uppercase for your logo filenames)
        airline_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()

        #1.5 Get the file name if it exists
        livery_png_type_name = airline_icao + '_' + pure_type + '.png'

        # 2. Check if the local file exists in the 'static/logos' folder
        logo_filename = f"{airline_icao}.png"
        logo_path = os.path.join("static", "logos", logo_filename)  # <--- Updated path
        has_local_logo = os.path.exists(logo_path)

        # print(f"Checking for logo at: {logo_path} -> Found: {has_local_logo}")
        print(
            f"DEBUG -> Callsign: {callsign}\n" 
            f"ICAO: {airline_icao}\n" 
            f"Type: {aircraft_type}\n" 
            f"Logo File: {logo_filename}\n"
            f"Found Locally:{has_local_logo}\n"
            f"PNG Type: {pure_type}\n"
            f"PNG file name: {livery_png_type_name}\n"
        )
      else:
        print("API returned 200, but no aircraft currently found in range.")
    else:
      print(f"Error fetching from adsb.lol: {response.status_code}")

  except Exception as e:
    print(f"An error occurred: {e}")

  # Fallback dummy data if no live aircraft are returned so the page doesn't crash
  if not raw_data:
    raw_data = {
        "flight": "NO FLIGHT",
        "r": "N/A",
        "t": "N/A",
        "alt_baro": 0,
        "lat": LAT,
        "lon": LON,
    }

  return render_template(
      "index.html",
      raw_data=raw_data,
      airline_icao=airline_icao,
      aircraft_type=aircraft_type,
      png_filename = livery_png_type_name if livery_png_type_name else None,
      logo_filename=logo_filename if has_local_logo else None,
      is_daylight=is_daylight
  )


# Route to serve the images from the logos folder directly
# This would have skirted looking into the 'static' folder
# Instead checking the same level 'logos' folder!
# @app.route("/logos/<path:filename>")
# def serve_logo(filename):
#   return send_from_directory("logos", filename)


if __name__ == "__main__":
  app.run(debug=True, port=5000)