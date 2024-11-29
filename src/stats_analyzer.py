import pandas as pd
import numpy as np

class AdvanceCalculations:
    def __init__(self, config):
        """
        Initialize the parent class with configurations and data storage.
        """
        self.config = config or {}
        self.data = None  # Placeholder for dataset

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

    def calculate_mean(self, column):
        """
        Calculate the mean of a specified column.
        """
        self.validate_column(column)
        mean_value = self.data[column].mean()
        print(f"Mean of column '{column}' : {mean_value}")
        return mean_value

    def calculate_median(self, column):
        """
        Calculate the median of a specified column.
        """
        self.validate_column(column)
        median_value = self.data[column].median()
        print(f"Median of column '{column}' : {median_value}")
        return median_value

    def calculate_std(self, column):
        """
        Calculate the standard deviation of a specified column.
        """
        self.validate_column(column)
        std_value = self.data[column].std()
        print(f"Standard Deviatian of column '{column}' : {std_value}")
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
    # Vector Operations
    # --------------------

    def base_vector_operation(self, vector1, vector2):
        """
        Abstract method for vector operations. 
        Child classes should implement specific logic.
        """
        raise NotImplementedError("This method should be implemented in child classes.")