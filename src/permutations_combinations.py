import os
import pandas as pd
from .stats_analyzer import AdvanceCalculations


class Permutations_Combination_Calculator(AdvanceCalculations):
    """
    Extends AdvanceCalculations to add functionality for permutations and combinations calculations.
    
    Features:
    - Calculates permutations and combinations with and without repetition
    - Handles circular permutations and partial permutations
    - Saves results to output files
    - Supports bulk calculations on dataset columns
    """
    
    def __init__(self, config):
        """
        Initialize the combinatorics calculator with configurations.
        
        Args:
        - config: Dictionary containing configuration (e.g., data path)
        """
        super().__init__(config)
        self.output_folder = "Output"

    def calculate_permutation(self, *args, **kwargs):
        """
        Calculate the number of permutations P(n,r) - ordering matters.
        
        Args:
        - *args: Accepts n, r as positional arguments
        - **kwargs: Accepts named arguments (n=value, r=value)
        
        Returns:
        - Number of possible permutations
        """
        if len(args) == 2:
            n, r = args
        else:
            n = kwargs.get('n')
            r = kwargs.get('r')
            
        if n < r:
            raise ValueError("n must be greater than or equal to r")
        
        result = self.factorial(n) // self.factorial(n - r)
        self._save_result("permutation", n, r, result)
        return result

    def calculate_combination(self, *args, **kwargs):
        """
        Calculate the number of combinations C(n,r) - ordering doesn't matter.
        
        Args:
        - *args: Accepts n, r as positional arguments
        - **kwargs: Accepts named arguments (n=value, r=value)
        
        Returns:
        - Number of possible combinations
        """
        if len(args) == 2:
            n, r = args
        else:
            n = kwargs.get('n')
            r = kwargs.get('r')
            
        if n < r:
            raise ValueError("n must be greater than or equal to r")
        
        result = self.factorial(n) // (self.factorial(r) * self.factorial(n - r))
        self._save_result("combination", n, r, result)
        return result

    def calculate_permutation_with_repetition(self, *args, **kwargs):
        """
        Calculate permutations where repetition is allowed.
        
        Args:
        - *args: Accepts n, r as positional arguments
        - **kwargs: Accepts named arguments (n=value, r=value)
        
        Returns:
        - Number of possible permutations with repetition
        """
        if len(args) == 2:
            n, r = args
        else:
            n = kwargs.get('n')
            r = kwargs.get('r')
            
        result = n ** r
        self._save_result("permutation_with_repetition", n, r, result)
        return result

    def get_unique_values_count(self, column):
        """
        Get the count of unique values in the specified column.

        Args:
        - column: Name of the column to analyze.

        Returns:
        - Count of unique values in the column.
        """
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in the dataset.")
        return self.data[column].nunique()

    def calculate_combination_with_repetition(self, *args, **kwargs):
        """
        Calculate combinations where repetition is allowed.
        
        Args:
        - *args: Accepts n, r as positional arguments
        - **kwargs: Accepts named arguments (n=value, r=value)
        
        Returns:
        - Number of possible combinations with repetition
        """
        if len(args) == 2:
            n, r = args
        else:
            n = kwargs.get('n')
            r = kwargs.get('r')
            
        result = self.factorial(n + r - 1) // (self.factorial(r) * self.factorial(n - 1))
        self._save_result("combination_with_repetition", n, r, result)
        return result

    def calculate_circular_permutation(self, *args, **kwargs):
        """
        Calculate circular permutations (necklace arrangements).
        
        Args:
        - *args: Accepts n as positional argument
        - **kwargs: Accepts named argument (n=value)
        
        Returns:
        - Number of possible circular permutations
        """
        n = args[0] if args else kwargs.get('n')
        
        if n < 1:
            raise ValueError("n must be at least 1")
            
        result = self.factorial(n - 1)
        self._save_result("circular_permutation", n, None, result)
        return result

    def analyze_column_combinations(self, *args, **kwargs):
        """
        Analyze possible combinations of unique values in a column.
        
        Args:
        - *args: Accepts column, r as positional arguments
        - **kwargs: Accepts named arguments (column=value, r=value)
        
        Returns:
        - DataFrame with combination analysis results
        """
        if len(args) == 2:
            column, r = args
        else:
            column = kwargs.get('column')
            r = kwargs.get('r')
            
        self.validate_column(column)
        unique_values = self.get_unique_values_count(column)
        
        results = {
            "Column": column,
            "Unique_Values": unique_values,
            "Combination_Size": r,
            "Simple_Combinations": self.calculate_combination(unique_values, r),
            "Combinations_With_Repetition": self.calculate_combination_with_repetition(unique_values, r)
        }
        
        results_df = pd.DataFrame([results])
        self.save_to_output(f"{column}_combination_analysis.csv", results_df)
        return results_df

    def calculate_permutations_from_frequencies(self, *args, **kwargs):
        """
        Calculate permutations when items have repetitions.
        
        Args:
        - *args: Accepts frequencies as positional argument
        - **kwargs: Accepts frequencies as named argument
        
        Returns:
        - Number of unique permutations
        """
        frequencies = args[0] if args else kwargs.get('frequencies')
        
        if isinstance(frequencies, dict):
            frequencies = list(frequencies.values())
            
        total_items = sum(frequencies)
        denominator = 1
        for freq in frequencies:
            denominator *= self.factorial(freq)
            
        result = self.factorial(total_items) // denominator
        self._save_result("permutation_with_frequencies", total_items, None, result)
        return result

    def _save_result(self, calculation_type, n, r, result):
        """
        Save calculation result to output file.
        
        Args:
        - calculation_type: Type of calculation performed
        - n: First parameter of calculation
        - r: Second parameter of calculation (if applicable)
        - result: Calculated result
        """
        result_data = {
            "Calculation_Type": [calculation_type],
            "n": [n],
            "r": [r] if r is not None else [None],
            "Result": [result]
        }
        
        result_df = pd.DataFrame(result_data)
        filename = f"{calculation_type}_n{n}" + (f"_r{r}" if r is not None else "") + ".csv"
        self.save_to_output(filename, result_df)

    def save_to_output(self, filename, result):
        """
        Save the result to a CSV file in the output folder.
        
        Args:
        - filename: Name of the output file
        - result: DataFrame containing the result to save
        """
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        output_path = os.path.join(self.output_folder, filename)
        result.to_csv(output_path, index=False)
        print(f"Result saved to {output_path}")