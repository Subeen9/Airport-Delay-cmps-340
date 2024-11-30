import os
import pandas as pd
from .stats_analyzer import AdvanceCalculations


class ProbabilityCalculations(AdvanceCalculations):
    """
    Extends AdvanceCalculations to add functionality for saving results to output files.
    
    Features:
    - Calculates mean, median, and standard deviation and saves results.
    - Computes joint probabilities and conditional probabilities for all combinations.
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
