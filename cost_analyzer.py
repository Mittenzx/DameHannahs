"""
Cost Analysis Module
Calculates cost savings comparing in-house maintenance vs contractor rates
"""
from typing import List, Dict, Tuple, Any
import pandas as pd
from models import MaintenanceLog
from config import DEFAULT_MARKET_RATES, DEFAULT_INHOUSE_RATES, OUTPUT_DIR
import os


class CostAnalyzer:
    """
    Analyzes maintenance logs and calculates cost savings
    """
    
    def __init__(
        self,
        market_rates: Dict[str, float] = None,
        inhouse_rates: Dict[str, float] = None
    ):
        """
        Initialize the cost analyzer
        
        Args:
            market_rates: Dictionary of market/contractor rates by task type
            inhouse_rates: Dictionary of in-house rates by task type
        """
        self.market_rates = market_rates or DEFAULT_MARKET_RATES
        self.inhouse_rates = inhouse_rates or DEFAULT_INHOUSE_RATES
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def get_rate(self, task_type: str, rate_dict: Dict[str, float]) -> float:
        """
        Get the hourly rate for a task type, with fallback to 'other'
        
        Args:
            task_type: Type of maintenance task
            rate_dict: Dictionary of rates
            
        Returns:
            Hourly rate for the task type
        """
        task_type = task_type.lower().strip()
        # Use 'other' as fallback if task type not found
        return rate_dict.get(task_type, rate_dict.get('other', 70.00))
    
    def analyze_log(self, log: MaintenanceLog) -> Dict[str, float]:
        """
        Analyze a single maintenance log
        
        Args:
            log: MaintenanceLog object
            
        Returns:
            Dictionary with cost analysis results
        """
        inhouse_rate = self.get_rate(log.task_type, self.inhouse_rates)
        market_rate = self.get_rate(log.task_type, self.market_rates)
        
        inhouse_cost = log.calculate_inhouse_cost(inhouse_rate)
        contractor_cost = log.calculate_contractor_cost(market_rate)
        savings = log.calculate_savings(inhouse_rate, market_rate)
        # Avoid division by zero
        savings_percentage = (savings / contractor_cost * 100) if contractor_cost > 0 else 0.0
        
        return {
            'date': log.date.strftime("%Y-%m-%d"),
            'task_type': log.task_type,
            'description': log.description,
            'hours_spent': log.hours_spent,
            'materials_cost': log.materials_cost,
            'inhouse_hourly_rate': inhouse_rate,
            'market_hourly_rate': market_rate,
            'inhouse_labor_cost': log.hours_spent * inhouse_rate,
            'market_labor_cost': log.hours_spent * market_rate,
            'inhouse_total_cost': inhouse_cost,
            'contractor_total_cost': contractor_cost,
            'cost_savings': savings,
            'savings_percentage': savings_percentage
        }
    
    def analyze_logs(self, logs: List[MaintenanceLog]) -> pd.DataFrame:
        """
        Analyze multiple maintenance logs
        
        Args:
            logs: List of MaintenanceLog objects
            
        Returns:
            pandas DataFrame with analysis results for all logs
        """
        results = [self.analyze_log(log) for log in logs]
        return pd.DataFrame(results)
    
    def generate_summary(self, analysis_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics from analysis results
        
        Args:
            analysis_df: DataFrame with analysis results
            
        Returns:
            Dictionary with summary statistics
        """
        if len(analysis_df) == 0:
            return {
                'total_tasks': 0,
                'total_hours': 0,
                'total_inhouse_cost': 0,
                'total_contractor_cost': 0,
                'total_savings': 0,
                'average_savings_percentage': 0,
                'tasks_by_type': {}
            }
        
        summary = {
            'total_tasks': len(analysis_df),
            'total_hours': analysis_df['hours_spent'].sum(),
            'total_materials_cost': analysis_df['materials_cost'].sum(),
            'total_inhouse_cost': analysis_df['inhouse_total_cost'].sum(),
            'total_contractor_cost': analysis_df['contractor_total_cost'].sum(),
            'total_savings': analysis_df['cost_savings'].sum(),
            'average_savings_percentage': analysis_df['savings_percentage'].mean(),
            'tasks_by_type': analysis_df.groupby('task_type').size().to_dict()
        }
        
        return summary
    
    def export_analysis(self, analysis_df: pd.DataFrame, output_filename: str = "cost_analysis.xlsx"):
        """
        Export analysis results to Excel file
        
        Args:
            analysis_df: DataFrame with analysis results
            output_filename: Name of output file
            
        Returns:
            Path to the exported file
        """
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Create summary
        summary = self.generate_summary(analysis_df)
        
        # Create Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write detailed analysis
            analysis_df.to_excel(writer, sheet_name='Detailed Analysis', index=False)
            
            # Write summary
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Write task type breakdown
            if len(analysis_df) > 0:
                task_summary = analysis_df.groupby('task_type').agg({
                    'hours_spent': 'sum',
                    'materials_cost': 'sum',
                    'inhouse_total_cost': 'sum',
                    'contractor_total_cost': 'sum',
                    'cost_savings': 'sum',
                    'savings_percentage': 'mean'
                }).reset_index()
                task_summary.to_excel(writer, sheet_name='By Task Type', index=False)
        
        print(f"Analysis exported to: {output_path}")
        return output_path
    
    def print_summary(self, summary: Dict[str, Any]):
        """
        Print a formatted summary to console
        
        Args:
            summary: Dictionary with summary statistics
        """
        print("\n" + "="*60)
        print("COST SAVINGS ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total Tasks Analyzed: {summary['total_tasks']}")
        print(f"Total Hours Worked: {summary['total_hours']:.2f}")
        print(f"Total Materials Cost: ${summary['total_materials_cost']:.2f}")
        print(f"\nIn-House Total Cost: ${summary['total_inhouse_cost']:.2f}")
        print(f"Contractor Total Cost: ${summary['total_contractor_cost']:.2f}")
        print(f"\nTOTAL COST SAVINGS: ${summary['total_savings']:.2f}")
        print(f"Average Savings Percentage: {summary['average_savings_percentage']:.2f}%")
        print(f"\nTasks by Type:")
        for task_type, count in summary['tasks_by_type'].items():
            print(f"  - {task_type}: {count} tasks")
        print("="*60 + "\n")
