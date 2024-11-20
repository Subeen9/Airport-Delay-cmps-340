from .handle_data import DataHandler  
from .handle_csv import DataVisualizer
from .config import DATA_PATH, DEFAULT_COLUMNS, region_mapping
from .module_tmp import (
    numpy_to_dataframe,
    DataProcessor,
    calculate_stats,
    PROCESSING_CONFIGS
)
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
            print("8. Convert data to DataFrame (Module tmp)")
            print("9. Calculate Statistics (Module tmp)")
            print("10. Process Data with Lambda (Module tmp)")
            print("11. Exit")

            choice = input("\nEnter your choice (1-11): ")
            
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
                print(filtered_data)
                
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
                numeric_data = child_visualizer.data_df[['arr_delay', 'carrier_delay']].to_numpy()
                new_df = numpy_to_dataframe(numeric_data, columns=['Arrival_Delay', 'Carrier_Delay'])
                print("\nConverted DataFrame:")
                print(new_df.head())
                
            elif choice == "9":
                column = input("Enter column name for statistics (e.g., 'arr_delay'): ")
                if column in child_visualizer.data_df.columns:
                    data = child_visualizer.data_df[column].dropna().tolist()
                    mean = calculate_stats(data, 'mean')
                    median = calculate_stats(data, 'median')
                    print(f"\nStatistics for {column}:")
                    print(f"Mean: {mean:.2f}")
                    print(f"Median: {median:.2f}")
                else:
                    print("Column not found in dataset")
                    
            elif choice == "10":
                processor = DataProcessor()
                column = input("Enter column name (e.g., 'arr_delay'): ")
                if column in child_visualizer.data_df.columns:
                    data = child_visualizer.data_df[column].dropna().tolist()
                    result = processor.process_with_lambda(data)
                    print(f"\nProcessed result: {result:.2f}")
                else:
                    print("Column not found in dataset")
                    
            elif choice == "11":
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