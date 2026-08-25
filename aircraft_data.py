# aircraft_data.py

COMMERCIAL_AIRCRAFT_FAMILIES = {
    # ==========================================
    # 1. AIRBUS FAMILY
    # ==========================================
    "BCS1": "A220",  # A220-100
    "BCS3": "A220",  # A220-300
    "220": "A220",  # Short code mapping
    "A318": "A320",
    "A319": "A320",
    "A320": "A320",
    "A321": "A320",
    "A20N": "A320",  # A320neo
    "A21N": "A320",  # A321neo
    "A319N": "A320",  # A319neo
    "AB3": "A300",  # Airbus A300
    "A300": "A300",  # Airbus A300
    "A332": "A330",  # A330-200
    "A333": "A330",  # A330-300
    "A338": "A330",  # A330-800neo
    "A339": "A330",  # A330-900neo
    "A342": "A340",
    "A343": "A340",
    "A345": "A340",
    "A346": "A340",
    "A359": "A351",  # A350-900
    "A35K": "A351",  # A350-1000
    "351": "A351",  # Short code mapping
    "A388": "A380",  # A380-800
    # ==========================================
    # 2. BOEING FAMILY
    # ==========================================
    "B732": "738",
    "B733": "738",
    "B734": "738",
    "B735": "738",
    "B736": "738",
    "B737": "738",
    "B738": "738",
    "B739": "738",
    "B37M": "738",  # 737 MAX 7
    "B38M": "738",  # 737 MAX 8
    "B39M": "738",  # 737 MAX 9
    "B3XM": "738",  # 737 MAX 10
    "B742": "747",
    "B743": "747",
    "B744": "747",
    "B748": "747",
    "B762": "767",
    "B763": "767",
    "B764": "767",
    "B772": "777",
    "B773": "777",
    "B77L": "777",
    "B77W": "777",
    "B779": "777",  # 777X
    "B788": "787",  # 787-8
    "B789": "787",  # 787-9
    "B78X": "787",  # 787-10
    # ==========================================
    # 3. COMAC FAMILY
    # ==========================================
    "ARJ2": "ARJ21",
    "ARJ21": "ARJ21",
    "C909": "ARJ21",  # Comac C909 (rebranded ARJ21)
    "C919": "C919",
    "919": "C919",  # Short code mapping
    # ==========================================
    # 4. EMBRAER & REGIONAL JETS
    # ==========================================
    "E120": "EM2",  # Embraer EMB 120 Brasilia (ICAO)
    "EM2": "EM2",   # Embraer EMB 120 Brasilia (IATA)
    "E135": "ERJ",
    "E145": "ERJ",
    "ERJ": "ERJ",  # General ERJ category
    "E170": "E75",
    "E175": "E75",
    "E75": "E75",
    "E190": "E90",
    "E195": "E90",
    "E90": "E90",
    "E290": "E90",  # E-Jets E2 (E190-E2)
    "E295": "E90",  # E-Jets E2 (E195-E2)
    "CR9": "CR9",  # Bombardier CRJ-900
    "CRJ9": "CR9",
    # ==========================================
    # 5. TURBOPROPS & OTHERS
    # ==========================================
    "AT43": "AT7",
    "AT45": "AT7",
    "AT72": "AT7",
    "AT7": "AT7",  # ATR 72 series
    "DH8A": "DH8",
    "DH8B": "DH8",
    "DH8C": "DH8",
    "DH8D": "DH8",
    "DH8": "DH8",  # Dash 8 family
    "BE9L": "BE9",  # Beechcraft King Air 90 (turboprop twin)
    "BE9T": "BE9",  # Beechcraft King Air 90 variants
    "BE9": "BE9",   # Beechcraft 90/99 series
    "BE20": "BE9",  # Often grouped or mapped if using a broad twin turboprop asset
    "S20": "S20",  # Saab 2000
    "SB20": "S20",  # Saab 2000 alternative ICAO code
    # ==========================================
    # 6. CLASSICS & OTHERS (BAe, MD, Fokker)
    # ==========================================
    "AR1": "146",   # Avro RJ85 / RJ100
    "146": "146",   # BAe 146
    "M80": "M80",   # McDonnell Douglas MD-80 series
    "MD80": "M80",
    "DC10": "DC10", # McDonnell Douglas DC-10
    "D10": "DC10",  # Short code / IATA mapping
    "MD10": "DC10", # Upgraded MD-10 variant
    "F70": "F70",   # Fokker 70
    "F50": "F50",   # Fokker 50
    
}