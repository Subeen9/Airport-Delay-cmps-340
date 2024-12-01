#%% MODULE BEGINS
# module_name = "data_operations.py"

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Library Imports
import os

# Third-Party Library Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Relative Imports
from .data_management import DataHandler


class DataVisualizer(DataHandler):
    def __init__(self):
        """Initialize DataVisualizer with parent's configuration."""
        super().__init__()

    def categorize_airports(self):
        """Map airport codes to their respective regions."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to process.")
            return
    # Utilizes Configuration constants    
        airport_to_region = {
            airport: region
            for region, airports in self.region_mapping.items()
            for airport in airports
        }
        
        if 'airport' in self.data_df.columns:
            self.data_df['region'] = self.data_df['airport'].map(airport_to_region).fillna('Other')
        else:
            print("Column 'airport' not found in the dataset.")
    
    def plot_violin(self, column_name):
        """Create a violin plot for the specified column by region."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
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
        plt.xticks(rotation=45)
        
        self.save_plot(f"violin_{column_name}")
        plt.show()
        plt.close()

    def plot_box(self, column_name):
        """Create a box plot for the specified column by region."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
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
        plt.xticks(rotation=45)
        
        self.save_plot(f"box_{column_name}")
        plt.show()
        plt.close()

    def plot_scatter(self, x_column, y_column):
        """Create a scatter plot between two columns, colored by region."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return

        if x_column not in self.data_df.columns or y_column not in self.data_df.columns:
            print(f"Columns '{x_column}' or '{y_column}' not found in the dataset.")
            return

        if 'region' not in self.data_df.columns:
            self.categorize_airports()

        plt.figure(figsize=(14, 8))
        sns.scatterplot(data=self.data_df, x=x_column, y=y_column, hue="region", palette="tab10")
        plt.title(f"Scatter Plot of {x_column} vs {y_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.yticks(rotation=90)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.locator_params(axis='y', nbins=10)
        
        self.save_plot(f"scatter_{x_column}_vs_{y_column}")
        plt.show()
        plt.close()
    
    def query_data(self, column_name, condition, value):
        """Query data based on specified conditions."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to query.")
            return pd.DataFrame()

        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return pd.DataFrame()

        try:
            if condition == '>':
                result_df = self.data_df[self.data_df[column_name] > value]
            elif condition == '<':
                result_df = self.data_df[self.data_df[column_name] < value]
            elif condition == '==':
                result_df = self.data_df[self.data_df[column_name] == value]
            elif condition == '!=':
                result_df = self.data_df[self.data_df[column_name] != value]
            elif condition == '>=':
                result_df = self.data_df[self.data_df[column_name] >= value]
            elif condition == '<=':
                result_df = self.data_df[self.data_df[column_name] <= value]
            else:
                print(f"Unsupported condition '{condition}'. Please use one of: '>', '<', '==', '!=', '>=', '<='.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error applying condition: {e}")
            return pd.DataFrame()

        if result_df.empty:
            print("No data matched the query.")
        else:
            print(f"Query returned {len(result_df)} rows.")
    
        return result_df