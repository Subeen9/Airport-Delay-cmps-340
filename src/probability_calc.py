#%% MODULE BEGINS
# module_name = "probability_calc.py"

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Library Imports
import os


# Third-Party Library Imports
import pandas as pd
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
        Override the parent method to calculate the mean and save the result.
        """
        mean_value = super().calculate_mean(column)
        result_data = pd.DataFrame({
            "Statistic": ["Mean"],
            "Column": [column],
            "Value": [mean_value]
        })
        self.save_to_output(f"{column}_mean.csv", result_data)
        return mean_value

    def calculate_median(self, column):
        """
        Override the parent method to calculate the median and save the result.
        """
        median_value = super().calculate_median(column)
        result_data = pd.DataFrame({
            "Statistic": ["Median"],
            "Column": [column],
            "Value": [median_value]
        })
        self.save_to_output(f"{column}_median.csv", result_data)
        return median_value

    def calculate_std(self, column):
        """
        Override the parent method to calculate the standard deviation and save the result.
        """
        std_value = super().calculate_std(column)
        result_data = pd.DataFrame({
            "Statistic": ["Standard Deviation"],
            "Column": [column],
            "Value": [std_value]
        })
        self.save_to_output(f"{column}_std.csv", result_data)
        return std_value

    def calculate_weighted_mean(self, column, weights_column):
        """
        Calculate the weighted mean for a given column using specified weights and save the result.
        
        Args:
        - column (str): Name of the column for which to calculate the weighted mean.
        - weights_column (str): Name of the column containing weights.

        Returns:
        - float: Weighted mean value.
        """
        if self.data is None or self.data.empty:
            raise ValueError("Data is not loaded or is empty.")

        if column not in self.data.columns or weights_column not in self.data.columns:
            raise KeyError(f"Columns '{column}' or '{weights_column}' not found in the dataset.")

        # Calculate weighted mean
        try:
            weights = self.data[weights_column]
            values = self.data[column]
            weighted_mean = (values * weights).sum() / weights.sum()

            # Save result to Output folder
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
        Calculate joint probabilities P(A and B) for all combinations of two columns.
        """
        joint_counts = self.calculate_joint_counts(col1, col2)
        total_samples = self.data.shape[0]
        joint_prob = joint_counts / total_samples
        print(f"Joint Probability Table:\n{joint_prob}")
        self.save_to_output(f"{col1}_{col2}_joint_probability.csv", joint_prob)
        return joint_prob

    def calculate_conditional_probability(self, col1, col2):
        """
        Calculate conditional probabilities P(col1 | col2) for all combinations.
        """
        joint_counts = self.calculate_joint_counts(col1, col2)
        marginal_col2 = joint_counts.sum(axis=1)
        conditional_probs = joint_counts.div(marginal_col2, axis=0).fillna(0)
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
