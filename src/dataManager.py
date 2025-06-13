from pathlib import Path, PosixPath
import pandas as pd
from datetime import datetime
from utils.parameters import *

class Manager():
    '''
    Manages everything related with the creation, update or deletion
    of entries in the register's data files.
    '''


    @staticmethod
    def __get_staff_info() -> pd.DataFrame:
        '''
        Retrieves (or creates) the dataframe containing the personal information about the staff

        :returns output (pd.DataFrame): The information
        '''

        if Path(DATA_DIR, STAFF_FILE).exists():
            return pd.read_parquet(Path(DATA_DIR, STAFF_FILE), 'pyarrow')
        else:
            return pd.DataFrame(columns=['NIF/NIE', 'Nombre', 'Apellido1', 'Apellido2', 'Código'])


    @staticmethod
    def __get_log_info() -> pd.DataFrame:
        '''
        Retrieves (or creates) the dataframe containing the registry

        :returns output (pd.DataFrame): The information
        '''

        if Path(DATA_DIR, LOG_FILE).exists():
            return pd.read_parquet(Path(DATA_DIR, LOG_FILE), 'pyarrow')
        else:
            return pd.DataFrame(columns=['NIF/NIE', 'Día', 'Hora', 'Jornada'])


    @staticmethod
    def add_worker(number: str, name: str, last1: str, last2: str, password: str) -> None:
        '''
        Adds a new worker's info to the dataframe

        Params:
            number (str): ID card number
            name (str): Employee's name
            last1 (str): Employee's last name (first one)
            last2 (str): Employee's last name (second one)
            password (str): Employee's password
        '''

        # Get dataframe
        df = Manager.__get_staff_info()

        # Verify if new employee
        if number in list(df['NIF/NIE']):
            print('Ya existe')
        else:
            df.loc[len(df)] = [number, name, last1, last2, password]

            # Save data
            df.to_parquet(Path(DATA_DIR, STAFF_FILE), engine='pyarrow')
    

    @staticmethod
    def add_entry(number: str, password: str) -> None:
        '''
        Adds a new log to the dataframe

        Params:
            number (str): ID card number
            password (str): Employee's password
        '''

        df = Manager.__get_staff_info()

        employee = df[df['NIF/NIE'] == number]

        if employee is not None and employee['Código'][0] == password:

            logs = Manager.__get_log_info()

            dt = str(datetime.now()).split()

            logs.loc[len(logs)] = [
                number,
                dt[0],
                dt[1].split('.')[0],
                'Inicio' if len(logs[logs['NIF/NIE'] == number]) % 2 == 0 else 'Fin'
            ]

            logs.to_parquet(Path(DATA_DIR, LOG_FILE), engine='pyarrow')