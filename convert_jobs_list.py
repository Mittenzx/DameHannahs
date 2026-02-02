"""
Job List Converter - Convert jobstotal.xlsx format to maintenance log format

This utility helps convert the jobs list data from jobstotal.xlsx into the format
required by the maintenance log analysis system.

The jobs list has:
- jobno, title, created, resolved, category, urgency, status, location, etc.

The analysis system needs:
- date, task_type, description, hours_spent, materials_cost

This script will help you prepare your data for cost analysis.
"""

import pandas as pd
import sys
import os


# Category mapping from jobs list to task types
CATEGORY_MAPPING = {
    'Electrical': 'electrician',
    'Plumbing': 'plumber',
    'Equipment': 'hvac_technician',  # Assuming equipment maintenance
    'Assembly': 'carpenter',
    'Decorative': 'painter',
    'Groundwork': 'landscaper',
    'Fire Safety': 'other',
    'Trust Vehicle': 'other',
    'Disposal': 'other',
    'Move': 'general_handyman',
    'Other': 'other',
}


def convert_jobs_list(input_file: str, output_file: str, default_hours: float = 2.0, default_materials: float = 50.0):
    """
    Convert jobs list format to maintenance log format
    
    Args:
        input_file: Path to jobstotal.xlsx file
        output_file: Path to output CSV file
        default_hours: Default hours if not specified (used for estimation)
        default_materials: Default materials cost if not specified
    """
    print(f"Reading jobs list from: {input_file}")
    
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name='jobslist')
    
    print(f"Loaded {len(df)} jobs")
    
    # Filter to completed jobs only (those with resolved dates)
    df_complete = df[df['status'] == 'Complete'].copy()
    print(f"Found {len(df_complete)} completed jobs")
    
    # Convert to maintenance log format
    maintenance_logs = []
    
    for idx, row in df_complete.iterrows():
        # Use resolved date, fall back to created date
        date = row['resolved'] if pd.notna(row['resolved']) else row['created']
        
        # Map category to task_type
        category = row['category'] if pd.notna(row['category']) else 'Other'
        task_type = CATEGORY_MAPPING.get(category, 'other')
        
        # Description from title
        description = row['title'] if pd.notna(row['title']) else 'No description'
        
        # Add job number to description for reference
        if pd.notna(row['jobno']):
            description = f"{row['jobno']}: {description}"
        
        # Default hours and materials (you should update these with actual data)
        hours_spent = default_hours
        materials_cost = default_materials
        
        # Optional fields
        location = row['location'] if pd.notna(row['location']) else None
        notes = row['notes'] if pd.notna(row['notes']) else None
        urgency = row['urgency'] if pd.notna(row['urgency']) else None
        
        maintenance_logs.append({
            'date': date,
            'task_type': task_type,
            'description': description,
            'hours_spent': hours_spent,
            'materials_cost': materials_cost,
            'technician_name': row['closedby'] if pd.notna(row.get('closedby')) else None,
            'location': location,
            'priority': urgency,
            'notes': notes
        })
    
    # Create output DataFrame
    output_df = pd.DataFrame(maintenance_logs)
    
    # Save to CSV
    output_df.to_csv(output_file, index=False)
    
    print(f"\nConverted {len(output_df)} jobs to maintenance log format")
    print(f"Saved to: {output_file}")
    
    # Show summary
    print("\nTask type distribution:")
    print(output_df['task_type'].value_counts())
    
    print("\n⚠️  IMPORTANT: This conversion uses default values for hours_spent and materials_cost")
    print("   You should update the CSV file with actual time and cost data for accurate analysis.")
    print("\n   Default values used:")
    print(f"   - hours_spent: {default_hours} hours per job")
    print(f"   - materials_cost: ${default_materials:.2f} per job")
    

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_jobs_list.py <input_file> [output_file]")
        print("\nExample:")
        print("  python convert_jobs_list.py jobstotal.xlsx converted_maintenance_logs.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'converted_maintenance_logs.csv'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    convert_jobs_list(input_file, output_file)
    
    print(f"\nNext steps:")
    print(f"1. Open {output_file} in Excel or a text editor")
    print(f"2. Update the hours_spent and materials_cost columns with actual data")
    print(f"3. Run the analysis: python analyze_maintenance_logs.py {output_file}")


if __name__ == "__main__":
    main()
