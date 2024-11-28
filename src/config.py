import os
from pathlib import Path

# Get the absolute path to the src directory
SRC_DIR = Path(__file__).parent

# Go up one level to the project root and then into the data directory
DATA_PATH = os.path.abspath(os.path.join(SRC_DIR.parent, 'Input', 'airline_delay_2023.csv'))

# Default columns
DEFAULT_COLUMNS = [
    "carrier_name", 
    "arr_delay",
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay"
]
 # Region mapping for Different Airports
region_mapping = {
    "Northeast": [
        "JFK", "LGA", "BOS", "PVD", "BDL", "ALB", "SYR", "ROC", "BGM", "BUF",
        "HPN", "ABE", "EWR", "SWF", "PWM", "BTV", "MVY", "ACK", "HYA"
    ],
    "Midwest": [
        "ORD", "MDW", "CLE", "CMH", "DAY", "CVG", "IND", "DTW", "GRR", "LAN",
        "MBS", "MSP", "DSM", "CID", "STL", "MCI", "OMA", "FAR", "GFK", "FSD",
        "BIS", "MOT", "XWA"
    ],
    "South": [
        "ATL", "CLT", "RDU", "IAD", "DCA", "BWI", "ORF", "RIC", "CHS", "SAV",
        "JAX", "MCO", "TPA", "FLL", "MIA", "PBI", "MEM", "BNA", "HSV", "BHM",
        "MOB", "MSY", "DAL", "DFW", "IAH", "HOU", "OKC", "TUL", "SAT", "AUS",
        "CRW", "SHV", "MGM", "GSP"
    ],
    "West": [
        "LAX", "SFO", "SAN", "SJC", "BUR", "ONT", "SMF", "RNO", "LAS", "PHX",
        "TUS", "SEA", "PDX", "BOI", "DEN", "COS", "SLC", "GEG", "MSO", "BZN",
        "FCA", "HLN", "BIL", "RDM"
    ],
    "Alaska": ["ANC", "FAI", "JNU", "KTN", "SIT", "ADK", "BET", "BRW", "CDV", "OTZ", "OME", "SCC", "WRG", "GST", "YAK"],
    "Pacific Territories": ["GUM", "SPN", "PPG"],
    "Other": []  
}