# Constants, file directories and stuff

from pathlib import Path

# Window related
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400


# Directories
DATA_DIR = Path(Path.home(), 'Clocker', 'data')
LOG_FILE = 'log.parquet'
STAFF_FILE = 'empleados.parquet'


# General stuff
SHOW_PASSWORD = '*'
PAGE_SIZE = 2
EMPTY_OPTION = 'Cualquiera'