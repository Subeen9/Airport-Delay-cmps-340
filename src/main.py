#%% MODULE BEGINS
# module_name = "main"

"""
Version: v1.0

Description:
    Main script for the Airport Data Analysis application. Initializes modules, handles user interaction, 
    and provides a menu-driven interface for various analysis functionalities.

Authors: Subin Bista, Aakash Poudel, Niraj Bhatta, Satyam Pathak
    
Date Created: November 13, 2024
Date Last Updated: November 30, 2024


"""

#%% IMPORTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os

#

# Custom imports
from .data_management import DataHandler
from .data_operations import DataVisualizer
from .stats_analyzer import AdvanceCalculations
from .probability_calc import ProbabilityCalculations
from .permutations_combinations import Permutations_Combination_Calculator
from .vector_operations import VectorOperations
from .config import DATA_PATH, OUTPUT_FOLDER

# Standard imports
import logging

#%% CONSTANTS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LOG_FILE = "app.log"

#%% CONFIGURATION   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setup_logging():
    """
    Set up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

#%% FUNCTION DEFINITIONS   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    """
    Main function for the Airport Data Analysis application.
    """
    setup_logging()
    logging.info("Starting the application.")

    # Initialize classes
    try:
        # Parent handler initialization
        parent_handler = DataHandler()
        parent_handler.load_data()

        # Child visualizer initialization
        child_visualizer = DataVisualizer()
        child_visualizer.data_df = parent_handler.data_df

        # Configuration setup for dependent modules
        config = {
            "DATA_PATH": DATA_PATH,
            "OUTPUT_FOLDER": OUTPUT_FOLDER
        }

        # Module-specific initializations
        advance_analysis = AdvanceCalculations(config)
        advance_analysis.load_data()
        probability_calc = ProbabilityCalculations(config)
        probability_calc.load_data()
        vector_ops = VectorOperations(config)
        permutation_combination_calc = Permutations_Combination_Calculator(config)
        permutation_combination_calc.load_data()
        

        logging.info("Data and modules initialized successfully.")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        print("An error occurred during initialization. Exiting.")
        return

    # Main menu loop
    while True:
        try:
            print("\n--- Airport Data Analysis Menu ---")
            print("1. View carrier frequencies (Parent - visualize_column)")
            print("2. View all delay types comparison (Parent - visualize_delays)")
            print("3. Query arrival delays by carrier (Parent - query_arrival_delays_by_carrier)")
            print("4. Query data with condition (Child - query_data)")
            print("5. View distribution of a column using violin plot (Child - plot_violin)")
            print("6. View distribution of a column using box plot (Child - plot_box)")
            print("7. View relationship between two columns using scatter plot (Child - plot_scatter)")
            print("8. Calculate the mean of a column (includes weighted mean)")
            print("9. Calculate the median of a column")
            print("10. Calculate the standard deviation of a column")
            print("11. Perform probability calculations (ProbabilityCalculations)")
            print("12. Perform vector operations")
            print("13. Show delay histogram (Parent - visualize_delay_histogram)")
            print("14. Perform permutation & combination on categorical data")
            print("15. Exit")

            choice = input("\nEnter your choice (1-15): ")
            # Carrier Frequency Calculation. Creates Multiple line plot
            if choice == "1":
                column = input("Enter the column name for carrier frequencies (e.g., 'carrier_name'): ")
                parent_handler.visualize_column(column)
            # Creates single line plot for delay types
            elif choice == "2":
                parent_handler.visualize_delays()
            # Query the delay by airlines.
            elif choice == "3":
                parent_handler.query_arrival_delays_by_carrier()
            # Query data using boolean indexing
            elif choice == "4":
                column = input("Enter the column name to query (e.g., 'arr_delay'): ")
                raw_condition = input("Enter the condition and value (e.g., '> 10'): ").strip()

                condition = raw_condition[0]
                if len(raw_condition) > 1:
                    value = float(raw_condition[1:].strip())
                else:
                    print("Invalid condition format. Please try again.")
                    continue

                filtered_data = child_visualizer.query_data(column, condition, value)
                if not filtered_data.empty:
                    print(filtered_data)
                else:
                    print("No matching data found.")
        # Visualizes with violin plot
            elif choice == "5":
                column = input("Enter the column name for the violin plot (e.g., 'arr_delay'): ")
                child_visualizer.plot_violin(column)
        # Visualizes with box plot
            elif choice == "6":
                column = input("Enter the column name for the box plot (e.g., 'weather_delay'): ")
                child_visualizer.plot_box(column)
        # Visualizes with scatter plot
            elif choice == "7":
                x_col = input("Enter the x-axis column name (e.g., 'arr_delay'): ")
                y_col = input("Enter the y-axis column name (e.g., 'weather_delay'): ")
                child_visualizer.plot_scatter(x_col, y_col)
        #Arithmetic Mean and Weighted Mean Calculation
            elif choice == "8":
                print("\nMean Calculation Options:")
                print("1. Calculate Simple Mean")
                print("2. Calculate Weighted Mean")

                mean_choice = input("Enter your choice (1-2): ")

                if mean_choice == "1":
                    column = input("Enter the column name for simple mean (e.g., 'arr_delay'): ")
                    mean_value = advance_analysis.calculate_mean(column)
                    print(f"Mean of {column}: {mean_value}")

                elif mean_choice == "2":
                    column = input("Enter the column name for weighted mean (e.g., 'arr_delay'): ")
                    weights_column = input("Enter the weights column (e.g., 'weight'): ")
                    weighted_mean = probability_calc.calculate_weighted_mean(column, weights_column)
                    print(f"Weighted Mean of {column} with weights from {weights_column}: {weighted_mean}")

                else:
                    print("Invalid choice. Returning to main menu.")
            # Median Calculation
            elif choice == "9":
                column = input("Enter the column name for median (e.g., 'arr_delay'): ")
                median_value = advance_analysis.calculate_median(column)
                print(f"Median of {column}: {median_value}")
        # Standard Deviation Calculation
            elif choice == "10":
                column = input("Enter the column name for standard deviation (e.g., 'weather_delay'): ")
                std_value = advance_analysis.calculate_std(column)
                print(f"Standard Deviation of {column}: {std_value}")
        # Different Probability Calculation
            elif choice == "11":
                print("\nProbability Calculations Menu:")
                print("1. Calculate Joint Probability")
                print("2. Calculate Conditional Probability")
                print("3. Calculate Joint Counts")
                print("4. Back to Main Menu")

                prob_choice = input("Enter your choice (1-4): ")

                if prob_choice == "1":
                    col1 = input("Enter the first column for joint probability (e.g., 'carrier'): ")
                    col2 = input("Enter the second column for joint probability (e.g., 'arr_delay'): ")
                    joint_prob = probability_calc.calculate_joint_probability(col1, col2)
                    print(joint_prob)

                elif prob_choice == "2":
                    col1 = input("Enter the dependent column for conditional probability (e.g., 'arr_delay'): ")
                    col2 = input("Enter the conditioning column for conditional probability (e.g., 'carrier'): ")
                    conditional_probs = probability_calc.calculate_conditional_probability(col1, col2)
                    print(conditional_probs)

                elif prob_choice == "3":
                    col1 = input("Enter the first column for joint counts (e.g., 'carrier'): ")
                    col2 = input("Enter the second column for joint counts (e.g., 'arr_delay'): ")
                    joint_counts = advance_analysis.calculate_joint_counts(col1, col2)
                    print(joint_counts)

                elif prob_choice == "4":
                    print("Returning to main menu.")

                else:
                    print("Invalid choice. Returning to main menu.")
        # Vector Operations
            if choice == "12":
                try:
                    print("\nAvailable numeric columns:")
                    numeric_columns = vector_ops.data.select_dtypes(include=['number']).columns
                    print(", ".join(numeric_columns))

                    column1 = input("Enter the first numeric column (e.g., 'arr_delay'): ").strip()
                    column2 = input("Enter the second numeric column (e.g., 'arr_flights'): ").strip()

                    if column1 not in numeric_columns or column2 not in numeric_columns:
                        print("Error: One or both columns not found in numeric columns.")
                        continue

                    results, vector1, vector2 = vector_ops.perform_vector_operations(column1, column2)
                    
                    print("\nInput Vectors:")
                    print(f"Vector 1 ({column1}): {vector1}")
                    print(f"Vector 2 ({column2}): {vector2}")
                    
                    print("\nVector Operation Results:")
                    for key, value in results.items():
                        print(f"{key}: {value}")
                
                except Exception as e:
                    print(f"An error occurred during vector operations: {e}")
                    logging.error(f"Vector operations error: {e}")
        # Histogram Visualization
            elif choice == "13":
                print("Available columns for histogram:")
                print(", ".join(child_visualizer.data_df.columns))
                column = input("Enter the column name for the histogram (e.g., 'arr_delay'): ")
                parent_handler.visualize_delay_histogram(column)
                
        # Permuatation and Combination Calculation 
            elif choice == "14":
                print("\nCombinatorics Analysis Menu:")
                print("1. Analyze Categorical Column")
                print("2. Back to Main Menu")

                comb_choice = input("Enter your choice (1-2): ")

                if comb_choice == "1":
                    print("\nAvailable categorical columns:")
                    print(", ".join(permutation_combination_calc.data.select_dtypes(include=['object']).columns))
                    column = input("Enter the categorical column name to analyze: ")
                    
                    # Get unique values and their count
                    unique_values = permutation_combination_calc.get_unique_values_count(column)
                    print(f"\nNumber of unique values in {column}: {unique_values}")
                    print("Unique values:", permutation_combination_calc.data[column].unique())

                    # Calculate permutations and combinations
                    r = int(input("\nEnter r (number of items to select): "))
                    
                    perm_result = permutation_combination_calc.calculate_permutation(unique_values, r)
                    comb_result = permutation_combination_calc.calculate_combination(unique_values, r)
                    
                    print(f"\nResults for column '{column}':")
                    print(f"Permutations P({unique_values},{r}): {perm_result}")
                    print(f"Combinations C({unique_values},{r}): {comb_result}")

                elif comb_choice == "2":
                    print("Returning to main menu.")
                    
                else:
                    print("Invalid choice. Returning to main menu.")

            elif choice == "15":
                logging.info("Exiting the application.")
                print("Goodbye!")
                break

        except Exception as e:  
            logging.error(f"Error occurred: {e}")  
            print(f"An error occurred: {e}")  


if __name__ == "__main__":
    main()











