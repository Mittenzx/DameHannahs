# Quick Start Guide - DameHannahs Maintenance Log Analysis

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Try the Sample Data
Run the analysis on the included sample data:
```bash
python analyze_maintenance_logs.py data/templates/sample_maintenance_logs.csv
```

You should see output like this:
```
COST SAVINGS ANALYSIS SUMMARY
============================================================
Total Tasks Analyzed: 15
Total Hours Worked: 34.50
Total Materials Cost: $1605.00

In-House Total Cost: $3036.00
Contractor Total Cost: $4255.00

TOTAL COST SAVINGS: $1219.00
Average Savings Percentage: 30.19%
```

### 3. Check the Results
Open the Excel file created in `data/output/` to see the detailed breakdown.

### 4. Use Your Own Data

#### Option A: Use the Template
1. Copy `data/templates/maintenance_log_template.csv`
2. Fill in your maintenance data
3. Save it in `data/uploads/`
4. Run: `python analyze_maintenance_logs.py data/uploads/your_file.csv`

#### Option B: Prepare Your Spreadsheet
Your spreadsheet needs these columns:
- **date** - Date in YYYY-MM-DD format (e.g., 2024-01-15)
- **task_type** - Type of work (electrician, plumber, hvac_technician, carpenter, general_handyman, painter, landscaper, or other)
- **description** - What was done
- **hours_spent** - Number of hours (decimal OK, e.g., 2.5)
- **materials_cost** - Cost in dollars (e.g., 125.50)

Optional columns:
- technician_name
- location
- priority
- notes

## Customizing Rates

If your market rates differ from the defaults, you can customize them:

1. Copy the example rate files from `data/templates/`:
   - `market_rates_example.json`
   - `inhouse_rates_example.json`

2. Edit the rates to match your area

3. Run with custom rates:
```bash
python analyze_with_custom_rates.py data/uploads/your_file.csv \
  --market-rates data/templates/your_market_rates.json \
  --inhouse-rates data/templates/your_inhouse_rates.json
```

## Understanding Task Types

The system recognizes these task types:
- **electrician** - Electrical work (default market rate: $85/hr)
- **plumber** - Plumbing work (default market rate: $90/hr)
- **hvac_technician** - HVAC work (default market rate: $95/hr)
- **carpenter** - Carpentry work (default market rate: $75/hr)
- **general_handyman** - General maintenance (default market rate: $65/hr)
- **painter** - Painting work (default market rate: $55/hr)
- **landscaper** - Landscaping work (default market rate: $50/hr)
- **other** - Anything else (default market rate: $70/hr)

Task types are case-insensitive and extra spaces are ignored.

## Tips for Accurate Analysis

1. **Be consistent with task types** - Use the same spelling each time
2. **Include all materials costs** - This affects total cost calculations
3. **Track actual hours** - Don't round too much; use decimals (e.g., 1.5 hours)
4. **Regular uploads** - Process logs monthly or quarterly for trends
5. **Compare regions** - Different markets have different rates

## Troubleshooting

### "Missing required columns" error
Make sure your spreadsheet has all required columns with exact names:
- date
- task_type
- description
- hours_spent
- materials_cost

### Wrong date format
Dates should be in YYYY-MM-DD format (e.g., 2024-01-15)

### Wrong task type rates being used
If your task type doesn't match exactly, it will use the "other" rate.
Check your spelling and make sure it's one of the recognized types.

## Next Steps

- Review `README.md` for full documentation
- Customize rates in `config.py` for permanent changes
- Export data from your maintenance tracking system
- Set up regular analysis reports (monthly/quarterly)
