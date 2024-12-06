#%% MODULE BEGINS
# module_name = "stats_analyzer.py"

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Library Imports
import math
import os
import pickle
from pathlib import Path

# Third-Party Library Imports
import pandas as pd
import numpy as np


class AdvanceCalculations:
    def __init__(self, config):
        """
        Initialize the parent class with configurations and data storage.
        """
        self.config = config or {}
        self.data = None  # Placeholder for dataset
        self.output_folder = self.config.get('OUTPUT_FOLDER', 'Output')
        self.stats_cache = {}  # Cache for storing statistical results

    # --------------------
    # Core Utilities
    # --------------------

    def load_data(self):
        """Load the dataset from the configured path."""
        try:
            self.data = pd.read_csv(self.config["DATA_PATH"])
            print("Data loaded successfully!")
        except FileNotFoundError:
            print(f"Error: File not found at {self.config['DATA_PATH']}")
            self.data = pd.DataFrame()

    def validate_column(self, column):
        """
        Ensure the specified column exists in the dataset.
        """
        if self.data is None or self.data.empty:
            raise ValueError("Dataset is not loaded or is empty.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in dataset.")

    def save_stats_to_pickle(self, column, stat_type, value):
        """
        Save statistical results to pickle file and in-memory cache.
        
        Args:
        - column: Column name
        - stat_type: Type of statistic (mean, median, std)
        - value: Calculated statistical value
        """
        # Create filename for pickle
        filename = f"{column}_{stat_type}_stats.pkl"
        filepath = os.path.join(self.output_folder, filename)

        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

        # Save to pickle
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(value, f)
            print(f"Saved {stat_type} for {column} to {filepath}")
        except Exception as e:
            print(f"Error saving stats to pickle: {e}")

        # Cache the result
        if column not in self.stats_cache:
            self.stats_cache[column] = {}
        self.stats_cache[column][stat_type] = value

    def load_stats_from_pickle(self, column, stat_type):
        """
        Load statistical results from pickle or cache.
        
        Args:
        - column: Column name
        - stat_type: Type of statistic to load
        
        Returns:
        - Loaded statistical value
        """
        # Check cache first
        if column in self.stats_cache and stat_type in self.stats_cache[column]:
            return self.stats_cache[column][stat_type]

        # Try to load from pickle
        filename = f"{column}_{stat_type}_stats.pkl"
        filepath = os.path.join(self.output_folder, filename)

        try:
            with open(filepath, 'rb') as f:
                value = pickle.load(f)
            
            # Update cache
            if column not in self.stats_cache:
                self.stats_cache[column] = {}
            self.stats_cache[column][stat_type] = value
            
            return value
        except FileNotFoundError:
            print(f"No saved {stat_type} stats found for {column}")
            return None

    def calculate_mean(self, column):
        """
        Calculate and save mean of a specified column.
        """
        self.validate_column(column)
        mean_value = self.data[column].mean()
        print(f"Mean of column '{column}' : {mean_value}")
        
        # Save to pickle
        self.save_stats_to_pickle(column, 'mean', mean_value)
        
        return mean_value

    def calculate_median(self, column):
        """
        Calculate and save median of a specified column.
        """
        self.validate_column(column)
        median_value = self.data[column].median()
        print(f"Median of column '{column}' : {median_value}")
        
        # Save to pickle
        self.save_stats_to_pickle(column, 'median', median_value)
        
        return median_value

    def calculate_std(self, column):
        """
        Calculate and save standard deviation of a specified column.
        """
        self.validate_column(column)
        std_value = self.data[column].std()
        print(f"Standard Deviation of column '{column}' : {std_value}")
        
        # Save to pickle
        self.save_stats_to_pickle(column, 'std', std_value)
        
        return std_value

    # --------------------
    # Probability Utilities
    # --------------------

    def calculate_joint_counts(self, col1, col2):
        """
        Calculate joint counts for two categorical columns.
        """
        self.validate_column(col1)
        self.validate_column(col2)
        prob_value = self.data.groupby([col1, col2]).size().unstack(fill_value=0)
        print(f"Probability is  {prob_value}")
        return prob_value
    
    # --------------------
    # Permutation_Combination Utilities
    # --------------------

    def get_unique_values_count(self, column):
        """
        Get the count of unique values in a column.
        
        Args:
        - column: Name of the column to analyze
        
        Returns:
        - Number of unique values in the column
        """
        self.validate_column(column)
        return len(self.data[column].unique())

    def get_value_frequencies(self, column):
        """
        Get frequency distribution of values in a column.
        
        Args:
        - column: Name of the column to analyze
        
        Returns:
        - Series with value frequencies
        """
        self.validate_column(column)
        return self.data[column].value_counts()

    def factorial(self, n):
        """
        Calculate factorial of a number.
        Utility method for combinatorics calculations.
        
        Args:
        - n: Number to calculate factorial for
        
        Returns:
        - Factorial of n
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("Factorial is only defined for non-negative integers")
        return math.factorial(n)

    # --------------------
    # Vector Operations
    # --------------------

    def base_vector_operation(self, vector1, vector2):
        """
        Abstract method for vector operations. 
        Child classes should implement specific logic.
        """
        raise NotImplementedError("This method should be implemented in child classes.")
    
    def save_results_to_pickle(self, results, filename):
        """
        Save calculation results to a pickle file.
        
        Args:
        - results: Data to be saved (can be DataFrame, Series, or other picklable object)
        - filename: Name of the output pickle file
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        output_path = os.path.join(self.output_folder, filename)
        
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(results, f)
            print(f"Results saved to pickle file: {output_path}")
        except Exception as e:
            print(f"Error saving results to pickle: {e}")
