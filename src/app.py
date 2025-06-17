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
        self.resizable(width=False, height=False)
        self.title('Clocker')

        # Attributes
        self._children = {}

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

        def change_to_login(event=None) -> None:
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
            },
            active=True
        )
        
        logInButton = Widget(
            Obj=ctk.CTkButton,
            master=mainFrame.widget,
            container=mainFrame.children,
            ID='logInButton',
            locator=ctk.CTkBaseClass.pack,
            forgetter=ctk.CTkBaseClass.pack_forget,
            params={
                'command': change_to_login,
                'text': 'Iniciar sesión'
            },
            position_params={
                'side': ctk.TOP,
                'anchor': ctk.CENTER,
                'pady': (self._current_height / 3, 0)
            },
            active=True
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
            },
            active=True
        )


    def __initialize_login(self) -> None:

        def add_log(event=None, frame: Frame = None) -> None:
            '''
            Tries to log, checking if everything is valid

            :params (Any, Default=None) e: The event which triggered this method
            '''

            text = frame.children['personalCodeEntry'].get()
            num = frame.children['idEntry'].get()

            try:
                Manager.add_entry(num, text)

            except Manager.InvalidID as e:
                print(e)

            except Manager.NotFoundID as e:
                print(e)

            except Manager.InvalidPassword as e:
                print(e)

            self.__unfocus(event)

        
        # The frame with all the login stuff
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
            }
        )

        # The entry for the ID number
        idEntry = Widget(
            Obj=ctk.CTkEntry,
            master=logInFrame.widget,
            container=logInFrame.children,
            ID='idEntry',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
            params={
                'placeholder_text': 'Introducir el DNI',
                'width': 200
            },
            position_params={
                'row': 0,
                'column': 0,
                'rowspan': 2,
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            }
        )
        idEntry.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # The entry for the personal code
        codeEntry = Widget(
            Obj=ctk.CTkEntry,
            master=logInFrame.widget,
            container=logInFrame.children,
            ID='personalCodeEntry',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
            params={
                'placeholder_text': 'Introducir el código',
                'width': 200
            },
            position_params={
                'row': 1,
                'column': 0,
                'rowspan': 2,
                'padx': self._current_width / 25,
                'pady': self._current_height / 25
            }
        )
        codeEntry.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # The button which checks the code
        Widget(
            Obj=ctk.CTkButton,
            master=logInFrame.widget,
            container=logInFrame.children,
            ID='personalCodeChecker',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
            params={
                'command': lambda: add_log(frame=logInFrame),
                'text': 'Comprobar'
            },
            position_params={
                'row': 0,
                'column': 1,
                'padx': self._current_width / 25,
                'pady': self._current_height / 25
            }
        )


    def __initialize_create(self) -> None:

        def createUser() -> None:
            print('Usuario creado!')


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
                'fg_color': "gray23",
                'height': 5 * self._current_height / 6
            },
            position_params={
                'fill': ctk.BOTH,
                'expand': True,
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
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
                'fill': ctk.BOTH,
                'expand': True,
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            }
        )
        buttonsFrame.widget.columnconfigure((0, 1), weight=1)


        # The widgets

        # nameEntry = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='nameEntry',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Nombre'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # nameEntry.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # lastname1 = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='lastname1',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Apellido 1'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # lastname1.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # lastname2 = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='lastname2',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Apellido 2'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # lastname2.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # postalCode = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='postalCode',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Código Postal'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # postalCode.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # idNumber = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='idNumber',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'NIF'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # idNumber.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # address = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='address',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Calle'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # address.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # email = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='email',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Correo electrónico'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # email.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # phoneNumber = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='phoneNumber',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Tfno'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # phoneNumber.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # password = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='password',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Contraseña'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # password.widget.bind(sequence="<Escape>", command=self.__unfocus)

        # repeatPassword = Widget(
        #     Obj=ctk.CTkEntry,
        #     master=createUserFrame.widget,
        #     container=createUserFrame.children,
        #     ID='repeatPassword',
        #     locator=ctk.CTkBaseClass.grid,
        #     forgetter=ctk.CTkBaseClass.grid_forget,
        #     params={
        #         'placeholder_text': 'Repetir contraseña'
        #     },
        #     position_params={
        #         'padx': self._current_width / 100,
        #         'pady': self._current_height / 100
        #     }
        # )
        # repeatPassword.widget.bind(sequence="<Escape>", command=self.__unfocus)

        createButton = Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='createButton',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
            params={
                'command': createUser,
                'text': 'Crear'
            },
            position_params={
                'row': 0,
                'column': 1,
                'sticky': 'nse',
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            }
        )

        cancelButton = Widget(
            Obj=ctk.CTkButton,
            master=buttonsFrame.widget,
            container=buttonsFrame.children,
            ID='cancelButton',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
            params={
                'command': cancel,
                'text': 'Cancelar',
                'border_color': '#1f538d',
                'border_width': 2,
                'fg_color': 'gray10'
            },
            position_params={
                'row': 0,
                'column': 0,
                'sticky': 'nsw',
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            }
        )


    def __initialize(self) -> None:
        '''
        Initializes all the required widgets and frames for the application
        '''

        ################
        # Log-In Stuff #
        ################

        self.__initialize_login()


        #####################
        # Create user Stuff #
        #####################

        self.__initialize_create()
        

        ##################
        # The main frame #
        ##################

        self.__initialize_main()
        

