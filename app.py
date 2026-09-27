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
            print(f"Successfully fetched {len(aircraft_list)} aircraft within {RADIUS}NM of ({LAT}, {LON}).\n")

            acceptable_aircrafts_list = []
            for aircraft in aircraft_list:
                callsign = aircraft.get("flight", "").strip()
                a_type = aircraft.get("t")
                
                # Parse airline ICAO from callsign
                parsed_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()

                # Check if ICAO is in your loaded livery list
                if parsed_icao in LIVERY_ICAOS:
                    print(f"Yes {parsed_icao} is in the ICAOS!")
                    acceptable_aircrafts_list.append(aircraft) # Fixed: use .append()
                else:
                    print(f"{parsed_icao} is NOT in the ICAOS!")

            if acceptable_aircrafts_list:
                # Pick the first matching aircraft
                raw_data = acceptable_aircrafts_list[0]
                
                # Re-extract details specifically for the selected raw_data aircraft
                callsign = raw_data.get("flight", "").strip()
                airline_icao = "".join([c for c in callsign if c.isalpha()])[:3].upper()
                aircraft_type = raw_data.get("t", "N/A")
                
                # Safe lookup for commercial family
                pure_type = COMMERCIAL_AIRCRAFT_FAMILIES.get(aircraft_type, "N/A")

                # Get the specific livery PNG name if needed
                livery_png_type_name = f"{airline_icao}_{pure_type}.png"

                # Check if the simple logo file exists in 'static/logos/'
                logo_filename = f"{airline_icao}.png"
                logo_path = os.path.join("static", "logos", logo_filename)
                has_local_logo = os.path.exists(logo_path)

                print(
                    f"DEBUG -> Callsign: {callsign}\n"
                    f"ICAO: {airline_icao}\n"
                    f"Type: {aircraft_type}\n"
                    f"Logo File: {logo_filename}\n"
                    f"Found Locally: {has_local_logo}\n"
                    f"PNG Type: {pure_type}\n"
                    f"PNG file name: {livery_png_type_name}\n"
                )
            else:
                print("API returned 200, but no matching aircraft found with your livery ICAOs in range.")
        else:
            print(f"Error fetching from adsb.lol: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Fallback dummy data if no matching aircraft are found
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
        png_filename=livery_png_type_name if livery_png_type_name != "N/A_" else None,
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