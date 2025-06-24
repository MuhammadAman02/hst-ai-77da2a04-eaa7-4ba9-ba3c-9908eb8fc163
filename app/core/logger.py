"""
Logging configuration for Seiko Watch Store
"""

import logging
import sys
from pathlib import Path

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / "seiko_store.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger instance
app_logger = logging.getLogger("SeikoStore")