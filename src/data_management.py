#%% MODULE BEGINS
# module_name = "data_management.py"

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Library Imports
import os
from pathlib import Path

# Third-Party Library Imports
import pandas as pd
import matplotlib.pyplot as plt


class DataHandler:
    def __init__(self):
        """Initialize DataHandler with built-in configuration."""
        # Get the absolute path to the src directory
        SRC_DIR = Path(__file__).parent
        
        # Go up one level to the project root and then into the data directory
        self.DATA_PATH = os.path.abspath(os.path.join(SRC_DIR.parent, 'Input', 'airline_delay_2023.csv'))
        
        self.DEFAULT_COLUMNS = [
            "carrier_name", 
            "arr_delay",
            "carrier_delay",
            "weather_delay",
            "nas_delay",
            "security_delay",
            "late_aircraft_delay"
        ]
        
        self.region_mapping = {
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
            "Alaska": [
                "ANC", "FAI", "JNU", "KTN", "SIT", "ADK", "BET", "BRW", "CDV", 
                "OTZ", "OME", "SCC", "WRG", "GST", "YAK"
            ],
            "Pacific Territories": ["GUM", "SPN", "PPG"],
            "Other": []  
        }
        
        self.data_df = None

    def load_data(self):
        """Load data from the built-in path."""
        try:
            self.data_df = pd.read_csv(self.DATA_PATH)
            print(f"Data loaded successfully from {self.DATA_PATH}")
        except FileNotFoundError:
            print(f"Error: File not found at {self.DATA_PATH}")
            self.data_df = pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data_df = pd.DataFrame()

    # Rest of the methods remain the same
    def visualize_delays(self):
        """Visualize all types of delays in a multi-line plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return

        delay_columns = {
            'arr_delay': 'blue',
            'carrier_delay': 'red',
            'weather_delay': 'green',
            'nas_delay': 'purple',
            'security_delay': 'orange',
            'late_aircraft_delay': 'brown',
        }

        plt.figure(figsize=(15, 8))
        for column, color in delay_columns.items():
            if column in self.data_df.columns:
                avg_delays = self.data_df.groupby('carrier_name')[column].mean().sort_values(ascending=False)
                plt.plot(range(len(avg_delays)),
                         avg_delays,
                         marker='o',
                         linestyle='-',
                         color=color,
                         label=column.replace('_', ' ').title(),
                         linewidth=2)

        plt.title('Average Delays by Carrier and Delay Type')
        plt.xlabel('Carrier')
        plt.ylabel('Average Delay (minutes)')
        carriers = self.data_df.groupby('carrier_name')['arr_delay'].mean().sort_values(ascending=False).index
        plt.xticks(range(len(carriers)), carriers, rotation=45, ha='right')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        self.save_plot("average_delays_by_carrier")
        plt.show()
        plt.close()

    def visualize_delay_histogram(self, column):
        """Create a histogram for the specified delay column."""
        if self.data_df is not None:
            if column in self.data_df.columns:
                plt.figure(figsize=(10, 6))
                self.data_df[column].dropna().plot(kind='hist', bins=30, color='skyblue', edgecolor='black')
                plt.title(f'Distribution of {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')
                plt.grid(True)
                plt.tight_layout()
                
                self.save_plot(f"histogram_{column}")
                plt.show()
                plt.close()
            else:
                print(f"Column '{column}' not found in the dataset.")
        else:
            print("Data not loaded. Please load the data first.")

    def visualize_column(self, column_name):
        """Visualize frequency distribution of a column."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return

        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        data = self.data_df[column_name].dropna()
        plt.figure(figsize=(15, 8))

        if data.dtype == 'object' or data.dtype.name == 'category':
            value_counts = data.value_counts().sort_index()
            ax = value_counts.plot(kind="line", marker="o", color="skyblue", linewidth=2)
            plt.title(f"Frequency of {column_name} (Line Plot)")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.grid(True, linestyle='--', alpha=0.7)

            for i, v in enumerate(value_counts):
                ax.text(i, v, str(v), ha='center', va='bottom')
        else:
            data.value_counts().sort_index().plot(kind="line", marker="o", color="skyblue", linewidth=2)
            plt.title(f"Frequency of {column_name} (Line Plot)")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, linestyle='--', alpha=0.7)

        plt.tight_layout()
        self.save_plot(f"{column_name}_frequency_plot")
        plt.show()
        plt.close()

    def query_arrival_delays_by_carrier(self):
        """Query arrival delays for a specific carrier."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to query.")
            return

        carrier_name = input("Enter the carrier name: ").strip()
        if carrier_name not in self.data_df["carrier_name"].unique():
            print(f"Carrier '{carrier_name}' not found in the dataset.")
            return

        carrier_data = self.data_df[self.data_df["carrier_name"] == carrier_name]
        total_delays = carrier_data["arr_delay"].dropna().count()
        print(f"The total number of recorded arrival delays for '{carrier_name}' is: {total_delays}")

    def save_plot(self, plot_name):
        """Helper method to save plots in the Output directory."""
        output_folder = "Output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, f"{plot_name}.png")
        plt.savefig(output_file)
        print(f"Plot saved as {output_file}")