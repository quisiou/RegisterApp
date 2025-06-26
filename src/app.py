import customtkinter as ctk

from tkinter.ttk import Treeview
from tkinter import messagebox, filedialog

from src.dataManager import Manager

from pathlib import Path

from src.widget import *
from src.window import Window

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
        self.geometry(self.__centerWindowOnScreen(width, height))
        # self.resizable(width=False, height=False)
        self.resizable(width=True, height=True)
        self.title('Clocker')

        # Attributes
        self._children = {}
        self._cookies = {}

        # Binds
        self.bind(sequence="<Escape>", func=self.__unfocus)

        # Create all the widgets for the application
        self.__initialize()


    def __centerWindowOnScreen(self, width: int, height: int, scale_factor: float = 1.0):
        '''
        Centers the window to the main display/monitor
        '''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (width/2)) * scale_factor)
        y = int(((screen_height/2) - (height/1.5)) * scale_factor)
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

            self._cookies = None


        def change_to_create(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['createUserFrame'].show()

        
        def check_log(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['logRegistryFrame'].show()

        
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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
            Obj=CTkFrame,
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


        def show_log(event=None) -> None:

            data = Manager.get_dataframe(as_list=True, path=LOG_FILE)

            tree = self._children['logRegistryFrame']['logTable'].widget

            # Delete possible items
            tree.delete(*tree.get_children())

            for entry in data:
                tree.insert(
                    parent='',
                    index=0, # New rows are inserted at the beginning
                    values=entry
                )


        def add_entries(event=None) -> int:
            colnames = Manager.get_columns(which='logs')

            logTable = Widget(
                Obj=Treeview,
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
            show_log()


        def filter_table(event=None) -> None:
            print('filtrando...')


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
            Obj=CTkFrame,
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

        add_entries()

        buttonsFrame = Widget(
            Obj=CTkFrame,
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
                'command': show_log,
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
                'command': filter_table,
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

            data = Manager.get_dataframe(as_list=True, path=STAFF_FILE)

            tree = self._children['staffRegistryFrame']['staffTable'].widget

            # Delete possible items
            tree.delete(*tree.get_children())

            for entry in data:
                tree.insert(
                    parent='',
                    index=0, # New rows are inserted at the beginning
                    values=entry
                )


        def add_entries(event=None) -> int:
            colnames = Manager.get_columns(which='staff')

            staffTable = Widget(
                Obj=Treeview,
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

        
        # The frame containing everything
        staffRegistryFrame = Widget(
            Obj=CTkFrame,
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

        add_entries()

        buttonsFrame = Widget(
            Obj=CTkFrame,
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