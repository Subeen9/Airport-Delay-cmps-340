import os
from pathlib import Path

# Get the absolute path to the src directory
SRC_DIR = Path(__file__).parent

# Go up one level to the project root and then into the data directory
DATA_PATH = os.path.abspath(os.path.join(SRC_DIR.parent, 'data', 'airline_delay_2023.csv'))

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