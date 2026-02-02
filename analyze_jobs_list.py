#!/usr/bin/env python3
"""
Analyze Jobs List with Smart Categorization

Reads the jobstotal.xlsx file, automatically categorizes each job by tradesperson type,
estimates time and costs, and calculates savings from having in-house staff vs
calling out contractors for each job.

Usage:
    python analyze_jobs_list.py <path_to_jobstotal.xlsx>
    
Example:
    python analyze_jobs_list.py jobstotal.xlsx
"""

import sys
import os
import pandas as pd
from smart_categorizer import SmartJobCategorizer, JobCostEstimator
from config import OUTPUT_DIR


def analyze_jobs_list(input_file: str, output_name: str = 'jobs_cost_analysis'):
    """
    Analyze jobs list with smart categorization and cost estimation
    
    Args:
        input_file: Path to jobstotal.xlsx file
        output_name: Base name for output files
    """
    print("="*80)
    print("JOBS LIST COST ANALYSIS - Smart Categorization")
    print("="*80)
    print(f"Reading jobs from: {input_file}\n")
    
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name='jobslist')
    print(f"Loaded {len(df)} jobs")
    
    # Filter to completed jobs
    df_complete = df[df['status'] == 'Complete'].copy()
    print(f"Analyzing {len(df_complete)} completed jobs")
    
    # Initialize categorizer and estimator
    categorizer = SmartJobCategorizer()
    estimator = JobCostEstimator()
    
    # Analyze each job
    results = []
    print("\nCategorizing and estimating costs...")
    
    for idx, row in df_complete.iterrows():
        # Categorize the job
        task_type = categorizer.categorize_job(
            title=row.get('title'),
            category=row.get('category'),
            description=row.get('notes')
        )
        
        # Estimate costs
        hours, materials, contractor_total, inhouse_total = estimator.estimate_job_cost(task_type)
        savings = contractor_total - inhouse_total
        savings_pct = (savings / contractor_total * 100) if contractor_total > 0 else 0
        
        # Get job details
        job_no = row.get('jobno', 'Unknown')
        title = row.get('title', 'No title')
        resolved_date = row.get('resolved', row.get('created', 'Unknown'))
        location = row.get('location', '')
        
        results.append({
            'job_number': job_no,
            'date': resolved_date,
            'title': title,
            'original_category': row.get('category', ''),
            'task_type': task_type,
            'location': location,
            'estimated_hours': hours,
            'estimated_materials': materials,
            'contractor_total': contractor_total,
            'inhouse_total': inhouse_total,
            'savings': savings,
            'savings_percentage': savings_pct
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Generate summary
    summary = {
        'total_jobs': len(results_df),
        'total_estimated_hours': results_df['estimated_hours'].sum(),
        'total_materials_cost': results_df['estimated_materials'].sum(),
        'total_contractor_cost': results_df['contractor_total'].sum(),
        'total_inhouse_cost': results_df['inhouse_total'].sum(),
        'total_savings': results_df['savings'].sum(),
        'average_savings_pct': results_df['savings_percentage'].mean(),
    }
    
    # Print summary
    print_summary(summary, results_df)
    
    # Export to Excel
    output_file = export_results(results_df, summary, output_name)
    
    print(f"\n✓ Analysis complete!")
    print(f"Results saved to: {output_file}")
    print(f"\nThe Excel file contains:")
    print(f"  1. Summary - Overall cost savings")
    print(f"  2. Detailed Analysis - Every job with cost breakdown")
    print(f"  3. By Task Type - Savings grouped by tradesperson")
    print(f"  4. By Year - Annual savings trends")
    
    return results_df, summary


def print_summary(summary: dict, results_df: pd.DataFrame):
    """Print formatted summary to console"""
    print("\n" + "="*80)
    print("COST SAVINGS SUMMARY")
    print("="*80)
    print(f"Total Jobs Analyzed: {summary['total_jobs']:,}")
    print(f"Estimated Total Hours: {summary['total_estimated_hours']:,.1f}")
    print(f"Estimated Materials Cost: ${summary['total_materials_cost']:,.2f}")
    print()
    print(f"Total Contractor Cost: ${summary['total_contractor_cost']:,.2f}")
    print(f"  (includes callout fees + hourly rates + materials)")
    print(f"Total In-House Cost: ${summary['total_inhouse_cost']:,.2f}")
    print(f"  (hourly rates + materials, no callout fees)")
    print()
    print(f"💰 TOTAL SAVINGS: ${summary['total_savings']:,.2f}")
    print(f"📊 Average Savings: {summary['average_savings_pct']:.1f}%")
    print()
    
    # Show breakdown by task type
    print("Breakdown by Tradesperson Type:")
    print("-" * 80)
    by_type = results_df.groupby('task_type').agg({
        'job_number': 'count',
        'savings': 'sum'
    }).sort_values('savings', ascending=False)
    
    for task_type, row in by_type.iterrows():
        jobs = int(row['job_number'])
        savings = row['savings']
        print(f"  {task_type:20s}: {jobs:4d} jobs → ${savings:10,.2f} saved")
    
    print("="*80)


def export_results(results_df: pd.DataFrame, summary: dict, output_name: str):
    """Export results to Excel file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"{output_name}.xlsx")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Summary sheet
        summary_df = pd.DataFrame([summary])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed analysis
        results_df.to_excel(writer, sheet_name='Detailed Analysis', index=False)
        
        # By task type
        by_type = results_df.groupby('task_type').agg({
            'job_number': 'count',
            'estimated_hours': 'sum',
            'estimated_materials': 'sum',
            'contractor_total': 'sum',
            'inhouse_total': 'sum',
            'savings': 'sum',
            'savings_percentage': 'mean'
        }).reset_index()
        by_type.columns = ['Task Type', 'Number of Jobs', 'Total Hours', 'Total Materials',
                          'Contractor Cost', 'In-House Cost', 'Total Savings', 'Avg Savings %']
        by_type.to_excel(writer, sheet_name='By Task Type', index=False)
        
        # Try to extract year from date and group by year
        try:
            results_df['year'] = pd.to_datetime(results_df['date'], format='%d/%m/%Y', errors='coerce').dt.year
            by_year = results_df.groupby('year').agg({
                'job_number': 'count',
                'savings': 'sum'
            }).reset_index()
            by_year.columns = ['Year', 'Number of Jobs', 'Total Savings']
            by_year.to_excel(writer, sheet_name='By Year', index=False)
        except:
            pass  # Skip if date parsing fails
    
    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_jobs_list.py <path_to_jobstotal.xlsx>")
        print("\nExample:")
        print("  python analyze_jobs_list.py jobstotal.xlsx")
        print("  python analyze_jobs_list.py data/uploads/jobstotal.xlsx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Get output name from input filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_name = f"{base_name}_cost_analysis"
    
    analyze_jobs_list(input_file, output_name)


if __name__ == "__main__":
    main()
