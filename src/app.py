import customtkinter as ctk

from tkinter.ttk import Treeview
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry

from src.dataManager import Manager

from pathlib import Path
from datetime import datetime

from src.widget import *

from utils.parameters import *
from utils.appearance import *

class App(ctk.CTk):
    '''
    Main application class
    '''

    _children: dict = None # Children widgets of the app
    _cookies: dict = None # Credential cookies for when logged in

    def __init__(self, width: int = WINDOW_WIDTH,
        height: int = WINDOW_HEIGHT, custom_theme: str = None):

        # set custom theme
        theme_path = Path(Path.cwd(), 'themes', f'{custom_theme}.json')
        if not custom_theme or not theme_path.exists():
            ctk.set_default_color_theme('blue')
        else:
            ctk.set_default_color_theme(theme_path)

        super().__init__()

        # window-related
        self.geometry(self.__centerWindowOnScreen(
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
            width,
            height
        ))
        self.resizable(width=False, height=False)
        self.title('Clocker')

        # Attributes
        self._children = {}
        self._cookies = {}

        # Binds
        self.bind(sequence="<Escape>", func=self.__unfocus)

        # Create all the widgets for the application
        self.__initialize()


    def __centerWindowOnScreen(self, screen_width, screen_height, width: int, height: int):
        '''
        Centers the window to the main display/monitor
        '''

        x = int((screen_width - width) / 2)
        y = int((screen_height / 2) - (height / 1.5))
        return f"{width}x{height}+{x}+{y}"


    def __unfocus(self, e=None) -> None:
        '''
        Unfocuses the actual focused widget (by focusing the main window)

        :params (Any, Default=None) e: The event which triggered this method
        '''

        self.focus()
    

    def __initialize_main(self) -> None:

        def log_out(event=None) -> None:

            self._children['mainFrame'].hide()
            self._children['logInFrame'].show()

            if self._cookies['admin']:
                self._children['mainFrame']['containerFrame']['checkLogButton'].deactivate()
                self._children['mainFrame']['containerFrame']['checkStaffButton'].deactivate()
                self._children['mainFrame']['containerFrame']['addStaffButton'].deactivate()

            else:
                self._children['mainFrame']['containerFrame']['addLogButton'].deactivate()

            self._children['logRegistryFrame']['logTable'].filters = None

            self._cookies = None


        def change_to_create(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['createUserFrame'].show()

        
        def check_log(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['logRegistryFrame'].show()
            self._children['logRegistryFrame']['logTable'].load(filename=LOG_FILE)

        
        def check_staff(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['staffRegistryFrame'].show()


        def add_log(event=None) -> None:

            if Manager.begin_shift(self._cookies['user']):
                self._children['mainFrame']['containerFrame']['addLogButton'].widget.configure(text="Finalizar jornada")
                
            else:
                self._children['mainFrame']['containerFrame']['addLogButton'].widget.configure(text="Comenzar jornada")

            Manager.add_entry(self._cookies['user'])
            messagebox.showinfo(message='Hora registrada.')
            

        mainFrame = Widget(
            Obj=ctk.CTkFrame,
            master=self,
            container=self._children,
            ID='mainFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'fill': ctk.BOTH, # Fill all the assigned space in the container
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )

        containerFrame = Widget(
            Obj=ctk.CTkFrame,
            master=mainFrame.widget,
            container=mainFrame.children,
            ID='containerFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )
        
        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='addStaffButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': change_to_create,
                'text': 'Crear usuario',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            },
            active=False
        )

        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='checkLogButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': check_log,
                'text': 'Registros',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            },
            active=False
        )

        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='checkStaffButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': check_staff,
                'text': 'Personal',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            },
            active=False
        )

        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='addLogButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': add_log,
                'text': 'Comenzar jornada',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            },
            active=False
        )

        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='logOutButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': log_out,
                'text': 'Cerrar sesión',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            }
        )


    def __initialize_login(self) -> None:

        def log_in(event=None, frame: Widget = None) -> None:

            try:
                passwd = frame.children['personalCodeEntry'].get()
                idNum = frame.children['idEntry'].get()

                isAdmin = Manager.log_in(idNum, passwd)

                self._cookies = {
                    'user': idNum,
                    'password': passwd,
                    'admin': isAdmin
                }

                if isAdmin:
                    self._children['mainFrame']['containerFrame']['checkLogButton'].activate()
                    self._children['mainFrame']['containerFrame']['checkStaffButton'].activate()
                    self._children['mainFrame']['containerFrame']['addStaffButton'].activate()

                else:
                    starts = Manager.begin_shift(idNum)
                    self._children['mainFrame']['containerFrame']['addLogButton'].activate()

                    if starts:
                        self._children['mainFrame']['containerFrame']['addLogButton'].widget.configure(text="Comenzar jornada")

                    else:
                        self._children['mainFrame']['containerFrame']['addLogButton'].widget.configure(text="Finalizar jornada")

                self._children['logInFrame'].hide()
                self._children['mainFrame'].show()

                frame.children['idEntry'].clear()
                frame.children['personalCodeEntry'].clear()

            except Manager.ManagerException as e:
                messagebox.showerror(message=str(e))

            self.__unfocus(event)

        
        # The frame containing everything
        logInFrame = Widget(
            Obj=ctk.CTkFrame,
            master=self,
            container=self._children,
            ID='logInFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'fill': ctk.BOTH, # Fill all the assigned space in the container
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            },
            show=True
        )

        # The frame with the widgets
        containerFrame = Widget(
            Obj=ctk.CTkFrame,
            master=logInFrame.widget,
            container=logInFrame.children,
            ID='containerFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            },
            show=True
        )

        # The entry for the ID number
        idEntry = Widget(
            Obj=ctk.CTkEntry,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='idEntry',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Introducir el DNI',
                'justify': ctk.CENTER,
                'width': WINDOW_WIDTH / 3,
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100
            },
            show=True
        )
        idEntry.widget.bind(sequence='<Return>', command=lambda x: log_in(event=x, frame=containerFrame))
        
        # The entry for the personal code
        personalCodeEntry = Widget(
            Obj=ctk.CTkEntry,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='personalCodeEntry',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Introducir el código',
                'show': SHOW_PASSWORD,
                'justify': ctk.CENTER,
                'width': WINDOW_WIDTH / 3,
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100
            },
            show=True
        )
        personalCodeEntry.widget.bind(sequence='<Return>', command=lambda x: log_in(event=x, frame=containerFrame))

        # The button which checks the code
        Widget(
            Obj=ctk.CTkButton,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='personalCodeChecker',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: log_in(frame=containerFrame),
                'text': 'Comprobar',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': WINDOW_WIDTH / 25,
                'pady': WINDOW_HEIGHT / 25
            },
            show=True
        ) 


    def __initialize_create(self) -> None:

        def createUser(*entries) -> None:
            try:
                for entry in entries:
                    if entry.get() == '':
                        raise Manager.EmptyEntry()

                Manager.add_worker(*[entry.get() for entry in entries])
                messagebox.showinfo(message='Empleado añadido correctamente.')

            except Manager.ManagerException as e:
                messagebox.showerror(message=str(e))

            self.__unfocus()


        def cancel(*entries) -> None:
            self._children['createUserFrame'].hide()
            self._children['mainFrame'].show()

            for entry in entries:
                entry.clear()

            self.__unfocus()


        # The frames and their configs

        createUserFrame = Widget(
            Obj=ctk.CTkFrame,
            master=self,
            container=self._children,
            ID='createUserFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': 'transparent'
            },
            position_params={
                'fill': ctk.BOTH,
                'expand': True,
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )

        dataInputFrame = Widget(
            Obj=ctk.CTkFrame,
            master=createUserFrame.widget,
            container=createUserFrame._children,
            ID='dataInputFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            }
        )
        
        buttonsFrame = Widget(
            Obj=ctk.CTkFrame,
            master=createUserFrame.widget,
            container=createUserFrame._children,
            ID='buttonsFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.BOTH
            }
        )
        
        nameInfoFrame = Widget(
            Obj=ctk.CTkFrame,
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='nameInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            } 
        )

        localInfoFrame = Widget(
            Obj=ctk.CTkFrame,
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='localInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            } 
        )

        accountInfoFrame = Widget(
            Obj=ctk.CTkFrame,
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='accountInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            } 
        )


        # The widgets

        nameEntry = Widget(
            Obj=ctk.CTkEntry,
            master=nameInfoFrame.widget,
            container=nameInfoFrame.children,
            ID='nameEntry',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Nombre',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT
            }
        )
        
        lastname1Entry = Widget(
            Obj=ctk.CTkEntry,
            master=nameInfoFrame.widget,
            container=nameInfoFrame.children,
            ID='lastname1',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Apellido 1',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        lastname2Entry = Widget(
            Obj=ctk.CTkEntry,
            master=nameInfoFrame.widget,
            container=nameInfoFrame.children,
            ID='lastname2',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Apellido 2',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        postalCodeEntry = Widget(
            Obj=ctk.CTkEntry,
            master=localInfoFrame.widget,
            container=localInfoFrame.children,
            ID='postalCode',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Código Postal',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
            }
        )
        
        addressEntry = Widget(
            Obj=ctk.CTkEntry,
            master=localInfoFrame.widget,
            container=localInfoFrame.children,
            ID='address',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Calle',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        emailEntry = Widget(
            Obj=ctk.CTkEntry,
            master=localInfoFrame.widget,
            container=localInfoFrame.children,
            ID='email',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Correo electrónico',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        phoneNumberEntry = Widget(
            Obj=ctk.CTkEntry,
            master=localInfoFrame.widget,
            container=localInfoFrame.children,
            ID='phoneNumber',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Tfno',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
            }
        )
        
        idNumberEntry = Widget(
            Obj=ctk.CTkEntry,
            master=accountInfoFrame.widget,
            container=accountInfoFrame.children,
            ID='idNumber',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'NIF',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
            }
        )
        
        passwordEntry = Widget(
            Obj=ctk.CTkEntry,
            master=accountInfoFrame.widget,
            container=accountInfoFrame.children,
            ID='password',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Contraseña',
                'show': SHOW_PASSWORD,
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        repeatPasswordEntry = Widget(
            Obj=ctk.CTkEntry,
            master=accountInfoFrame.widget,
            container=accountInfoFrame.children,
            ID='repeatPassword',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Repetir contraseña',
                'show': SHOW_PASSWORD,
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        adminCheckBox = Widget(
            Obj=ctk.CTkCheckBox,
            master=accountInfoFrame.widget,
            container=accountInfoFrame.children,
            ID='adminCheckBox',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'text': 'Administrador',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='cancelButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: cancel(nameEntry, lastname1Entry, lastname2Entry, postalCodeEntry, addressEntry,
                                emailEntry, phoneNumberEntry, idNumberEntry, passwordEntry, repeatPasswordEntry),
                'text': 'Volver',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='createButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: createUser(nameEntry, lastname1Entry, lastname2Entry, postalCodeEntry, addressEntry,
                                emailEntry, phoneNumberEntry, idNumberEntry, passwordEntry, repeatPasswordEntry, adminCheckBox),
                'text': 'Crear',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.RIGHT
            }
        )


    def __initialize_log_registry(self) -> None:

        def cancel(event=None) -> None:
            self._children['logRegistryFrame'].hide()
            self._children['mainFrame'].show()

            self.__unfocus()


        def add_entries(event=None) -> Table:
            colnames = Manager.get_columns(which='logs')

            logTable = Table(
                master=self._children['logRegistryFrame'].widget,
                container=self._children['logRegistryFrame'].children,
                ID='logTable',
                locator=Treeview.pack,
                forgetter=Treeview.pack_forget,
                params={
                    'columns': colnames,
                    'show': 'headings'
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT,
                    'fill': ctk.BOTH,
                    'expand': True
                }
            )
            
            # Add the column names to the heading
            for col in colnames:
                logTable.widget.heading(col, text=col)
                logTable.widget.column(col, stretch='NO', width=WINDOW_WIDTH // 5, anchor=TREEVIEW_ANCHOR)

            # Add the data to the table
            logTable.load(filename=LOG_FILE)

            return logTable


        def filter_table(event=None, table: Table = None) -> None:

            def save_filters(event=None, window: Window = None, table: Table = None, params: dict = None) -> None:
                
                table.filters = {
                    'NIF/NIE': numberDropdown.get(),
                    'Día': [
                        str(startDateEntry.widget.get_date()),
                        str(finalDateEntry.widget.get_date())
                    ],
                    'Jornada': shiftDropdown.get()
                }

                table.load(filename=LOG_FILE)

                window.destroy()


            def set_current_filters():
                filters = self._children['logRegistryFrame']['logTable'].filters

                if filters is not None:
                    numberDropdown.widget.set(filters['NIF/NIE'])
                    startDateEntry.widget.set_date(datetime.strptime(filters['Día'][0], '%Y-%m-%d').date())
                    finalDateEntry.widget.set_date(datetime.strptime(filters['Día'][1], '%Y-%m-%d').date())
                    shiftDropdown.widget.set(filters['Jornada'])


            modal = Window()
            modal.geometry(self.__centerWindowOnScreen(
                self.winfo_screenwidth(),
                self.winfo_screenheight(),
                4 * WINDOW_WIDTH // 5,
                4 * WINDOW_HEIGHT // 5
            ))
            modal.title('Búsqueda filtrada')
            modal.resizable(width=False, height=False)

            data = Manager.get_dataframe(filename=LOG_FILE)
            min_date = Manager.get_min_max(data, 'Día')[0].split('-')

            mainModalFrame = Widget(
                Obj=ctk.CTkFrame,
                master=modal,
                container=modal.content,
                ID='filtersFrame',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'fg_color': "transparent"
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'fill': ctk.BOTH,
                    'expand': True
                },
                show=True
            )

            filtersFrame = Widget(
                Obj=ctk.CTkFrame,
                master=mainModalFrame.widget,
                container=mainModalFrame.children,
                ID='filtersFrame',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'fg_color': "transparent"
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'fill': ctk.BOTH,
                    'expand': True
                },
                show=True
            )

            dropdownFrame = Widget(
                Obj=ctk.CTkFrame,
                master=filtersFrame.widget,
                container=filtersFrame.children,
                ID='dropdownFrame',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'fg_color': "transparent"
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'expand': True
                },
                show=True
            )

            Widget(
                Obj=ctk.CTkLabel,
                master=dropdownFrame.widget,
                container=dropdownFrame.children,
                ID='numberLabel',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'text': 'NIF/NIE:',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 100, WINDOW_WIDTH / 200),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT
                },
                show=True
            )

            numberDropdown = Widget(
                Obj=ctk.CTkOptionMenu,
                master=dropdownFrame.widget,
                container=dropdownFrame.children,
                ID='numberDropdown',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'values': [EMPTY_OPTION,] + Manager.get_uniques(data, col='NIF/NIE'),
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 200, WINDOW_WIDTH / 50),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT
                },
                show=True
            )

            shiftDropdown = Widget(
                Obj=ctk.CTkOptionMenu,
                master=dropdownFrame.widget,
                container=dropdownFrame.children,
                ID='shiftDropdown',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'values': [EMPTY_OPTION,] + Manager.get_uniques(data, col='Jornada'),
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 200, WINDOW_WIDTH / 100),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.RIGHT
                },
                show=True
            )

            Widget(
                Obj=ctk.CTkLabel,
                master=dropdownFrame.widget,
                container=dropdownFrame.children,
                ID='shiftLabel',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'text': 'Jornada:',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 50, WINDOW_WIDTH / 200),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.RIGHT
                },
                show=True
            )

            dateFrame = Widget(
                Obj=ctk.CTkFrame,
                master=filtersFrame.widget,
                container=filtersFrame.children,
                ID='startDateFrame',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'fg_color': "transparent"
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'expand': True
                },
                show=True
            )

            Widget(
                Obj=ctk.CTkLabel,
                master=dateFrame.widget,
                container=dateFrame.children,
                ID='startDateLabel',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'text': 'Desde:',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 100, WINDOW_WIDTH / 200),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT
                },
                show=True
            )

            startDateEntry = Widget(
                Obj=DateEntry,
                master=dateFrame.widget,
                container=dateFrame.children,
                ID='startDateEntry',
                locator=DateEntry.pack,
                forgetter=DateEntry.pack_forget,
                params={
                    'locale': 'es_ES',
                    'selectmode': 'day',
                    'showweeknumbers': False,
                    'showothermonthdays': False,
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold'),
                    'day': int(min_date[2]),
                    'month': int(min_date[1]),
                    'year': int(min_date[0])
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 200, WINDOW_WIDTH / 50),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT
                },
                show=True
            )
            
            finalDateEntry = Widget(
                Obj=DateEntry,
                master=dateFrame.widget,
                container=dateFrame.children,
                ID='finalDateEntry',
                locator=DateEntry.pack,
                forgetter=DateEntry.pack_forget,
                params={
                    'locale': 'es_ES',
                    'selectmode': 'day',
                    'showweeknumbers': False,
                    'showothermonthdays': False,
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 200, WINDOW_WIDTH / 100),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.RIGHT
                },
                show=True
            )
            
            Widget(
                Obj=ctk.CTkLabel,
                master=dateFrame.widget,
                container=dateFrame.children,
                ID='finalDateLabel',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'text': 'Hasta:',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': (WINDOW_WIDTH / 50, WINDOW_WIDTH / 200),
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.RIGHT
                },
                show=True
            )

            modalButtonsFrame = Widget(
                Obj=ctk.CTkFrame,
                master=mainModalFrame.widget,
                container=mainModalFrame.children,
                ID='modalButtonsFrame',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'fg_color': "transparent"
                },
                position_params={
                    'padx': WINDOW_HEIGHT / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'fill': ctk.BOTH
                },
                show=True
            )

            Widget(
                Obj=ctk.CTkButton,
                master=modalButtonsFrame.widget,
                container=modalButtonsFrame.children,
                ID='cancelButton',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'command': modal.destroy,
                    'text': 'Volver',
                    'border_color': '#1f538d',
                    'border_width': 2,
                    'fg_color': 'gray10',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.LEFT
                },
                show=True
            )
            
            Widget(
                Obj=ctk.CTkButton,
                master=modalButtonsFrame.widget,
                container=modalButtonsFrame.children,
                ID='applyFiltersButton',
                locator=ctk.CTkBaseClass.pack,
                forgetter=ctk.CTkBaseClass.pack_forget,
                params={
                    'command': lambda: save_filters(window=modal, table=table),
                    'text': 'Aplicar',
                    'height': WINDOW_HEIGHT / 10,
                    'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.RIGHT
                },
                show=True
            )

            set_current_filters()

            self.wait_window(modal)


        def export_table(event=None) -> None:

            tree: Treeview = self._children['logRegistryFrame']['logTable'].widget
            columns = tree['columns']
            rows = []

            # Add rows
            for item_id in tree.get_children():
                rows.append(tree.item(item_id)['values'])

            # Get export path
            path = filedialog.asksaveasfilename(
                title='Seleccionar ruta de destino',
                filetypes=(('CSV file', '*.csv'), ('All files', '*.*')),
                initialdir=Path.home()
            )

            if path:
                Manager.export_df(colnames=columns, rows=rows, path=path)

        
        # The frame containing everything
        logRegistryFrame = Widget(
            Obj=ctk.CTkFrame,
            master=self,
            container=self._children,
            ID='logRegistryFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'fill': ctk.BOTH, # Fill all the assigned space in the container
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )

        logTable = add_entries()

        vScrollBar = Widget(
            Obj=ctk.CTkScrollbar,
            master=logRegistryFrame.widget,
            container=logRegistryFrame.children,
            ID='vScrollBar',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'orientation': 'vertical',
                'command': logTable.widget.yview
            },
            position_params={
                'padx': (0, WINDOW_WIDTH / 100),
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT,
                'fill': ctk.Y
            }
        )
        logTable.widget.configure(yscrollcommand=vScrollBar.widget.set)

        buttonsFrame = Widget(
            Obj=ctk.CTkFrame,
            master=logRegistryFrame.widget,
            container=logRegistryFrame._children,
            ID='buttonsFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.RIGHT,
                'fill': ctk.BOTH
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='createButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: logTable.reload(filename=LOG_FILE),
                'text': 'Refrescar',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.X
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='filterTableButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: filter_table(table=logTable),
                'text': 'Filtrar',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.X,
                'expand': True
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='exportButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': export_table,
                'text': 'Exportar',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.X,
                'expand': True
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='cancelButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': cancel,
                'text': 'Volver',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.BOTTOM,
                'fill': ctk.X
            }
        )


    def __initialize_staff_registry(self) -> None:

        def cancel(event=None) -> None:
            self._children['staffRegistryFrame'].hide()
            self._children['mainFrame'].show()

            self.__unfocus()


        def show_staff(event=None) -> None:

            data = Manager.get_dataframe(as_list=True, filename=STAFF_FILE)

            tree = self._children['staffRegistryFrame']['staffTable'].widget

            # Delete possible items
            tree.delete(*tree.get_children())

            for entry in data:
                tree.insert(
                    parent='',
                    index=0, # New rows are inserted at the beginning
                    values=entry
                )


        def add_entries(event=None) -> Table:
            colnames = Manager.get_columns(which='staff')

            staffTable = Table(
                master=staffRegistryFrame.widget,
                container=staffRegistryFrame.children,
                ID='staffTable',
                locator=Treeview.pack,
                forgetter=Treeview.pack_forget,
                params={
                    'columns': colnames,
                    'show': 'headings'
                },
                position_params={
                    'padx': WINDOW_WIDTH / 100,
                    'pady': WINDOW_HEIGHT / 100,
                    'side': ctk.TOP,
                    'fill': ctk.BOTH,
                    'expand': True
                }
            )
            
            # Add the column names to the heading
            for col in colnames:
                staffTable.widget.heading(col, text=col)
                staffTable.widget.column(col, stretch='NO', width=WINDOW_WIDTH // 6, anchor=TREEVIEW_ANCHOR)

            # Add the data to the table
            show_staff()

            return staffTable

        
        # The frame containing everything
        staffRegistryFrame = Widget(
            Obj=ctk.CTkFrame,
            master=self,
            container=self._children,
            ID='staffRegistryFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'fill': ctk.BOTH, # Fill all the assigned space in the container
                'expand': True, # expand when window is resized
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )

        staffTable = add_entries()

        hScrollBar = Widget(
            Obj=ctk.CTkScrollbar,
            master=staffRegistryFrame.widget,
            container=staffRegistryFrame.children,
            ID='hScrollBar',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'orientation': 'horizontal',
                'command': staffTable.widget.xview
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.X
            }
        )
        staffTable.widget.configure(xscrollcommand=hScrollBar.widget.set)

        buttonsFrame = Widget(
            Obj=ctk.CTkFrame,
            master=staffRegistryFrame.widget,
            container=staffRegistryFrame._children,
            ID='buttonsFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.TOP,
                'fill': ctk.BOTH
            }
        )

        Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='cancelButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': cancel,
                'text': 'Volver',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': WINDOW_WIDTH / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': ctk.LEFT
            }
        )


    def __initialize(self) -> None:
        '''
        Initializes all the required widgets and frames for the application
        '''

        #####################
        # Create user Stuff #
        #####################

        self.__initialize_create()


        ################
        # Log Registry #
        ################

        self.__initialize_log_registry()


        ##################
        # Staff Registry #
        ##################

        self.__initialize_staff_registry()
        

        ##############################
        # The main frame (logged in) #
        ##############################

        self.__initialize_main()
        

        ################
        # Log-In Stuff #
        ################

        self.__initialize_login()