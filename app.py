import os
from flask import Flask, render_template, send_from_directory

# Tell Flask where your local logos folder is located
app = Flask(__name__, static_folder="logos")


@app.route("/")
def index():
  raw_data = {
      "hex": "4d00de",
      "type": "adsb_icao",
      "flight": "LGL65R  ",
      "r": "LX-LED",
      "t": "E295",
      "alt_baro": 33775,
      "lat": 47.280716,
      "lon": 8.070351,
  }

  # 1. Parse and sanitize callsign to get airline ICAO code (e.g. "LGL")
  raw_callsign = raw_data.get("flight", "").strip()
  airline_icao = "".join([c for c in raw_callsign if c.isalpha()])[
      :3
  ].upper()
#   ].lower()  # lowercase matches standard filenames usually

  aircraft_type = raw_data.get("t")

  # 2. Check if the local file exists in the 'logos' folder
  logo_filename = f"{airline_icao}.png"
  logo_path = os.path.join("logos", logo_filename)

  has_local_logo = os.path.exists(logo_path)
  print(f"Checking for logo at: {logo_path} -> Found: {has_local_logo}")
  print(
    f"DEBUG -> Callsign: '{raw_data.get('flight')}', ICAO: '{airline_icao}',"
    f" Type: '{aircraft_type}', Logo File: '{logo_filename}', Found Locally:"
    f" {has_local_logo}"
)

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