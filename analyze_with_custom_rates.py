#!/usr/bin/env python3
"""
Advanced maintenance log analysis with custom rate configuration
Usage:
    python analyze_with_custom_rates.py <spreadsheet> [--market-rates-file <file>] [--inhouse-rates-file <file>]
"""
import sys
import argparse
import json
from spreadsheet_processor import SpreadsheetProcessor
from cost_analyzer import CostAnalyzer


def load_rates_from_json(filepath: str) -> dict:
    """Load custom rates from a JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading rates from {filepath}: {e}")
        sys.exit(1)


def main():
    """Main function with custom rates support"""
    parser = argparse.ArgumentParser(
        description="Analyze maintenance logs with optional custom rates"
    )
    parser.add_argument(
        'spreadsheet',
        help='Path to the maintenance log spreadsheet (CSV or Excel)'
    )
    parser.add_argument(
        '--market-rates',
        help='Path to JSON file with custom market/contractor rates',
        default=None
    )
    parser.add_argument(
        '--inhouse-rates',
        help='Path to JSON file with custom in-house rates',
        default=None
    )
    parser.add_argument(
        '--output-name',
        help='Custom name for the output file (without extension)',
        default=None
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("MAINTENANCE LOG COST ANALYSIS (Advanced)")
    print("="*60)
    print(f"Processing file: {args.spreadsheet}\n")
    
    # Load custom rates if provided
    market_rates = None
    inhouse_rates = None
    
    if args.market_rates:
        print(f"Loading custom market rates from: {args.market_rates}")
        market_rates = load_rates_from_json(args.market_rates)
    
    if args.inhouse_rates:
        print(f"Loading custom in-house rates from: {args.inhouse_rates}")
        inhouse_rates = load_rates_from_json(args.inhouse_rates)
    
    # Process spreadsheet
    processor = SpreadsheetProcessor()
    logs = processor.process_file(args.spreadsheet)
    
    if logs is None or len(logs) == 0:
        print("Error: No logs were successfully processed.")
        sys.exit(1)
    
    print(f"\n✓ Successfully loaded {len(logs)} maintenance logs\n")
    
    # Analyze with custom rates
    analyzer = CostAnalyzer(market_rates=market_rates, inhouse_rates=inhouse_rates)
    analysis_df = analyzer.analyze_logs(logs)
    
    # Generate and display summary
    summary = analyzer.generate_summary(analysis_df)
    analyzer.print_summary(summary)
    
    # Export results
    if args.output_name:
        output_filename = args.output_name + ".xlsx"
    else:
        import os
        output_filename = os.path.splitext(os.path.basename(args.spreadsheet))[0] + "_analysis.xlsx"
    
    output_path = analyzer.export_analysis(analysis_df, output_filename)
    
    print(f"✓ Analysis complete! Results saved to: {output_path}")


if __name__ == "__main__":
    main()
