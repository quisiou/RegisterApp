# Constants, file directories and stuff

from pathlib import Path

# Window related
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 200


# Directories
DATA_DIR = Path(Path.cwd(), 'data')
LOG_FILE = 'log.parquet'
STAFF_FILE = 'empleados.parquet'