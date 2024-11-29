from .data_management import DataHandler  
from .data_operations import DataVisualizer
from .stats_analyzer import AdvanceCalculations
from .config import DATA_PATH, DEFAULT_COLUMNS, region_mapping
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()
    logging.info("Starting the application.")
    
    config = {
        "DATA_PATH": DATA_PATH,
        "DEFAULT_COLUMNS": DEFAULT_COLUMNS,
        "region_mapping": region_mapping
    }

    # Initialize classes
    parent_handler = DataHandler(config)
    parent_handler.load_data()

    child_visualizer = DataVisualizer(config)
    child_visualizer.data_df = parent_handler.data_df
    
    # 2nd class
    advance_analysis = AdvanceCalculations(config)
    advance_analysis.load_data()

    logging.info("Data loaded successfully.")

    while True:
        try:
            print("\nAirport Data Analysis Menu:")
            print("1. View carrier frequencies (Parent - visualize_column)")
            print("2. View all delay types comparison (Parent - visualize_delays)")
            print("3. Query arrival delays by carrier (Parent - query_arrival_delays_by_carrier)")
            print("4. Query data with condition (Child - query_data)")
            print("5. View distribution of a column using violin plot (Child - plot_violin)")
            print("6. View distribution of a column using box plot (Child - plot_box)")
            print("7. View relationship between two columns using scatter plot (Child - plot_scatter)")
            print("8. Calculate the mean of the column ")
            print("9. Calculate the median of column ")
            print('10. Calulate the standard deviation of column')
            print('11. Calculate the probability calculaton')
            print('12. Perform vector operations')
            print("13. Show delay histogram (Parent - visualize_delay_histogram) ")  
            print("14. Exit")

            choice = input("\nEnter your choice (1-14): ")
            
            if choice == "1":
                column = input("Enter the column name (e.g., 'carrier_name'): ")
                parent_handler.visualize_column(column)
                
            elif choice == "2":
                parent_handler.visualize_delays()
                
            elif choice == "3":
                parent_handler.query_arrival_delays_by_carrier()
                
            elif choice == "4":
                column = input("Enter the column name to query (e.g., 'arr_delay'): ")
                raw_condition = input("Enter the condition and value (e.g., '> 10'): ").strip()
                
                # Parse the condition and value
                condition = raw_condition[0]  # First character is the condition
                if len(raw_condition) > 1:
                    value = float(raw_condition[1:].strip())  # Convert the rest to a number
                else:
                    print("Invalid condition format. Please try again.")
                    continue

                filtered_data = child_visualizer.query_data(column, condition, value)
                if not filtered_data.empty:
                    print(filtered_data)
                else:
                    print("No matching data found.")

            elif choice == "5":
                column = input("Enter the column name for the violin plot: ")
                child_visualizer.plot_violin(column)
                
            elif choice == "6":
                column = input("Enter the column name for the box plot: ")
                child_visualizer.plot_box(column)
                
            elif choice == "7":
                x_col = input("Enter the x-axis column name: ")
                y_col = input("Enter the y-axis column name: ")
                child_visualizer.plot_scatter(x_col, y_col)
            
            elif choice == '8':
                column = input('Enter the column name for mean ')
                advance_analysis.calculate_mean(column)
            
            elif choice == '9':
                column = input('Enter the column name for median ')
                advance_analysis.calculate_median(column)
            
            elif choice == '10':
                column = input('Enter the column name for standard deviation ')
                advance_analysis.calculate_std(column)
            
            elif choice == '11':
                column = input('Enter the first column name for probability ')
                column2 = input ('Enter the second column name for probability ')
                advance_analysis.calculate_joint_counts(column, column2)
            
            elif choice == '12':
                column = input('Enter the first column name for vector ')
                column2 = input ('Enter the second column name for vector ')
                advance_analysis.base_vector_operation(column, column2)
                    
            elif choice == "13":
                # Display available column names for the histogram
                print("Available columns for histogram:")
                print(", ".join(child_visualizer.data_df.columns))  # Print available column names
                column = input("Enter the column name for the histogram (e.g., 'arr_delay'): ")
                parent_handler.visualize_delay_histogram(column)
       
            elif choice == "14":
                logging.info("Exiting the application.")
                print("Goodbye!")
                break
                
            else:
                logging.warning("Invalid choice entered.")
                print("Invalid choice. Please try again.")
                
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
