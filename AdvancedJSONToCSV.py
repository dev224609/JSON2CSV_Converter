"""Advanced JSON to CSV converter using pandas for better performance."""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime


class AdvancedJSONToCSV:
    """Advanced JSON to CSV converter using pandas."""
    
    def __init__(self, output_directory: str = "advanced_csv_output"):
        """Initialize the advanced converter."""
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
    
    def convert_with_pandas(self, json_file_path: str,
                          target_keys: List[str] = None,
                          nested_key_path: str = None,
                          output_csv_path: str = None) -> str:
        """
        Convert JSON to CSV using pandas for better performance.
        
        Args:
            json_file_path: Path to JSON file
            target_keys: Keys to extract
            nested_key_path: Path to nested data
            output_csv_path: Output CSV path
        
        Returns:
            Path to created CSV file
        """
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract nested data if specified
        if nested_key_path:
            keys = nested_key_path.split('.')
            for key in keys:
                if isinstance(data, dict) and key in data:
                    data = data[key]
                elif isinstance(data, list) and key.isdigit():
                    data = data[int(key)]
                else:
                    raise KeyError(f"Key path '{nested_key_path}' not found")
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.json_normalize(data)
        elif isinstance(data, dict):
            df = pd.json_normalize([data])
        else:
            df = pd.DataFrame([{"value": data}])
        
        # Filter by target keys if specified
        if target_keys:
            available_keys = [key for key in target_keys if key in df.columns]
            df = df[available_keys]
        
        # Generate output path
        if output_csv_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = Path(json_file_path).stem
            output_csv_path = self.output_directory / f"{json_filename}_pandas_{timestamp}.csv"
        
        # Write to CSV
        df.to_csv(output_csv_path, index=False)
        
        return str(output_csv_path)
    
    def convert_with_transformations(self, json_file_path: str,
                                   transformations: Dict[str, callable],
                                   output_csv_path: str = None) -> str:
        """
        Convert JSON to CSV with custom transformations.
        
        Args:
            json_file_path: Path to JSON file
            transformations: Dictionary of column transformations
            output_csv_path: Output CSV path
        
        Returns:
            Path to created CSV file
        """
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.json_normalize(data if isinstance(data, list) else [data])
        
        # Apply transformations
        for column, transform_func in transformations.items():
            if column in df.columns:
                df[column] = df[column].apply(transform_func)
        
        if output_csv_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = Path(json_file_path).stem
            output_csv_path = self.output_directory / f"{json_filename}_transformed_{timestamp}.csv"
        
        df.to_csv(output_csv_path, index=False)
        return str(output_csv_path)