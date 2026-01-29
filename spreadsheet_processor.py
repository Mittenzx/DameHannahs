"""
Spreadsheet Upload and Processing Module
Handles CSV and Excel file uploads and converts them to MaintenanceLog objects
"""
import pandas as pd
from datetime import datetime
from typing import List, Optional
import os
from models import MaintenanceLog
from config import REQUIRED_COLUMNS, OPTIONAL_COLUMNS, UPLOAD_DIR


class SpreadsheetProcessor:
    """
    Handles uploading and processing maintenance log spreadsheets
    """
    
    def __init__(self):
        """Initialize the processor"""
        # Ensure upload directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    def load_spreadsheet(self, filepath: str) -> pd.DataFrame:
        """
        Load a spreadsheet from CSV or Excel format
        
        Args:
            filepath: Path to the spreadsheet file
            
        Returns:
            pandas DataFrame with the data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(filepath)
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Please use CSV or Excel files.")
        
        return df
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        """
        Validate that the DataFrame has all required columns
        Note: This method normalizes column names in place
        
        Args:
            df: pandas DataFrame to validate (modified in place)
            
        Returns:
            True if valid, False otherwise
        """
        # Normalize column names (lowercase, strip whitespace)
        df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
        
        missing_columns = []
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"Error: Missing required columns: {', '.join(missing_columns)}")
            print(f"Required columns are: {', '.join(REQUIRED_COLUMNS)}")
            return False
        
        return True
    
    def parse_logs_from_dataframe(self, df: pd.DataFrame) -> List[MaintenanceLog]:
        """
        Parse MaintenanceLog objects from a DataFrame
        
        Args:
            df: pandas DataFrame with maintenance log data
            
        Returns:
            List of MaintenanceLog objects
        """
        logs = []
        
        for index, row in df.iterrows():
            try:
                # Parse date
                if isinstance(row['date'], str):
                    date = pd.to_datetime(row['date'])
                else:
                    date = row['date']
                
                # Create MaintenanceLog object
                log = MaintenanceLog(
                    date=date,
                    task_type=str(row['task_type']),
                    description=str(row['description']),
                    hours_spent=float(row['hours_spent']),
                    materials_cost=float(row.get('materials_cost', 0.0)),
                    technician_name=str(row['technician_name']) if 'technician_name' in row and pd.notna(row['technician_name']) else None,
                    location=str(row['location']) if 'location' in row and pd.notna(row['location']) else None,
                    priority=str(row['priority']) if 'priority' in row and pd.notna(row['priority']) else None,
                    notes=str(row['notes']) if 'notes' in row and pd.notna(row['notes']) else None
                )
                
                logs.append(log)
                
            except Exception as e:
                print(f"Warning: Error parsing row {index}: {e}")
                continue
        
        return logs
    
    def process_file(self, filepath: str) -> Optional[List[MaintenanceLog]]:
        """
        Complete processing pipeline: load, validate, and parse a spreadsheet
        
        Args:
            filepath: Path to the spreadsheet file
            
        Returns:
            List of MaintenanceLog objects, or None if processing failed
        """
        try:
            print(f"Loading spreadsheet: {filepath}")
            df = self.load_spreadsheet(filepath)
            
            print(f"Loaded {len(df)} rows")
            
            if not self.validate_columns(df):
                return None
            
            print("Columns validated successfully")
            
            logs = self.parse_logs_from_dataframe(df)
            
            print(f"Successfully parsed {len(logs)} maintenance logs")
            
            return logs
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return None
