#!/usr/bin/env python3
"""
Main script to process maintenance log spreadsheets and generate cost analysis
Usage:
    python analyze_maintenance_logs.py <path_to_spreadsheet>
    
Example:
    python analyze_maintenance_logs.py data/uploads/maintenance_logs_2024.xlsx
"""
import sys
import os
from spreadsheet_processor import SpreadsheetProcessor
from cost_analyzer import CostAnalyzer


def main():
    """Main function to run the maintenance log analysis"""
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python analyze_maintenance_logs.py <path_to_spreadsheet>")
        print("\nExample:")
        print("  python analyze_maintenance_logs.py data/uploads/maintenance_logs.xlsx")
        print("  python analyze_maintenance_logs.py data/uploads/maintenance_logs.csv")
        sys.exit(1)
    
    spreadsheet_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(spreadsheet_path):
        print(f"Error: File not found: {spreadsheet_path}")
        sys.exit(1)
    
    print("="*60)
    print("MAINTENANCE LOG COST ANALYSIS")
    print("="*60)
    print(f"Processing file: {spreadsheet_path}\n")
    
    # Step 1: Process the spreadsheet
    processor = SpreadsheetProcessor()
    logs = processor.process_file(spreadsheet_path)
    
    if logs is None or len(logs) == 0:
        print("Error: No logs were successfully processed.")
        sys.exit(1)
    
    print(f"\n✓ Successfully loaded {len(logs)} maintenance logs\n")
    
    # Step 2: Analyze costs
    analyzer = CostAnalyzer()
    analysis_df = analyzer.analyze_logs(logs)
    
    # Step 3: Generate and display summary
    summary = analyzer.generate_summary(analysis_df)
    analyzer.print_summary(summary)
    
    # Step 4: Export results
    output_filename = os.path.splitext(os.path.basename(spreadsheet_path))[0] + "_analysis.xlsx"
    output_path = analyzer.export_analysis(analysis_df, output_filename)
    
    print(f"✓ Analysis complete! Results saved to: {output_path}")
    print("\nThe output Excel file contains three sheets:")
    print("  1. Detailed Analysis - Line-by-line cost breakdown")
    print("  2. Summary - Overall cost savings summary")
    print("  3. By Task Type - Breakdown by maintenance task type")
    

if __name__ == "__main__":
    main()
