import pandas as pd
import matplotlib.pyplot as plt
from config import DATA_PATH, DEFAULT_COLUMNS

class DataHandler:
    def __init__(self, config):
        self.config = config
        self.data_df = None

    def load_data(self):
        """Load the dataset from the configured path."""
        try:
            self.data_df = pd.read_csv(self.config["DATA_PATH"])
            print("Data loaded successfully!")
        except FileNotFoundError:
            print(f"Error: File not found at {self.config['DATA_PATH']}")
            self.data_df = pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data_df = pd.DataFrame()

    def visualize_delays(self):
        """Visualize all types of delays in a multi-line plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return

        # Define delay columns and their colors
        delay_columns = {
            'arr_delay': 'blue',
            'carrier_delay': 'red',
            'weather_delay': 'green',
            'nas_delay': 'purple',
            'security_delay': 'orange',
            'late_aircraft_delay': 'brown'
        }

        # Create figure with enough height and width
        plt.figure(figsize=(15, 8))

        # Plot each delay type
        for column, color in delay_columns.items():
            if column in self.data_df.columns:
                # Calculate average delay by carrier for this type
                avg_delays = self.data_df.groupby('carrier_name')[column].mean().sort_values(ascending=False)
                plt.plot(range(len(avg_delays)), 
                        avg_delays, 
                        marker='o', 
                        linestyle='-', 
                        color=color, 
                        label=column.replace('_', ' ').title(),
                        linewidth=2)

        # Customize the plot
        plt.title('Average Delays by Carrier and Delay Type')
        plt.xlabel('Carrier')
        plt.ylabel('Average Delay (minutes)')
        
        # Set x-axis labels (carrier names)
        carriers = self.data_df.groupby('carrier_name')['arr_delay'].mean().sort_values(ascending=False).index
        plt.xticks(range(len(carriers)), carriers, rotation=45, ha='right')
        
        # Add legend
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Add grid
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        plt.show()

    def visualize_column(self, column_name):
        """Visualize data for a given column using a line plot with improved label handling."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        data = self.data_df[column_name].dropna()

        if data.dtype == 'object' or data.dtype.name == 'category':
            value_counts = data.value_counts().sort_index()
            
            plt.figure(figsize=(15, 8))
            ax = value_counts.plot(kind="line", marker="o", color="skyblue", linewidth=2)
            
            plt.title(f"Frequency of {column_name} (Line Plot)")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, ha='right')
            plt.tight_layout()
            plt.grid(True, linestyle='--', alpha=0.7)
            
            for i, v in enumerate(value_counts):
                ax.text(i, v, str(v), ha='center', va='bottom')
        
        else:
            plt.figure(figsize=(15, 8))
            data.value_counts().sort_index().plot(kind="line", marker="o", color="skyblue", linewidth=2)
            plt.title(f"Frequency of {column_name} (Line Plot)")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

        plt.show()

    def query_data(self, column_name, condition):
        """Query the data based on a condition."""
        if self.data_df.empty:
            print("Error: No data loaded to query.")
            return pd.DataFrame()

        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return pd.DataFrame()

        query_str = f"{column_name} {condition}"
        try:
            filtered_data = self.data_df.query(query_str)
            print(f"Query successful! {len(filtered_data)} rows found.")
            return filtered_data
        except Exception as e:
            print(f"Error in query: {e}")
            return pd.DataFrame()

    def query_arrival_delays_by_carrier(self):
        """Query the number of arrival delays for a specific carrier."""
        if self.data_df.empty:
            print("Error: No data loaded to query.")
            return

        carrier_name = input("Enter the carrier name: ").strip()
        
        if carrier_name not in self.data_df["carrier_name"].unique():
            print(f"Carrier '{carrier_name}' not found in the dataset.")
            return
        
        carrier_data = self.data_df[self.data_df["carrier_name"] == carrier_name]
        total_delays = carrier_data["arr_delay"].dropna().count()
        print(f"The total number of recorded arrival delays for '{carrier_name}' is: {total_delays}")

# Example usage
if __name__ == "__main__":
    # Load configuration
    config = {
        "DATA_PATH": DATA_PATH,
        "DEFAULT_COLUMNS": DEFAULT_COLUMNS,
    }

    # Initialize and load data
    handler = DataHandler(config)
    handler.load_data()

    while True:
        print("\nAirport Data Analysis Menu:")
        print("1. View all carriers (visualization)")
        print("2. View all delay types comparison")
        print("3. Query arrival delays by carrier")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            handler.visualize_column("carrier_name")
        elif choice == '2':
            handler.visualize_delays()
        elif choice == '3':
            handler.query_arrival_delays_by_carrier()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")