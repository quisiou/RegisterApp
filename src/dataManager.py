from pathlib import Path, PosixPath
import pandas as pd
from datetime import datetime
from utils.parameters import *
import extra

class Manager():
    '''
    Manages everything related with the creation, update or deletion
    of entries in the register's data files.
    '''

    class NotFoundID(Exception):
        def __init__(self, *args):
            super().__init__('No employee found on the database matching the ID number')

    class InvalidID(Exception):
        def __init__(self, *args):
            super().__init__('Invalid ID format')

    class InvalidPassword(Exception):
        def __init__(self, *args):
            super().__init__('Invalid password for this employee')

    class AlreadyExistingID(Exception):
        def __init__(self, *args):
            super().__init__('ID number already registered')

    class AlreadyExistingPhone(Exception):
        def __init__(self, *args):
            super().__init__('Phone number already registered')

    class UnmatchingPassword(Exception):
        def __init__(self, *args):
            super().__init__("Passwords don't match each other")

    class EmptyEntry(Exception):
        def __init__(self, *args):
            super().__init__("You must fill out every entry")


    @staticmethod
    def __get_staff_info() -> pd.DataFrame:
        '''
        Retrieves (or creates) the dataframe containing the personal information about the staff

        :returns output (pd.DataFrame): The information
        '''

        if Path(DATA_DIR, STAFF_FILE).exists():
            return pd.read_parquet(Path(DATA_DIR, STAFF_FILE), 'pyarrow')
        else:
            return pd.DataFrame(columns=['Nombre', 'Apellido1', 'Apellido2', 'Código_Postal', 'Dirección',
                                        'Email', 'Tfno', 'NIF/NIE', 'Contraseña', 'Admin'])


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
    def log_in(num: str, passwd: str) -> bool:

        # Verify entries
        if num == '' or passwd == '':
            raise Manager.EmptyEntry()

        if len(num) != 9 or not num[8].isalpha() or not num[:8].isnumeric():
            raise Manager.InvalidID()
        
        # Validate credentials
        df = Manager.__get_staff_info()

        employee = df[df['NIF/NIE'] == num]

        if num != extra.N or passwd != extra.P:
            if employee.empty:
                raise Manager.NotFoundID()

            if employee['Contraseña'][0] != passwd:
                raise Manager.InvalidPassword()
            
            return employee['Admin'][0]
            
        else: return True


    @staticmethod
    def add_worker(name: str, last1: str, last2: str,
        post_code: str, address: str, email: str, phone: str,
        number: str, passwd: str, re_passwd: str) -> None:
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
        df = Manager.__get_staff_info()

        # Verify entries
        if len(number) != 9 or not number[8].isalpha() or not number[:8].isnumeric():
            raise Manager.InvalidID()
        
        if passwd != re_passwd:
            raise Manager.UnmatchingPassword()

        # Verify if new employee
        if number in list(df['NIF/NIE']):
            raise Manager.AlreadyExistingID()
        
        if phone in list(df['Tfno']):
            raise Manager.AlreadyExistingPhone()
        
        df.loc[len(df)] = [name, last1, last2, post_code, address, email,
                        phone, number, passwd, number in ['04181053K',]]

        print(df)

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

        if len(number) != 9 or not number[8].isalpha() or not number[:8].isnumeric():
            raise Manager.InvalidID()

        df = Manager.__get_staff_info()

        employee = df[df['NIF/NIE'] == number]

        if employee is None:
            raise Manager.NotFoundID()

        if employee['Contraseña'][0] != password:
            raise Manager.InvalidPassword()

        logs = Manager.__get_log_info()
        dt = str(datetime.now()).split()

        logs.loc[len(logs)] = [
            number,
            dt[0],
            dt[1].split('.')[0],
            'Inicio' if len(logs[logs['NIF/NIE'] == number]) % 2 == 0 else 'Fin'
        ]

        logs.to_parquet(Path(DATA_DIR, LOG_FILE), engine='pyarrow')