import os
import seaborn as sns
import matplotlib.pyplot as plt
from .config import region_mapping
from .data_management import DataHandler
import pandas as pd
from .module_tmp import DataProcessor, calculate_stats

class DataVisualizer(DataHandler):
    def __init__(self, config):
        super().__init__(config)
        self.processor = DataProcessor()  # Add DataProcessor instance
        
        # Check for region_mapping
        if "region_mapping" not in config:
            raise ValueError("missing region_mapping")
        self.region_mapping = config["region_mapping"]
        
    def analyze_column(self, column_name):
        """New method using module_tmp functionality"""
        if column_name in self.data_df.columns:
            data = self.data_df[column_name].dropna().tolist()
            stats = {
                'mean': calculate_stats(data, 'mean'),
                'median': calculate_stats(data, 'median'),
                'lambda_process': self.processor.process_with_lambda(data)
            }
            return stats
        return None

    def categorize_airports(self):
        """Map airport codes to their respective regions."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to process.")
            return
        
        # Reverse mapping for quick lookup
        airport_to_region = {
            airport: region
            for region, airports in self.region_mapping.items()
            for airport in airports
        }
        
        # Create a new 'region' column based on the airport mapping
        if 'airport' in self.data_df.columns:
            self.data_df['region'] = self.data_df['airport'].map(airport_to_region).fillna('Other')
        else:
            print("Column 'airport' not found in the dataset.")
    
    def plot_violin(self, column_name):
        """Visualize the distribution of a column using a violin plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        # Categorize airports if not already done
        if 'region' not in self.data_df.columns:
            self.categorize_airports()
        
        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        plt.figure(figsize=(14, 8))
        sns.violinplot(data=self.data_df, x='region', y=column_name, palette="muted")
        plt.title(f"Violin Plot of {column_name} by Region")
        plt.xlabel("Region")
        plt.ylabel(column_name)
        plt.xticks(rotation=45)  # Rotate region labels for readability
        
        # Save the plot to Output folder
        self.save_plot(f"violin_{column_name}")

    def plot_box(self, column_name):
        """Visualize the distribution of a column using a box plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        # Categorize airports if not already done
        if 'region' not in self.data_df.columns:
            self.categorize_airports()
        
        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.data_df, x='region', y=column_name, palette="muted")
        plt.title(f"Box Plot of {column_name} by Region")
        plt.xlabel("Region")
        plt.ylabel(column_name)
        plt.xticks(rotation=45)  # Rotate region labels for readability
        
        # Save the plot to Output folder
        self.save_plot(f"box_{column_name}")

    def plot_scatter(self, x_column, y_column):
        """Visualize the relationship between two columns using a scatter plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return

        if x_column not in self.data_df.columns or y_column not in self.data_df.columns:
            print(f"Columns '{x_column}' or '{y_column}' not found in the dataset.")
            return

        # Categorize airports if not already done
        if 'region' not in self.data_df.columns:
            self.categorize_airports()

        plt.figure(figsize=(14, 8))  # Increase figure size
        sns.scatterplot(data=self.data_df, x=x_column, y=y_column, hue="region", palette="tab10")
        plt.title(f"Scatter Plot of {x_column} vs {y_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)

        plt.yticks(rotation=90)
    
        # Adjust legend placement
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        # Reduce the number of ticks
        plt.locator_params(axis='y', nbins=10)

        # Save the plot to Output folder
        self.save_plot(f"scatter_{x_column}_vs_{y_column}")

    def query_data(self, column_name, condition):
        """Query data using Boolean indexing for numeric and string columns while reusing parent's query_data."""
        if self.data_df.empty:
            print("Error: No data loaded to query.")
            return pd.DataFrame()

        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return pd.DataFrame()

        filtered_data = super().query_data(column_name, condition)

        if filtered_data.empty:
            return filtered_data  
        if self.data_df[column_name].dtype == 'object' or self.data_df[column_name].dtype.name == 'category':
            
            condition_mask = self.data_df[column_name].apply(lambda x: eval(f"'{x}' {condition}") if pd.notna(x) else False)
        else:
            condition_mask = self.data_df[column_name].apply(lambda x: eval(f"{x} {condition}") if pd.notna(x) else False)

        filtered_data = self.data_df[condition_mask]
        print(f"Query successful! {len(filtered_data)} rows found.")
        return filtered_data

    def save_plot(self, plot_name):
        """Helper method to save plots in the Output directory."""
        output_folder = "Output"  # Directory where the images will be saved
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the plot with a unique name
        output_file = os.path.join(output_folder, f"{plot_name}.png")
        plt.savefig(output_file)
        print(f"Plot saved as {output_file}")

        plt.close()
