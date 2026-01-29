# DameHannahs - Maintenance Log Cost Analysis System

A Python-based system for uploading maintenance log spreadsheets and quantifying cost savings by comparing in-house maintenance costs versus contractor/market rates.

## 🎯 Purpose

This system helps organizations:
- Track maintenance activities through spreadsheet uploads (CSV/Excel)
- Calculate cost savings from in-house maintenance vs. hiring contractors
- Compare actual costs against market rates for different types of maintenance work
- Generate detailed cost analysis reports
- Quantify the value of having in-house maintenance teams

## 📋 Features

- ✅ **Spreadsheet Upload**: Support for CSV and Excel (.xlsx, .xls) files
- ✅ **Cost Calculation**: Automatic calculation of in-house vs. contractor costs
- ✅ **Multiple Task Types**: Support for various maintenance categories (electrician, plumber, HVAC, carpenter, etc.)
- ✅ **Detailed Reports**: Export comprehensive analysis to Excel with multiple sheets
- ✅ **Summary Statistics**: Total savings, percentage savings, breakdown by task type
- ✅ **Flexible Configuration**: Customizable hourly rates for different markets

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Mittenzx/DameHannahs.git
cd DameHannahs
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

1. **Prepare your maintenance log spreadsheet** with the following required columns:
   - `date` - Date of the maintenance task (YYYY-MM-DD format)
   - `task_type` - Type of maintenance (e.g., electrician, plumber, hvac_technician)
   - `description` - Brief description of the work performed
   - `hours_spent` - Number of hours spent on the task
   - `materials_cost` - Cost of materials used (in USD)

   Optional columns:
   - `technician_name` - Name of the person who performed the work
   - `location` - Where the work was performed
   - `priority` - Priority level (High, Medium, Low)
   - `notes` - Additional notes or comments

2. **Place your spreadsheet** in the `data/uploads/` directory

3. **Run the analysis**:
```bash
python analyze_maintenance_logs.py data/uploads/your_maintenance_logs.xlsx
```

4. **View results** in the `data/output/` directory

### Example

Try the sample data included in the repository:
```bash
python analyze_maintenance_logs.py data/templates/sample_maintenance_logs.csv
```

This will generate a detailed cost analysis report showing savings from in-house maintenance.

## 📊 Understanding the Output

The analysis generates an Excel file with three sheets:

1. **Detailed Analysis**: Line-by-line breakdown showing:
   - In-house vs. contractor costs for each task
   - Labor costs and material costs separately
   - Cost savings per task
   - Savings percentage

2. **Summary**: Overall statistics including:
   - Total number of tasks
   - Total hours worked
   - Total in-house cost vs. contractor cost
   - Total cost savings
   - Average savings percentage

3. **By Task Type**: Breakdown showing:
   - Costs and savings grouped by maintenance category
   - Helps identify which types of work provide the most savings

## ⚙️ Configuration

### Customizing Hourly Rates

Edit `config.py` to adjust the hourly rates for your market:

```python
# Market/Contractor rates (per hour in USD)
DEFAULT_MARKET_RATES = {
    "electrician": 85.00,
    "plumber": 90.00,
    "hvac_technician": 95.00,
    # ... add more task types
}

# In-house rates (per hour in USD)
DEFAULT_INHOUSE_RATES = {
    "electrician": 45.00,
    "plumber": 48.00,
    "hvac_technician": 50.00,
    # ... add more task types
}
```

### Supported Task Types

The system recognizes the following task types by default:
- `electrician` - Electrical work
- `plumber` - Plumbing work
- `hvac_technician` - Heating, ventilation, and air conditioning
- `carpenter` - Carpentry and woodwork
- `general_handyman` - General maintenance tasks
- `painter` - Painting work
- `landscaper` - Landscaping and grounds maintenance
- `other` - Any other maintenance tasks

Tasks not matching these categories will use the "other" rate.

## 📁 Project Structure

```
DameHannahs/
├── analyze_maintenance_logs.py  # Main script to run analysis
├── config.py                    # Configuration and rate settings
├── models.py                    # Data models for maintenance logs
├── spreadsheet_processor.py     # Spreadsheet upload and parsing
├── cost_analyzer.py             # Cost calculation and analysis
├── requirements.txt             # Python dependencies
├── data/
│   ├── uploads/                 # Place your spreadsheets here
│   ├── output/                  # Analysis results are saved here
│   └── templates/               # Sample data and templates
│       └── sample_maintenance_logs.csv
└── README.md                    # This file
```

## 🔍 Example Analysis

Here's what a typical analysis might show:

```
COST SAVINGS ANALYSIS SUMMARY
============================================================
Total Tasks Analyzed: 15
Total Hours Worked: 34.50
Total Materials Cost: $1,605.00

In-House Total Cost: $3,069.00
Contractor Total Cost: $4,447.50

TOTAL COST SAVINGS: $1,378.50
Average Savings Percentage: 31.02%

Tasks by Type:
  - electrician: 5 tasks
  - plumber: 3 tasks
  - hvac_technician: 2 tasks
  - carpenter: 2 tasks
  - general_handyman: 2 tasks
  - painter: 1 task
============================================================
```

## 🤝 Contributing

This system can be extended to support:
- Additional task types and categories
- Different rate structures (by region, by skill level)
- Time-based rate changes
- Integration with other maintenance management systems
- Custom reporting formats

## 📝 License

This project is provided as-is for organizational use in tracking maintenance costs and calculating savings.

## 📧 Support

For questions or issues, please open an issue on the GitHub repository.