# Constants, file directories and stuff

from pathlib import Path
from platform import system
import os

# Window related
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400


# Directories
if system() == 'Windows':
    DATA_DIR = Path(os.getenv('LOCALAPPDATA'), 'Clocker', 'data')

elif system() == 'Linux':
    DATA_DIR = Path(Path.home(), '.local', 'share', 'Clocker', 'data')


LOG_FILE = 'log.parquet'
STAFF_FILE = 'empleados.parquet'


# General stuff
SHOW_PASSWORD = '*'
PAGE_SIZE = 2
EMPTY_OPTION = 'Cualquiera'