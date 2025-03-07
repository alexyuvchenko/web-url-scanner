"""
Configuration for the URL Scanner.
"""

from pathlib import Path

# Get the project root directory (parent of src)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Define paths for logs and reports
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True, parents=True)
REPORTS_DIR.mkdir(exist_ok=True, parents=True) 
