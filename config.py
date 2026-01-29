"""
Configuration settings for the Maintenance Log Analysis System
"""

# Directory paths
UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/output"
TEMPLATES_DIR = "data/templates"

# Default market rates (per hour in USD)
DEFAULT_MARKET_RATES = {
    "electrician": 85.00,
    "plumber": 90.00,
    "hvac_technician": 95.00,
    "carpenter": 75.00,
    "general_handyman": 65.00,
    "painter": 55.00,
    "landscaper": 50.00,
    "other": 70.00
}

# Default in-house rates (per hour in USD)
# These are typically lower as they include salary costs divided by working hours
DEFAULT_INHOUSE_RATES = {
    "electrician": 45.00,
    "plumber": 48.00,
    "hvac_technician": 50.00,
    "carpenter": 42.00,
    "general_handyman": 35.00,
    "painter": 30.00,
    "landscaper": 28.00,
    "other": 38.00
}

# CSV/Excel column mappings (customize based on your spreadsheet format)
REQUIRED_COLUMNS = [
    "date",
    "task_type",
    "description",
    "hours_spent",
    "materials_cost"
]

# Optional columns
OPTIONAL_COLUMNS = [
    "technician_name",
    "location",
    "priority",
    "notes"
]
