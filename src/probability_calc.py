#%% MODULE BEGINS
# module_name = "probability_calc.py"

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Library Imports
import os

# Third-Party Library Imports
import pandas as pd
import numpy as np

# Relative Imports
from .stats_analyzer import AdvanceCalculations


class ProbabilityCalculations(AdvanceCalculations):
    """
    Extends AdvanceCalculations to add functionality for saving results to output files.
    
    Features:
    - Calculates mean, median, and standard deviation and saves results.
    - Computes joint probabilities and conditional probabilities for all combinations.
    - Calculates and saves weighted mean.
    """
    def __init__(self, config):
        """
        Initialize the child class with configurations.
        
        Args:
        - config: Dictionary containing configuration (e.g., data path).
        """
        super().__init__(config)
        self.output_folder = "Output"  # Path to save output files

    def calculate_mean(self, column):
        """
        Calculate the mean using saved pickle data if available, otherwise calculate, save, and return it.
        """
        # Attempt to load the mean from the pickle file
        mean_value = self.load_stats_from_pickle(column, 'mean')
        if mean_value is not None:
            print(f"Loaded mean of column '{column}' from pickle: {mean_value}")
        else:
            print(f"Mean not found in pickle. Calculating mean for column '{column}'.")
            mean_value = self.data[column].mean()
            # Save to pickle
            self.save_stats_to_pickle(column, 'mean', mean_value)
        return mean_value

    def calculate_median(self, column):
        """
        Calculate the median using saved pickle data if available, otherwise calculate, save, and return it.
        """
        # Attempt to load the median from the pickle file
        median_value = self.load_stats_from_pickle(column, 'median')
        if median_value is not None:
            print(f"Loaded median of column '{column}' from pickle: {median_value}")
        else:
            print(f"Median not found in pickle. Calculating median for column '{column}'.")
            median_value = self.data[column].median()
            # Save to pickle
            self.save_stats_to_pickle(column, 'median', median_value)
        return median_value

    def calculate_std(self, column):
        """
        Calculate the standard deviation using saved pickle data if available, otherwise calculate, save, and return it.
        """
        # Attempt to load the standard deviation from the pickle file
        std_value = self.load_stats_from_pickle(column, 'std')
        if std_value is not None:
            print(f"Loaded standard deviation of column '{column}' from pickle: {std_value}")
        else:
            print(f"Standard deviation not found in pickle. Calculating standard deviation for column '{column}'.")
            std_value = self.data[column].std()
            # Save to pickle
            self.save_stats_to_pickle(column, 'std', std_value)
        return std_value

    def calculate_weighted_mean(self, column, weights_column):
        """
        Calculate the weighted mean using lambda function and save the result.
        """
        if self.data is None or self.data.empty:
            raise ValueError("Data is not loaded or is empty.")

        if column not in self.data.columns or weights_column not in self.data.columns:
            raise KeyError(f"Columns '{column}' or '{weights_column}' not found in the dataset.")

        try:
            # Using lambda for weighted mean calculation
            weighted_mean_func = lambda v, w: (v * w).sum() / w.sum()
            weighted_mean = weighted_mean_func(self.data[column], self.data[weights_column])

            result_data = pd.DataFrame({
                "Statistic": ["Weighted Mean"],
                "Column": [column],
                "Weights Column": [weights_column],
                "Value": [weighted_mean]
            })

            self.save_to_output(f"{column}_weighted_mean.csv", result_data)
            return weighted_mean
        except Exception as e:
            raise ValueError(f"Error calculating weighted mean: {e}")

    def calculate_joint_probability(self, col1, col2):
        """
        Calculate joint probabilities using eval() for the final calculation.
        """
        joint_counts = self.calculate_joint_counts(col1, col2)
        total_samples = self.data.shape[0]
        # Using eval() for probability calculation
        joint_prob = eval("counts / total", {"counts": joint_counts, "total": total_samples})
        print(f"Joint Probability Table:\n{joint_prob}")
        self.save_to_output(f"{col1}_{col2}_joint_probability.csv", joint_prob)
        return joint_prob

    def calculate_conditional_probability(self, col1, col2):
        """
        Calculate conditional probabilities using lambda for division operation.
        """
        joint_counts = self.calculate_joint_counts(col1, col2)
        marginal_col2 = joint_counts.sum(axis=1)
        # Using lambda for conditional probability calculation
        cond_prob_func = lambda joint, marginal: joint.div(marginal, axis=0).fillna(0)
        conditional_probs = cond_prob_func(joint_counts, marginal_col2)
        print(f"Conditional Probability Table P({col1} | {col2}):\n{conditional_probs}")
        self.save_to_output(f"{col1}_{col2}_conditional_probability.csv", conditional_probs)
        return conditional_probs

    def save_to_output(self, filename, result):
        """
        Save the result to a CSV file in the output folder.
        
        Args:
        - filename: Name of the output file.
        - result: DataFrame containing the result to save.
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        output_path = os.path.join(self.output_folder, filename)
        if isinstance(result, pd.DataFrame):
            result.to_csv(output_path, index=False)
        else:
            raise ValueError("Result must be a DataFrame to save to CSV.")

        print(f"Result saved to {output_path}")
