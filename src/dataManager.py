from pathlib import Path, PosixPath
import pandas as pd
import numpy as np

from datetime import datetime

from utils.parameters import *
import extra

from typing import Literal

class Manager():
    '''
    Manages everything related with the creation, update or deletion
    of entries in the register's data files.
    '''

    class ManagerException(Exception):
        def __init__(self, message: str = ''):
            super().__init__(message)

    class NotFoundID(ManagerException):
        def __init__(self):
            super().__init__('NIF/NIE no encontrado.')

    class InvalidID(ManagerException):
        def __init__(self):
            super().__init__('Formato de NIF/NIE inválido.')

    class InvalidCredentials(ManagerException):
        def __init__(self):
            super().__init__('Credenciales incorrectas.')

    class AlreadyExistingID(ManagerException):
        def __init__(self):
            super().__init__('NIF/NIE ya registrado.')

    class AlreadyExistingPhone(ManagerException):
        def __init__(self):
            super().__init__('Número de teléfono ya registrado.')

    class UnmatchingPassword(ManagerException):
        def __init__(self):
            super().__init__("Las contraseñas no coinciden.")

    class EmptyEntry(ManagerException):
        def __init__(self):
            super().__init__("Debe rellenar todos los campos.")


    @staticmethod
    def setup() -> None:
        '''
        Prepares all dependencies for the program to run correctly
        '''

        # Check if directories exist+
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True)


    @staticmethod
    def get_dataframe(size: int = None, as_list: bool = False,
            filename: str | Path | PosixPath = None) -> pd.DataFrame | list:
        '''
        Retrieves (or creates) the dataframe containing the solicited registry

        Params:
            start (int, Default=0): Starting index (row) for the dataframe
            size (int, Default=None): Maximum number of rows to be retrieved
            as_list (bool, Default=False): Whether to return a DataFrame or a list of rows
            filename (str | Path | PosixPath, Default=None): Name of the file storing the data

        :returns output (pd.DataFrame | list): The information
        '''

        if Path(DATA_DIR, filename).exists():
            df = pd.read_parquet(Path(DATA_DIR, filename), 'pyarrow')

        elif filename == LOG_FILE:
            df = pd.DataFrame(columns=['NIF/NIE', 'Día', 'Hora', 'Jornada'])
        
        elif filename == STAFF_FILE:
            df = pd.DataFrame(columns=['NIF/NIE', 'Nombre', 'Apellido1', 'Apellido2', 'Código_Postal',
                                        'Dirección', 'Email', 'Tfno', 'Contraseña', 'Admin'])

        if size is None:
            size = len(df)

        res_df = df[ : min(size, len(df))]

        if as_list:
            return res_df.values.tolist()

        else:
            return res_df


    @staticmethod
    def get_columns(which: Literal['staff', 'logs'] = None) -> list:
        '''
        Retrieves the column names of the specified dataframe

        :params (Literal['staff', 'logs'], Default=None) which: The dataframe

        :returns output (list): The column names
        '''

        if which == 'staff':
            df = Manager.get_dataframe(filename=STAFF_FILE)
        
        else:
            df = Manager.get_dataframe(filename=LOG_FILE)

        return list(df.columns)


    @staticmethod
    def get_uniques(df: pd.DataFrame, col: str) -> list:
        '''
        Retrieves the unique values of the specified column

        Params:
            df (pd.DataFrame): The dataframe
            col (str): The column to get the values from

        :returns output (list): The unique values
        '''

        return list(df[col].unique())


    @staticmethod
    def get_min(df: pd.DataFrame, col: str) -> str:
        '''
        Retrieves the minimum value of the specified column

        Params:
            df (pd.DataFrame): The dataframe
            col (str): The column to get the values from

        :returns output (str): The min value
        '''

        return str(datetime.now().date()) if df[col].empty else df[col].min()


    @staticmethod
    def get_max(df: pd.DataFrame, col: str) -> str:
        '''
        Retrieves the maximum value of the specified column

        Params:
            df (pd.DataFrame): The dataframe
            col (str): The column to get the values from

        :returns output (str): The max value
        '''

        return str(datetime.now().date()) if df[col].empty else df[col].max()


    @staticmethod
    def export_df(colnames: list | tuple, rows: list | tuple, path: str | Path | PosixPath) -> None:
        '''
        Exports the current table into a CSV file

        Params:
            colnames (list | tuple): The column names for the dataframe
            rows (list | tuple): The rows of the dataframe
            path (str | Path | PosixPath): Location for the CSV file to be saved
        '''

        df = pd.DataFrame(columns=colnames)

        for row in rows:
            df.loc[len(df)] = row

        df.to_csv(path, index=False)
        

    @staticmethod
    def filter_df(filename: str | Path | PosixPath, params: dict, as_list: bool = False) -> pd.DataFrame | list:
        '''
        Returns a dataframe extracted from `path`, filters it and returns it

        Params:
            filename (str | Path | PosixPath): Name of the file storing the data
            params (dict): The filters to apply
            as_list (bool, Default=False): Whether to return a DataFrame or a list of rows

        :returns output (pd.DataFrame | list): The filtered information
        '''
        
        df = Manager.get_dataframe(filename=filename)

        for p, value in params.items():
            
            if type(value) != list:
                if value != EMPTY_OPTION:
                    df = df[df[p] == value]

            else:
                df = df[(df[p] >= value[0]) & (df[p] <= value[1])]

        if as_list:
            return df.values.tolist()

        else:
            return df


    @staticmethod
    def __valid_id(num: str) -> bool:
        '''
        Checks whether an ID number has a valid format

        :params (str) num: The ID number

        :returns output (bool): `True` if the ID number is valid; `False` otherwise
        '''

        is_nif = (len(num) == 9) and (num[:8].isnumeric()) and (num[8].isalpha())
        is_nie = (len(num) == 9) and (num[1:8].isnumeric()) and (num[8].isalpha()) and (num[0] in ['X', 'Y', 'Z'])

        return is_nif or is_nie


    @staticmethod
    def log_in(num: str, passwd: str) -> bool:
        '''
        Checks whether the passed credentials correspond to a member in the database

        Params:
            num (str): The ID number
            passwd (str): The password associated with that ID number

        :returns output (bool): `True` if the log in has been successful; `False` otherwise
        '''

        # Verify entries
        if num == '' or passwd == '':
            raise Manager.EmptyEntry()

        if not Manager.__valid_id(num):
            raise Manager.InvalidID()
        
        # Validate credentials
        df = Manager.get_dataframe(filename=STAFF_FILE)

        employee = df[df['NIF/NIE'] == num]

        if num != extra.N or passwd != extra.P:
            if employee.empty or list(employee['Contraseña'])[0] != passwd:
                raise Manager.InvalidCredentials()
            
            return list(employee['Admin'])[0]
            
        else: return True


    @staticmethod
    def add_worker(name: str, last1: str, last2: str,
        post_code: str, address: str, email: str, phone: str,
        number: str, passwd: str, re_passwd: str, isAdmin: int) -> None:
        '''
        Adds a new worker's information to the dataframe

        Params:
            name (str): Employee's name
            last1 (str): Employee's last name (first one)
            last2 (str): Employee's last name (second one)
            post_code (str): Employee's postal code
            address (str): Employee's physical address
            email (str): Employee's email address
            phone (str): Employee's phone number
            number (str): ID card number
            passwd (str): Employee's password
            re_passwd (str): Employee's password again (to check)
            isAdmin (int): Whether the user has been granted admin priviledges (`1`) or not (`0`)
        '''

        # Get dataframe
        df = Manager.get_dataframe(filename=STAFF_FILE)

        # Verify entries
        if not Manager.__valid_id(number):
            raise Manager.InvalidID()
        
        if passwd != re_passwd:
            raise Manager.UnmatchingPassword()
        
        # Verify if new employee
        if number in list(df['NIF/NIE']):
            raise Manager.AlreadyExistingID()
        
        if phone in list(df['Tfno']):
            raise Manager.AlreadyExistingPhone()
        
        df.loc[len(df)] = [number, name, last1, last2, post_code, address,
                        email, phone, passwd, bool(isAdmin)]

        # Save data
        df.to_parquet(Path(DATA_DIR, STAFF_FILE), engine='pyarrow')
    

    @staticmethod
    def begin_shift(number: str) -> bool:
        '''
        Checks whether a shift is starting or ending

        :params (str) number: ID number

        :returns output (bool): `True` if is the beginning of the user's shift; `False` otherwise
        '''
        
        logs = Manager.get_dataframe(filename=LOG_FILE)

        return len(logs[logs['NIF/NIE'] == number]) % 2 == 0


    @staticmethod
    def add_entry(number: str) -> None:
        '''
        Adds a new log to the dataframe

        :params (str) number: ID number
        '''

        if not Manager.__valid_id(number):
            raise Manager.InvalidID()

        df = Manager.get_dataframe(filename=STAFF_FILE)

        employee = df[df['NIF/NIE'] == number]

        if employee is None:
            raise Manager.NotFoundID()

        logs = Manager.get_dataframe(filename=LOG_FILE)
        dt = str(datetime.now()).split()

        startShift = Manager.begin_shift(number)

        logs.loc[len(logs)] = [
            number,
            dt[0],
            dt[1].split('.')[0],
            'Inicio' if startShift else 'Fin'
        ]

        logs.to_parquet(Path(DATA_DIR, LOG_FILE), engine='pyarrow')