from .handle_data import DataHandler  
from .handle_csv import DataVisualizer
from .config import DATA_PATH, DEFAULT_COLUMNS  # Import the configuration file


def main():
    config={
        "DATA_PATH": DATA_PATH,
        "DEFAULT_COLUMNS": DEFAULT_COLUMNS
    }
    # Step 1: Initialize the parent class
    parent_handler = DataHandler(config)
    parent_handler.load_data()

    # Step 2: Initialize the child class
    child_visualizer = DataVisualizer(config)
    child_visualizer.data_df = parent_handler.data_df  # Pass loaded data to the child

    while True:
        print("\nAirport Data Analysis Menu:")
        print("1. View carrier frequencies (Parent - visualize_column)")
        print("2. View all delay types comparison (Parent - visualize_delays)")
        print("3. Query arrival delays by carrier (Parent - query_arrival_delays_by_carrier)")
        print("4. View distribution of a column using violin plot (Child - plot_violin)")
        print("5. View distribution of a column using box plot (Child - plot_box)")
        print("6. View relationship between two columns using scatter plot (Child - plot_scatter)")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")
        if choice == "1":
            column = input("Enter the column name (e.g., 'carrier_name'): ")
            parent_handler.visualize_column(column)
        elif choice == "2":
            parent_handler.visualize_delays()
        elif choice == "3":
            parent_handler.query_arrival_delays_by_carrier()
        elif choice == "4":
            column = input("Enter the column name for the violin plot: ")
            child_visualizer.plot_violin(column)
        elif choice == "5":
            column = input("Enter the column name for the box plot: ")
            child_visualizer.plot_box(column)
        elif choice == "6":
            x_col = input("Enter the x-axis column name: ")
            y_col = input("Enter the y-axis column name: ")
            child_visualizer.plot_scatter(x_col, y_col)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
