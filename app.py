import os
from aircraft_data import COMMERCIAL_AIRCRAFT_FAMILIES
import requests
from flask import Flask, render_template, send_from_directory

# Tell Flask where your local logos folder is located
app = Flask(__name__, static_folder="logos")

# Coordinates for Sursee / Central Switzerland and radius in nautical miles
LAT = 47.17
LON = 8.11
RADIUS = 15
ADSB_URL = f"https://api.adsb.lol/v2/point/{LAT}/{LON}/{RADIUS}"


@app.route("/")
def index():
  raw_data = None
  airline_icao = "N/A"
  aircraft_type = "N/A"
  logo_filename = None
  has_local_logo = False

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

        callsign = raw_data.get("flight", "").strip()
        aircraft_type = raw_data.get("t")

        # 1. Parse and sanitize callsign to get airline ICAO code (Uppercase for your logo filenames)
        airline_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()

        # 2. Check if the local file exists in the 'logos' folder
        logo_filename = f"{airline_icao}.png"
        logo_path = os.path.join("logos", logo_filename)
        has_local_logo = os.path.exists(logo_path)

        print(f"Checking for logo at: {logo_path} -> Found: {has_local_logo}")
        print(
            f"DEBUG -> Callsign: '{callsign}', ICAO: '{airline_icao}', Type:"
            f" '{aircraft_type}', Logo File: '{logo_filename}', Found Locally:"
            f" {has_local_logo}"
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
      logo_filename=logo_filename if has_local_logo else None,
  )


# Route to serve the images from the logos folder directly
@app.route("/logos/<path:filename>")
def serve_logo(filename):
  return send_from_directory("logos", filename)


if __name__ == "__main__":
  app.run(debug=True, port=5000)