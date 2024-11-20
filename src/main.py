from .handle_data import DataHandler  
from .handle_csv import DataVisualizer
from .config import DATA_PATH, DEFAULT_COLUMNS,region_mapping  # Import the configuration file
import logging

# Set up logging configuration
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Log level (can be INFO, DEBUG, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file named app.log
            logging.StreamHandler()          # Log to the console
        ]
    )

# Example usage in the main function
def main():
    setup_logging()  # Initialize logging

    # Log some information
    logging.info("Starting the application.")
    
    config = {
        "DATA_PATH": DATA_PATH,
        "DEFAULT_COLUMNS": DEFAULT_COLUMNS,
        "region_mapping": region_mapping
    }

    # Step 1: Initialize the parent class
    parent_handler = DataHandler(config)
    parent_handler.load_data()

    # Step 2: Initialize the child class
    child_visualizer = DataVisualizer(config)
    child_visualizer.data_df = parent_handler.data_df  # Pass loaded data to the child

    logging.info("Data loaded successfully.")

    while True:
        try:
            print("\nAirport Data Analysis Menu:")
            print("1. View carrier frequencies (Parent - visualize_column)")
            print("2. View all delay types comparison (Parent - visualize_delays)")
            print("3. Query arrival delays by carrier (Parent - query_arrival_delays_by_carrier)")
            print("4. Query data with condition (Child - query_data)")  # New option
            print("5. View distribution of a column using violin plot (Child - plot_violin)")
            print("6. View distribution of a column using box plot (Child - plot_box)")
            print("7. View relationship between two columns using scatter plot (Child - plot_scatter)")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ")
            if choice == "1":
                column = input("Enter the column name (e.g., 'carrier_name'): ")
                parent_handler.visualize_column(column)
            elif choice == "2":
                parent_handler.visualize_delays()
            elif choice == "3":
                parent_handler.query_arrival_delays_by_carrier()
            elif choice == "4":
                column = input("Enter the column name to query (e.g., 'arr_delay'): ")
                condition = input("Enter the condition (e.g., '> 10'): ")
                filtered_data = child_visualizer.query_data(column, condition)
                logging.info(f"Filtered data based on condition '{condition}' for column '{column}'")
                print(filtered_data)  # Display the filtered data
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
            elif choice == "8":
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
