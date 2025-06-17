# Constants, file directories and stuff

from pathlib import Path

# Window related
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400


# Directories
DATA_DIR = Path(Path.cwd(), 'data')
LOG_FILE = 'log.parquet'
STAFF_FILE = 'empleados.parquet'