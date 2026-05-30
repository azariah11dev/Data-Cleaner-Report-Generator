import sys
import os
 
# Replicate the same sys.path uvicorn uses when running from src/backend/
# This lets pytest resolve bare imports like `from services.cleaner import ...`
# without modifying any source files.
backend_dir = os.path.join(os.path.dirname(__file__), "src", "backend")
sys.path.insert(0, backend_dir)