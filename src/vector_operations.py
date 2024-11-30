import numpy as np # type: ignore
import os
import pandas as pd # type: ignore
from .stats_analyzer import AdvanceCalculations


class VectorOperations(AdvanceCalculations):
    """
    Extends AdvanceCalculations to add functionality for vector operations.
    
    Features:
    - Perform operations such as addition, subtraction, dot product, cross product, and other advanced vector operations.
    """
    def __init__(self, config):
        """Initialize with configuration and set up output folder."""
        super().__init__(config)
        self.output_folder = "Output"
        self.data = None
        self.load_data()

    def load_data(self):
        """Load data from the configured path."""
        try:
            self.data = pd.read_csv(self.config["DATA_PATH"])
            return self.data
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def validate_vectors(self, vector1, vector2):
        """Validate vectors before operations."""
        if len(vector1) != len(vector2):
            min_length = min(len(vector1), len(vector2))
            vector1 = vector1[:min_length]
            vector2 = vector2[:min_length]
        return vector1, vector2

    def perform_vector_operations(self, column1, column2):
        """
        Perform various vector operations on two columns.
        
        Args:
            column1 (str): Name of first column
            column2 (str): Name of second column
            
        Returns:
            tuple: (results_dict, vector1, vector2)
        """
        try:
            # Validate columns exist in dataset
            if column1 not in self.data.columns or column2 not in self.data.columns:
                raise ValueError(f"Column not found: {column1 if column1 not in self.data.columns else column2}")

            # Get vectors and handle NaN values
            vector1 = self.data[column1].fillna(0).to_numpy()
            vector2 = self.data[column2].fillna(0).to_numpy()

            # Validate and adjust vectors
            vector1, vector2 = self.validate_vectors(vector1, vector2)

            # Perform calculations
            results = {
                "Addition": vector1 + vector2,
                "Subtraction": vector1 - vector2,
                "Dot Product": float(np.dot(vector1, vector2)),
                "Element-wise Multiplication": vector1 * vector2,
                "Vector 1 Magnitude": float(np.linalg.norm(vector1)),
                "Vector 2 Magnitude": float(np.linalg.norm(vector2))
            }

            # Calculate angle between vectors
            angle = self.calculate_angle_between_vectors(vector1, vector2)
            results["Angle (radians)"] = float(angle)
            results["Angle (degrees)"] = float(np.degrees(angle))

            # Check orthogonality
            results["Orthogonal"] = self.check_for_orthogonality(vector1, vector2)

            # Save results
            self._save_results_to_csv(column1, column2, results)

            # Return first 5 elements for display
            display_results = {k: v[:5].tolist() if isinstance(v, np.ndarray) else v 
                             for k, v in results.items()}
            
            return display_results, vector1[:5].tolist(), vector2[:5].tolist()

        except Exception as e:
            raise RuntimeError(f"Error during vector operations: {e}")

    def obtain_position_vector(self, origin, point):
        """Calculate position vector from origin to point."""
        try:
            return np.array(point) - np.array(origin)
        except Exception as e:
            raise ValueError(f"Error calculating position vector: {e}")

    def obtain_unit_vector(self, vector):
        """Calculate unit vector."""
        try:
            norm = np.linalg.norm(vector)
            if np.isclose(norm, 0):
                raise ValueError("Zero vector cannot have a unit vector.")
            return vector / norm
        except Exception as e:
            raise ValueError(f"Error calculating unit vector: {e}")

    def obtain_projection_vector(self, vector, onto_vector):
        """Calculate vector projection."""
        try:
            dot_product = np.dot(onto_vector, onto_vector)
            if np.isclose(dot_product, 0):
                raise ValueError("Cannot project onto zero vector.")
            return (np.dot(vector, onto_vector) / dot_product) * onto_vector
        except Exception as e:
            raise ValueError(f"Error calculating projection vector: {e}")

    def calculate_angle_between_vectors(self, vector1, vector2):
        """Calculate angle between vectors in radians."""
        try:
            dot_product = np.dot(vector1, vector2)
            norms = np.linalg.norm(vector1) * np.linalg.norm(vector2)
            
            if np.isclose(norms, 0):
                raise ValueError("Cannot calculate angle with zero vector.")
                
            cosine_angle = dot_product / norms
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
            return np.arccos(cosine_angle)
        except Exception as e:
            raise ValueError(f"Error calculating angle: {e}")

    def check_for_orthogonality(self, vector1, vector2):
        """Check if vectors are orthogonal."""
        try:
            return np.isclose(np.dot(vector1, vector2), 0)
        except Exception as e:
            raise ValueError(f"Error checking orthogonality: {e}")

    def _save_results_to_csv(self, column1, column2, results):
        """Save results to CSV file."""
        try:
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)

            # Prepare results for saving
            df_results = pd.DataFrame({
                "Operation": list(results.keys()),
                "Result": [str(results[key]) for key in results]
            })

            # Save to file
            output_path = os.path.join(self.output_folder, 
                                     f"{column1}_{column2}_vector_operations.csv")
            df_results.to_csv(output_path, index=False)
            print(f"Results saved to {output_path}")
            
        except Exception as e:
            print(f"Warning: Could not save results to file: {e}")