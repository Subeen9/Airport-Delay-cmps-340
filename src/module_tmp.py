"""
Module containing utility functions and common methods for data analysis
"""
import pandas as pd
import numpy as np
from typing import Any, List, Dict, Union, Callable

# Global variables with proper suffix as required
VALID_OPERATIONS_gl = ['mean', 'median', 'sum']
DEFAULT_FILL_VALUE_gl = -999

# Configuration constants in dictionary as required
PROCESSING_CONFIGS = {
    'numeric_precision': 2,
    'missing_value_fill': DEFAULT_FILL_VALUE_gl,
    'categorical_max_unique': 50
}

def process_data(*args, **kwargs) -> Any:
    """Demonstrates *args, **kwargs, and nonlocal variable usage"""
    def inner_processor():
        nonlocal process_count
        process_count += 1
        return process_count
    
    process_count = 0  # nonlocal variable demo
    return inner_processor()

def numpy_to_dataframe(array: np.ndarray, **kwargs) -> pd.DataFrame:
    """Convert mxn Numpy array to DataFrame (required functionality)"""
    try:
        n_columns = array.shape[1] if len(array.shape) > 1 else 1
        columns = kwargs.get('columns', [f'col_{i}' for i in range(n_columns)])
        return pd.DataFrame(array, columns=columns)
    except Exception as e:
        print(f"Error converting array: {e}")
        return pd.DataFrame()

class DataProcessor:
    """Class demonstrating private variables and lambda functions"""
    def __init__(self):
        self._private_data = None  # private-like variable
        
    def process_with_lambda(self, data: List[float]) -> float:
        """Using lambda function as required"""
        calculator = lambda x: sum(x) / len(x) if len(x) > 0 else 0
        return calculator(data)

    def evaluate_expression(self, expr: str) -> Callable:
        """Using eval() as required"""
        return eval(f"lambda x: {expr}")

def calculate_stats(data: List[float], method: str = 'mean') -> float:
    """Function with default argument as required"""
    if not data:
        return 0.0
    
    if method == 'mean':
        return sum(data) / len(data)
    elif method == 'median':
        sorted_data = sorted(data)
        mid = len(sorted_data) // 2
        return sorted_data[mid]
    return 0.0