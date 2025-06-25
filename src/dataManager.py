from pathlib import Path, PosixPath
import pandas as pd

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
    def get_dataframe(start=0, size=None, as_list=False, path=None) -> pd.DataFrame:
        '''
        Retrieves (or creates) the dataframe containing the solicited registry

        :returns output (pd.DataFrame): The information
        '''

        if Path(DATA_DIR, path).exists():
            df = pd.read_parquet(Path(DATA_DIR, path), 'pyarrow')

        elif path == LOG_FILE:
            df = pd.DataFrame(columns=['NIF/NIE', 'Día', 'Hora', 'Jornada'])
        
        elif path == STAFF_FILE:
            df = pd.DataFrame(columns=['Nombre', 'Apellido1', 'Apellido2', 'Código_Postal',
                                    'Dirección', 'Email', 'Tfno', 'NIF/NIE', 'Contraseña', 'Admin'])

        if size is None:
            size = len(df)

        res_df = df[min(start, 0) : min(start + size, len(df))]

        if as_list:
            return res_df.values.tolist()

        else:
            return res_df


    @staticmethod
    def get_columns(which: Literal['staff', 'logs'] = None) -> tuple:

        if which == 'staff':
            df = Manager.get_dataframe(path=STAFF_FILE)
        
        else:
            df = Manager.get_dataframe(path=LOG_FILE)

        return tuple(df.columns)


    @staticmethod
    def __valid_id(num: str) -> bool:
        is_nif = (len(num) == 9) and (num[:8].isnumeric()) and (num[8].isalpha())
        is_nie = (len(num) == 9) and (num[1:8].isnumeric()) and (num[8].isalpha()) and (num[0] in ['X', 'Y', 'Z'])

        return is_nif or is_nie


    @staticmethod
    def log_in(num: str, passwd: str) -> bool:

        # Verify entries
        if num == '' or passwd == '':
            raise Manager.EmptyEntry()

        if not Manager.__valid_id(num):
            raise Manager.InvalidID()
        
        # Validate credentials
        df = Manager.get_dataframe(path=STAFF_FILE)

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
        Adds a new worker's info to the dataframe

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
        '''

        # Get dataframe
        df = Manager.get_dataframe(path=STAFF_FILE)

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
        
        df.loc[len(df)] = [name, last1, last2, post_code, address, email,
                        phone, number, passwd, bool(isAdmin)]

        # Save data
        df.to_parquet(Path(DATA_DIR, STAFF_FILE), engine='pyarrow')
    

    @staticmethod
    def begin_shift(number: str) -> bool:
        '''
        Checks whether a shift is starting or ending

        :params (str) number: ID card number

        :returns output (bool): `True` if the shift is starting, `False` otherwise
        '''
        
        logs = Manager.get_dataframe(path=LOG_FILE)

        return len(logs[logs['NIF/NIE'] == number]) % 2 == 0


    @staticmethod
    def add_entry(number: str) -> bool:
        '''
        Adds a new log to the dataframe

        Params:
            number (str): ID card number
            password (str): Employee's password
        '''

        if not Manager.__valid_id(number):
            raise Manager.InvalidID()

        df = Manager.get_dataframe(path=STAFF_FILE)

        employee = df[df['NIF/NIE'] == number]

        if employee is None:
            raise Manager.NotFoundID()

        logs = Manager.get_dataframe(path=LOG_FILE)
        dt = str(datetime.now()).split()

        startShift = Manager.begin_shift(number)

        logs.loc[len(logs)] = [
            number,
            dt[0],
            dt[1].split('.')[0],
            'Inicio' if startShift else 'Fin'
        ]

        logs.to_parquet(Path(DATA_DIR, LOG_FILE), engine='pyarrow')