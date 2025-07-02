# Constants, file directories and stuff

from pathlib import Path
from platform import system
import os

# Name
APP_NAME = 'ClockR'

# Window related
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400


# Directories
if system() == 'Windows':
    DATA_DIR = Path(os.getenv('LOCALAPPDATA'), APP_NAME, 'data')

elif system() == 'Linux':
    DATA_DIR = Path(Path.home(), '.local', 'share', APP_NAME, 'data')


LOG_FILE = 'log.parquet'
STAFF_FILE = 'empleados.parquet'

IMG_DIR = Path(Path.cwd(), 'img')
DEFAULT_EXPORT_DIR = Path.home()
DEFAULT_EXPORT_NAME = 'registro.csv'


# General stuff
SHOW_PASSWORD = '*'
PAGE_SIZE = 2
EMPTY_OPTION = 'Cualquiera'