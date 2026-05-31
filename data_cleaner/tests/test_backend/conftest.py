import sys
import os
 
# Replicate the same sys.path uvicorn uses when running from src/backend/
# This lets pytest resolve bare imports like `from services.cleaner import ...`
# without modifying any source files.
backend_test_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = os.path.dirname(backend_test_dir)
root_dir = os.path.dirname(tests_dir)
backend_dir = os.path.join(root_dir, "src", "backend")
sys.path.insert(0, backend_dir)