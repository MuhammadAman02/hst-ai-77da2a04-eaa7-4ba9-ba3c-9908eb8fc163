"""
Production-ready Seiko Watch Store with:
✓ Complete e-commerce functionality with luxury watch focus
✓ Professional product galleries with zoom and detailed views
✓ Shopping cart, user authentication, and order management
✓ Admin panel for inventory and order management
✓ Automatic professional watch imagery integration
✓ Modern responsive design with premium aesthetic
✓ Payment integration setup (Stripe documentation included)
✓ Zero-configuration deployment readiness
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from app.main import create_seiko_store
    from app.core.config import settings
    from app.core.database import init_database
    from app.core.logger import app_logger
    
    if __name__ in {"__main__", "__mp_main__"}:
        # Initialize database with sample data
        app_logger.info("Initializing Seiko Watch Store database...")
        init_database()
        
        # Create and run the store
        app_logger.info(f"Starting Seiko Watch Store on {settings.host}:{settings.port}")
        create_seiko_store()
        
except Exception as e:
    print(f"Error starting Seiko Watch Store: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)