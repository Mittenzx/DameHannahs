# Converting Your Jobs List to Maintenance Log Format

## Overview

If you have a jobs list in a different format (like the `jobstotal.xlsx` format), you can use the `convert_jobs_list.py` utility to convert it into the format required by the maintenance log analysis system.

## Jobs List Format

Your jobs list should have columns like:
- `jobno` - Job reference number
- `title` - Description of the job
- `created` - Date job was created
- `resolved` - Date job was completed
- `category` - Type of job (Electrical, Plumbing, etc.)
- `status` - Job status (Complete, New, etc.)

## Required Information for Cost Analysis

To perform accurate cost analysis, you need to add:
1. **Hours spent** on each job (actual time worked)
2. **Materials cost** for each job (cost of parts/materials used)

## Conversion Process

### Step 1: Convert the Jobs List

Run the converter script:
```bash
python convert_jobs_list.py jobstotal.xlsx output_filename.csv
```

This will:
- Read your jobs list
- Filter to completed jobs only
- Map job categories to task types
- Create a CSV file with default values for hours and costs

**Important:** The converter uses default placeholder values:
- Hours spent: 2.0 hours per job
- Materials cost: $50.00 per job

### Step 2: Add Actual Time and Cost Data

Open the converted CSV file and update:
1. `hours_spent` - Replace with actual hours worked
2. `materials_cost` - Replace with actual materials cost

You can do this in:
- Microsoft Excel
- Google Sheets
- Any text editor
- Python script with your time tracking data

### Step 3: Run the Analysis

Once you've added the actual time and cost data:
```bash
python analyze_maintenance_logs.py output_filename.csv
```

## Category Mapping

The converter maps job categories to task types:

| Jobs List Category | Analysis Task Type |
|-------------------|-------------------|
| Electrical        | electrician       |
| Plumbing          | plumber          |
| Equipment         | hvac_technician  |
| Assembly          | carpenter        |
| Decorative        | painter          |
| Groundwork        | landscaper       |
| Move              | general_handyman |
| Other categories  | other            |

## Example

```bash
# Convert jobs list
python convert_jobs_list.py data/jobstotal.xlsx data/uploads/2024_jobs.csv

# Open in Excel and add hours_spent and materials_cost columns
# Save the file

# Run analysis
python analyze_maintenance_logs.py data/uploads/2024_jobs.csv
```

## Tips for Adding Time/Cost Data

### If you track time separately:
Join your time tracking data with the converted CSV using the job number.

### If you don't have exact data:
You can estimate based on:
- Job category averages
- Typical time for similar tasks
- Historical data from invoices

### For better accuracy:
- Start tracking time going forward
- Review past invoices or work orders
- Interview maintenance staff for estimates
- Use time ranges (e.g., 1-2 hours = 1.5)

## Customizing the Converter

You can modify `convert_jobs_list.py` to:
- Change default hours/costs
- Adjust category mappings
- Add custom logic for your data structure
- Integrate with other data sources

## Need Help?

If you need assistance:
1. Check the main README.md for system documentation
2. Review QUICKSTART.md for getting started
3. Run `python validate_spreadsheet.py your_file.csv` to check format
4. Look at sample data in `data/templates/` for examples
