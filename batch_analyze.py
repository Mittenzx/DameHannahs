#!/usr/bin/env python3
"""
Batch analyzer - Process multiple maintenance log files and compare them
Usage:
    python batch_analyze.py <file1> <file2> [file3] ...
    
Example:
    python batch_analyze.py data/uploads/Q1_2024.csv data/uploads/Q2_2024.csv
"""
import sys
import os
from spreadsheet_processor import SpreadsheetProcessor
from cost_analyzer import CostAnalyzer
import pandas as pd


def analyze_file(filepath: str, analyzer: CostAnalyzer):
    """Analyze a single file and return summary"""
    processor = SpreadsheetProcessor()
    logs = processor.process_file(filepath)
    
    if logs is None or len(logs) == 0:
        return None
    
    analysis_df = analyzer.analyze_logs(logs)
    summary = analyzer.generate_summary(analysis_df)
    summary['filename'] = os.path.basename(filepath)
    
    return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_analyze.py <file1> <file2> [file3] ...")
        print("\nExample:")
        print("  python batch_analyze.py data/uploads/Q1_2024.csv data/uploads/Q2_2024.csv")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    print("="*80)
    print("BATCH MAINTENANCE LOG ANALYSIS")
    print("="*80)
    print(f"Processing {len(files)} file(s)...\n")
    
    analyzer = CostAnalyzer()
    summaries = []
    
    for filepath in files:
        print(f"Processing: {filepath}")
        if not os.path.exists(filepath):
            print(f"  ❌ File not found, skipping\n")
            continue
        
        summary = analyze_file(filepath, analyzer)
        if summary:
            summaries.append(summary)
            print(f"  ✓ Analyzed {summary['total_tasks']} tasks\n")
        else:
            print(f"  ❌ Failed to process file\n")
    
    if not summaries:
        print("No files were successfully processed.")
        sys.exit(1)
    
    # Create comparison table
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80 + "\n")
    
    # Build comparison dataframe
    comparison_data = []
    for summary in summaries:
        comparison_data.append({
            'File': summary['filename'],
            'Total Tasks': summary['total_tasks'],
            'Total Hours': f"{summary['total_hours']:.2f}",
            'Materials Cost': f"£{summary['total_materials_cost']:.2f}",
            'In-House Cost': f"£{summary['total_inhouse_cost']:.2f}",
            'Contractor Cost': f"£{summary['total_contractor_cost']:.2f}",
            'Total Savings': f"£{summary['total_savings']:.2f}",
            'Avg Savings %': f"{summary['average_savings_percentage']:.2f}%"
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Print the comparison table
    print(df.to_string(index=False))
    print("\n" + "="*80)
    
    # Calculate totals across all files
    total_tasks = sum(s['total_tasks'] for s in summaries)
    total_hours = sum(s['total_hours'] for s in summaries)
    total_materials = sum(s['total_materials_cost'] for s in summaries)
    total_inhouse = sum(s['total_inhouse_cost'] for s in summaries)
    total_contractor = sum(s['total_contractor_cost'] for s in summaries)
    total_savings = sum(s['total_savings'] for s in summaries)
    
    print("\nCOMBINED TOTALS:")
    print(f"  Total Tasks: {total_tasks}")
    print(f"  Total Hours: {total_hours:.2f}")
    print(f"  Total Materials Cost: £{total_materials:.2f}")
    print(f"  Total In-House Cost: £{total_inhouse:.2f}")
    print(f"  Total Contractor Cost: £{total_contractor:.2f}")
    print(f"  TOTAL SAVINGS: £{total_savings:.2f}")
    if total_contractor > 0:
        overall_savings_pct = (total_savings / total_contractor * 100)
        print(f"  Overall Savings Percentage: {overall_savings_pct:.2f}%")
    
    print("="*80 + "\n")
    
    # Export combined analysis
    output_path = os.path.join('data/output', 'batch_comparison_report.xlsx')
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Comparison', index=False)
        
        # Add totals sheet
        totals_df = pd.DataFrame([{
            'Metric': 'Combined Totals',
            'Total Tasks': total_tasks,
            'Total Hours': total_hours,
            'Total Materials Cost': total_materials,
            'Total In-House Cost': total_inhouse,
            'Total Contractor Cost': total_contractor,
            'Total Savings': total_savings,
            'Overall Savings Percentage': total_savings / total_contractor * 100 if total_contractor > 0 else 0
        }])
        totals_df.to_excel(writer, sheet_name='Combined Totals', index=False)
    
    print(f"✓ Comparison report saved to: {output_path}")


if __name__ == "__main__":
    main()
