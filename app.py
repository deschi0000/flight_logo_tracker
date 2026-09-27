import os
from aircraft_data import COMMERCIAL_AIRCRAFT_FAMILIES
from aircraft_icaos import LIVERY_ICAOS
import requests
from flask import Flask, render_template, send_from_directory, jsonify
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
    current_hour = datetime.now().hour
    is_daylight = 6 <= current_hour < 20
    return render_template("index.html", is_daylight=is_daylight)

# New API endpoint for background updates
@app.route("/api/current-aircraft")
def current_aircraft():
    raw_data = None
    airline_icao = "N/A"
    aircraft_type = "N/A"
    livery_png_type_name = None
    has_local_logo = False
    logo_filename = None

    headers = {"User-Agent": "FlightLogoTracker/1.0"}

    try:
        response = requests.get(ADSB_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            aircraft_list = data.get("ac", [])
            
            acceptable_aircrafts_list = []
            for aircraft in aircraft_list:
                callsign = aircraft.get("flight", "").strip()
                parsed_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()

                if parsed_icao in LIVERY_ICAOS:
                    acceptable_aircrafts_list.append(aircraft)

            if acceptable_aircrafts_list:
                raw_data = acceptable_aircrafts_list[0]
                callsign = raw_data.get("flight", "").strip()
                airline_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()
                aircraft_type = raw_data.get("t", "N/A")
                pure_type = COMMERCIAL_AIRCRAFT_FAMILIES.get(aircraft_type, "N/A")
                livery_png_type_name = f"{airline_icao}_{pure_type}.png"
                
                logo_filename = f"{airline_icao}.png"
                logo_path = os.path.join("static", "logos", logo_filename)
                has_local_logo = os.path.exists(logo_path)
    except Exception as e:
        print(f"Error: {e}")

    if not raw_data:
        raw_data = {
            "flight": "NO FLIGHT",
            "r": "N/A",
            "t": "N/A",
        }
        airline_icao = "N/A"
        aircraft_type = "N/A"
        livery_png_type_name = None

    # Return pure JSON data to the frontend
    return jsonify({
        "flight": raw_data.get("flight", "NO FLIGHT"),
        "registration": raw_data.get("r", "N/A"),
        "airline_icao": airline_icao,
        "aircraft_type": aircraft_type,
        "png_filename": livery_png_type_name if livery_png_type_name != "N/A_N/A.png" else None
    })

# Route to serve the images from the logos folder directly
# This would have skirted looking into the 'static' folder
# Instead checking the same level 'logos' folder!
# @app.route("/logos/<path:filename>")
# def serve_logo(filename):
#   return send_from_directory("logos", filename)


if __name__ == "__main__":
  app.run(debug=True, port=5000)