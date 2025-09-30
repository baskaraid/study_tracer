import sys
import os

# --- Tambahkan path project kamu ---
path = '/home/username/study_tracer'   # Ganti 'username' sesuai username PythonAnywhere kamu
if path not in sys.path:
    sys.path.append(path)

# --- Set working directory ---
os.chdir(path)

# --- Import Flask app dari app.py ---
from app import application  # Pastikan di app.py ada baris: application = app
