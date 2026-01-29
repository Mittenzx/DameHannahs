#!/usr/bin/env python3
"""
Spreadsheet validation utility
Checks if your maintenance log spreadsheet has the correct format before analysis
Usage:
    python validate_spreadsheet.py <path_to_spreadsheet>
"""
import sys
import os
from spreadsheet_processor import SpreadsheetProcessor
from config import REQUIRED_COLUMNS, OPTIONAL_COLUMNS


def validate_file(filepath: str):
    """Validate a spreadsheet file"""
    
    print("="*60)
    print("SPREADSHEET VALIDATION")
    print("="*60)
    print(f"Checking file: {filepath}\n")
    
    if not os.path.exists(filepath):
        print("❌ Error: File not found")
        return False
    
    processor = SpreadsheetProcessor()
    
    # Try to load the file
    try:
        df = processor.load_spreadsheet(filepath)
        print(f"✓ File loaded successfully ({len(df)} rows)")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return False
    
    # Normalize column names
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
    
    # Check required columns
    print(f"\nChecking required columns...")
    missing_columns = []
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            print(f"  ✓ {col}")
        else:
            print(f"  ❌ {col} (MISSING)")
            missing_columns.append(col)
    
    # Check optional columns
    print(f"\nOptional columns found:")
    for col in OPTIONAL_COLUMNS:
        if col in df.columns:
            print(f"  ✓ {col}")
    
    # Check for extra columns
    all_expected = REQUIRED_COLUMNS + OPTIONAL_COLUMNS
    extra_columns = [col for col in df.columns if col not in all_expected]
    if extra_columns:
        print(f"\nNote: Extra columns found (will be ignored):")
        for col in extra_columns:
            print(f"  • {col}")
    
    # Validate data types
    print(f"\nValidating data types...")
    
    # Check dates
    try:
        import pandas as pd
        df['date'] = pd.to_datetime(df['date'])
        print(f"  ✓ Dates are valid")
    except Exception as e:
        print(f"  ⚠️  Date format warning: {e}")
        print(f"     Dates should be in YYYY-MM-DD format")
    
    # Check numeric columns
    numeric_issues = []
    if 'hours_spent' in df.columns:
        try:
            df['hours_spent'] = df['hours_spent'].astype(float)
            print(f"  ✓ hours_spent are numeric")
        except:
            numeric_issues.append('hours_spent')
    
    if 'materials_cost' in df.columns:
        try:
            df['materials_cost'] = df['materials_cost'].astype(float)
            print(f"  ✓ materials_cost are numeric")
        except:
            numeric_issues.append('materials_cost')
    
    if numeric_issues:
        for col in numeric_issues:
            print(f"  ❌ {col} contains non-numeric values")
    
    # Check task types
    if 'task_type' in df.columns:
        unique_types = df['task_type'].unique()
        print(f"\nTask types found ({len(unique_types)}):")
        for task_type in unique_types:
            print(f"  • {task_type}")
    
    # Summary
    print("\n" + "="*60)
    if missing_columns:
        print("❌ VALIDATION FAILED")
        print(f"\nMissing required columns: {', '.join(missing_columns)}")
        print("\nPlease add these columns to your spreadsheet.")
        return False
    elif numeric_issues:
        print("⚠️  VALIDATION WARNING")
        print(f"\nSome numeric columns contain invalid values.")
        print("Please check and fix these before running the analysis.")
        return False
    else:
        print("✓ VALIDATION PASSED")
        print("\nYour spreadsheet is ready for analysis!")
        print(f"\nRun: python analyze_maintenance_logs.py {filepath}")
        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_spreadsheet.py <path_to_spreadsheet>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = validate_file(filepath)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
