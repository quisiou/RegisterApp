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
            print('En construcción...')


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
        idEntry.widget.bind(sequence="<Return>", command=lambda x: add_log(event=x, frame=logInFrame))
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
        codeEntry.widget.bind(sequence="<Return>", command=lambda x: add_log(event=x, frame=logInFrame))
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


    def __initialize(self) -> None:
        '''
        Initializes all the required widgets and frames for the application
        '''

        ################
        # Log-In Stuff #
        ################

        self.__initialize_login()
        

        ##################
        # The main frame #
        ##################

        self.__initialize_main()
        

