import seaborn as sns
from .handle_data import DataHandler
import matplotlib.pyplot as plt

class DataVisualizer(DataHandler):
    def __init__(self, config):
        super().__init__(config)
    
    def plot_violin(self, column_name):
        """Visualize the distribution of a column using a violin plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        plt.figure(figsize=(12, 6))
        sns.violinplot(data=self.data_df, x=column_name, palette="muted")
        plt.title(f"Violin Plot of {column_name}")
        plt.xlabel(column_name)
        plt.ylabel("Density")
        plt.show()

    def plot_box(self, column_name):
        """Visualize the distribution of a column using a box plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        if column_name not in self.data_df.columns:
            print(f"Column '{column_name}' not found in the dataset.")
            return

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.data_df, x=column_name, palette="muted")
        plt.title(f"Box Plot of {column_name}")
        plt.xlabel(column_name)
        plt.show()

    def plot_scatter(self, x_column, y_column):
        """Visualize the relationship between two columns using a scatter plot."""
        if self.data_df is None or self.data_df.empty:
            print("Error: No data loaded to visualize.")
            return
        
        if x_column not in self.data_df.columns or y_column not in self.data_df.columns:
            print(f"Columns '{x_column}' or '{y_column}' not found in the dataset.")
            return

        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=self.data_df, x=x_column, y=y_column, hue="carrier_name", palette="tab10")
        plt.title(f"Scatter Plot of {x_column} vs {y_column}")
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
