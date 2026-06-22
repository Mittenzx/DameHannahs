# Project Overview - DameHannahs Maintenance Log Analysis System

## What This System Does

This repository provides a complete solution for:
1. **Uploading maintenance log spreadsheets** (CSV or Excel format)
2. **Calculating cost savings** by comparing in-house maintenance vs contractor rates
3. **Generating detailed reports** with Excel output showing cost breakdowns
4. **Comparing multiple time periods** to track savings over time

## Key Features

✅ **Easy to Use**: Simple command-line interface
✅ **Multiple Formats**: Supports CSV and Excel (.xlsx, .xls)
✅ **Customizable Rates**: Configure hourly rates for your market
✅ **Comprehensive Reports**: Excel output with multiple analysis sheets
✅ **Validation Tools**: Check your data before analysis
✅ **Batch Processing**: Compare multiple time periods side-by-side

## Repository Structure

```
DameHannahs/
├── Core Analysis Scripts
│   ├── analyze_maintenance_logs.py      # Main analysis script
│   ├── analyze_with_custom_rates.py     # Analysis with custom rate files
│   └── batch_analyze.py                 # Compare multiple files
│
├── Utilities
│   └── validate_spreadsheet.py          # Validate spreadsheet format
│
├── Core Modules
│   ├── models.py                        # Data models
│   ├── spreadsheet_processor.py         # File upload & parsing
│   ├── cost_analyzer.py                 # Cost calculation engine
│   └── config.py                        # Configuration settings
│
├── Data Directories
│   ├── data/uploads/                    # Place your spreadsheets here
│   ├── data/output/                     # Analysis results saved here
│   └── data/templates/                  # Sample data & templates
│
├── Documentation
│   ├── README.md                        # Full documentation
│   ├── QUICKSTART.md                    # Quick start guide
│   └── PROJECT_OVERVIEW.md              # This file
│
└── requirements.txt                     # Python dependencies
```

## Usage Examples

### Basic Analysis
```bash
python analyze_maintenance_logs.py data/uploads/maintenance_logs.csv
```

### With Custom Rates
```bash
python analyze_with_custom_rates.py data/uploads/logs.csv \
  --market-rates data/templates/market_rates.json \
  --inhouse-rates data/templates/inhouse_rates.json
```

### Batch Comparison
```bash
python batch_analyze.py \
  data/uploads/Q1_2024.csv \
  data/uploads/Q2_2024.csv \
  data/uploads/Q3_2024.csv
```

### Validate Before Analysis
```bash
python validate_spreadsheet.py data/uploads/my_logs.csv
```

## What Gets Calculated

For each maintenance task, the system calculates:
- **In-house labor cost** = hours × in-house hourly rate
- **Contractor labor cost** = hours × market hourly rate
- **Total in-house cost** = in-house labor + materials
- **Total contractor cost** = contractor labor + materials
- **Cost savings** = contractor total - in-house total
- **Savings percentage** = (savings / contractor total) × 100

## Output Reports

Analysis generates Excel files with three sheets:

1. **Detailed Analysis**: Every task with full cost breakdown
2. **Summary**: Total savings and aggregate statistics
3. **By Task Type**: Savings grouped by maintenance category

## Use Cases

### Monthly/Quarterly Reporting
Track maintenance costs and demonstrate ROI of in-house team:
```bash
python analyze_maintenance_logs.py data/uploads/october_2024.csv
```

### Annual Comparison
Compare savings across multiple quarters:
```bash
python batch_analyze.py data/uploads/Q*.csv
```

### Budget Planning
Use historical data to justify maintenance staff positions by showing cost savings vs hiring contractors.

### Regional Analysis
Customize rates for different locations and compare:
```bash
python analyze_with_custom_rates.py data/uploads/site_A.csv \
  --market-rates data/regional_rates/site_A_market.json \
  --inhouse-rates data/regional_rates/site_A_inhouse.json
```

## Customization

### Changing Default Rates
Edit `config.py` to change default hourly rates:
```python
DEFAULT_MARKET_RATES = {
    "electrician": 85.00,  # Change to your local rate
    "plumber": 90.00,      # etc.
    # ...
}
```

### Adding New Task Types
Add entries to the rate dictionaries in `config.py`:
```python
DEFAULT_MARKET_RATES = {
    # existing types...
    "roofer": 80.00,       # New task type
    "mason": 75.00,        # New task type
}
```

## System Requirements

- Python 3.8 or higher
- Dependencies (auto-installed via pip):
  - pandas >= 2.0.0
  - openpyxl >= 3.1.0
  - xlrd >= 2.0.1
  - numpy >= 1.24.0

## Getting Started

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Try sample data**: `python analyze_maintenance_logs.py data/templates/sample_maintenance_logs.csv`
3. **Prepare your data**: Use `data/templates/maintenance_log_template.csv` as a guide
4. **Run analysis**: `python analyze_maintenance_logs.py data/uploads/your_file.csv`
5. **View results**: Open the Excel file in `data/output/`

## Support & Documentation

- See `README.md` for complete documentation
- See `QUICKSTART.md` for a 5-minute getting started guide
- Sample data available in `data/templates/`
- Template spreadsheet provided for easy data entry

## Extending the System

This system can be extended to support:
- Web interface for file uploads
- Database storage for historical tracking
- Automated email reports
- Dashboard visualizations
- Integration with work order systems
- Mobile app for field data entry
- API for programmatic access

## License & Usage

This project is provided for organizational use in tracking maintenance costs and calculating the financial benefits of in-house maintenance teams versus contractor hiring.
