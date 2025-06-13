import customtkinter as ctk

from src.frame import Frame
from src.dataManager import Manager

from pathlib import Path

from utils.widgets import *
from utils.parameters import *

class App(ctk.CTk):
    '''
    Main application class
    '''

    __children: dict = None # Children widgets of the app

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
        self.geometry(f"{width}x{height}")
        self.resizable(width=False, height=False)
        self.title('Clocker')

        # Attributes
        self.__children = {}

        # Create all the widgets for the application
        self.__initialize()


    def __unfocus(self, e=None) -> None:
        '''
        Unfocuses the actual focused widget (by focusing the main window)

        :params (Any, Default=None) e: The event which triggered this method
        '''

        self.focus()
    

    def __initialize(self) -> None:
        '''
        Initializes all the required widgets and frames for the application
        '''


        def add_log(event=None):
            '''
            Tries to log, checking if everything is valid

            :params (Any, Default=None) e: The event which triggered this method
            '''

            text = logInFrame.children['personalCodeEntry'].get()
            num = logInFrame.children['idEntry'].get()

            try:
                Manager.add_entry(num, text)

            except Manager.InvalidID as e:
                print(e)

            except Manager.NotFoundID as e:
                print(e)

            except Manager.InvalidPassword as e:
                print(e)

            self.__unfocus(event)


        # The main frame
        mainFrame = Frame(
            master=self,
            locator=ctk.CTkBaseClass.pack,
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
        add_widget_to_container(mainFrame, self.__children, 'mainFrame')

        # The log in frame
        logInFrame = Frame(
            master=self,
            locator=ctk.CTkBaseClass.pack,
            params={
                'fg_color': "transparent",
            },
            position_params={
                'fill': ctk.BOTH, # Fill all the assigned space in the container
                'expand': True, # expand when window is resized
                'padx': self._current_height / 100,
                'pady': self._current_height / 100
            }
        )
        add_widget_to_container(logInFrame, self.__children, 'logInFrame')

        # The entry for the ID number
        idEntry = create_widget(
            Widget=ctk.CTkEntry,
            master=logInFrame.widget,
            container=logInFrame.children,
            id='idEntry',
            locator=ctk.CTkBaseClass.grid,
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
            },
            out=True
        )
        idEntry.bind(
            sequence="<Return>",
            command=add_log
        )
        idEntry.bind(
            sequence="<Escape>",
            command=self.__unfocus
        )

        # The entry for the personal code
        codeEntry = create_widget(
            Widget=ctk.CTkEntry,
            master=logInFrame.widget,
            container=logInFrame.children,
            id='personalCodeEntry',
            locator=ctk.CTkBaseClass.grid,
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
            },
            out=True
        )
        codeEntry.bind(
            sequence="<Return>",
            command=add_log
        )
        codeEntry.bind(
            sequence="<Escape>",
            command=self.__unfocus
        )

        # The button which checks the code
        create_widget(
            Widget=ctk.CTkButton,
            master=logInFrame.widget,
            container=logInFrame.children,
            id='personalCodeChecker',
            locator=ctk.CTkBaseClass.grid,
            params={
                'command': add_log,
                'text': 'Comprobar'
            },
            position_params={
                'row': 0,
                'column': 1,
                'padx': self._current_width / 25,
                'pady': self._current_height / 25
            }
        )