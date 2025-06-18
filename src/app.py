import customtkinter as ctk

from src.dataManager import Manager

from pathlib import Path

from src.widget import Widget, Frame
from utils.parameters import *

class App(ctk.CTk):
    '''
    Main application class
    '''

    _children: dict = None # Children widgets of the app

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


        def change_to_create(event=None) -> None:
            self._children['mainFrame'].hide()
            self._children['createUserFrame'].show()


        mainFrame = Frame(
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
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            }
        )
        
        logInButton = Widget(
            Obj=ctk.CTkButton,
            master=mainFrame.widget,
            container=mainFrame.children,
            ID='logInButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': log_out,
                'text': 'Cerrar sesión'
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'pady': (self._current_height / 3, 0)
            }
        )
        
        addStaffButton = Widget(
            Obj=ctk.CTkButton,
            master=mainFrame.widget,
            container=mainFrame.children,
            ID='addStaffButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': change_to_create,
                'text': 'Crear usuario',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10'
            },
            position_params={
                'side': ctk.BOTTOM,
                'anchor': ctk.CENTER,
                'pady': (0, self._current_height / 3)
            }
        )


    def __initialize_login(self) -> None:

        def log_in(event=None, frame: Frame = None) -> None:

            try:
                passwd = frame.children['personalCodeEntry'].get()
                idNum = frame.children['idEntry'].get()

                Manager.log_in(idNum, passwd)

                self._children['logInFrame'].hide()
                self._children['mainFrame'].show()

            except Manager.EmptyEntry as e:
                print(e)

            except Manager.InvalidID as e:
                print(e)

            except Manager.NotFoundID as e:
                print(e)

            except Manager.InvalidPassword as e:
                print(e)

            self.__unfocus(event)

        
        # The frame containing everything
        logInFrame = Frame(
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
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            },
            active=True
        )

        # The frame with the widgets
        containerFrame = Frame(
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
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            },
            active=True
        )

        # The entry for the ID number
        Widget(
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            },
            active=True
        )
        
        # The entry for the personal code
        Widget(
            Obj=ctk.CTkEntry,
            master=containerFrame.widget,
            container=containerFrame.children,
            ID='personalCodeEntry',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'placeholder_text': 'Introducir el código',
                'justify': ctk.CENTER,
                'width': WINDOW_WIDTH / 3,
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            },
            active=True
        )
        
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
                'padx': self._current_width / 25,
                'pady': self._current_height / 25
            },
            active=True
        )


    def __initialize_create(self) -> None:

        def createUser(*entries) -> None:
            try:
                Manager.add_worker(*[entry.get() for entry in entries])
            except Manager.UnmatchingPassword as e:
                print(e)
            except Manager.AlreadyExistingID as e:
                print(e)
            except Manager.AlreadyExistingPhone as e:
                print(e)


        def cancel() -> None:
            self._children['createUserFrame'].hide()
            self._children['mainFrame'].show()


        # The frames and their configs

        createUserFrame = Frame(
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
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            }
        )

        dataInputFrame = Frame(
            master=createUserFrame.widget,
            container=createUserFrame._children,
            ID='dataInputFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': self._current_height / 100,
                'pady': self._current_height / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            }
        )
        
        buttonsFrame = Frame(
            master=createUserFrame.widget,
            container=createUserFrame._children,
            ID='buttonsFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': self._current_height / 100,
                'pady': self._current_height / 100,
                'side': ctk.TOP,
                'fill': ctk.BOTH
            }
        )
        
        nameInfoFrame = Frame(
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='nameInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': self._current_height / 100,
                'pady': self._current_height / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            } 
        )

        localInfoFrame = Frame(
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='localInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': self._current_height / 100,
                'pady': self._current_height / 100,
                'side': ctk.TOP,
                'expand': True,
                'fill': ctk.BOTH
            } 
        )

        accountInfoFrame = Frame(
            master=dataInputFrame.widget,
            container=dataInputFrame._children,
            ID='accountInfoFrame',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'fg_color': "transparent"
            },
            position_params={
                'padx': self._current_height / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
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
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
                'side': ctk.LEFT,
                'expand': True,
                'fill': ctk.X
            }
        )
        
        cancelButtonEntry = Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='cancelButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': cancel,
                'text': 'Cancelar',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
                'side': ctk.LEFT
            }
        )

        createButtonEntry = Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='createButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': lambda: createUser(nameEntry, lastname1Entry, lastname2Entry, postalCodeEntry, addressEntry,
                                    emailEntry, phoneNumberEntry, idNumberEntry, passwordEntry, repeatPasswordEntry),
                'text': 'Crear',
                'height': WINDOW_HEIGHT / 10,
                'font': ctk.CTkFont(family='Calibri', size=WINDOW_HEIGHT // 20, weight='bold')
            },
            position_params={
                'padx': self._current_width / 100,
                'pady': self._current_height / 100,
                'side': ctk.RIGHT
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
        

        ##############################
        # The main frame (logged in) #
        ##############################

        self.__initialize_main()
        

        ################
        # Log-In Stuff #
        ################

        self.__initialize_login()