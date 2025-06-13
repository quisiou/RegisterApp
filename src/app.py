import customtkinter as ctk

from src.dataManager import Manager

from pathlib import Path

from src.widget import Widget, Frame
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
        # Frame(
        #     master=self,
        #     container=self.__children,
        #     ID='mainFrame',
        #     locator=ctk.CTkBaseClass.pack,
        #     forgetter=ctk.CTkBaseClass.pack_forget,
        #     params={
        #         'fg_color': "transparent"
        #     },
        #     position_params={
        #         'fill': ctk.BOTH, # Fill all the assigned space in the container
        #         'expand': True, # expand when window is resized
        #         'padx': self._current_height / 100,
        #         'pady': self._current_height / 100
        #     }
        # )

        # The log in frame
        logInFrame = Frame(
            master=self,
            container=self.__children,
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
        logInFrame.show()

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
        idEntry.widget.bind(
            sequence="<Return>",
            command=add_log
        )
        idEntry.widget.bind(
            sequence="<Escape>",
            command=self.__unfocus
        )
        idEntry.show()

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
        codeEntry.widget.bind(
            sequence="<Return>",
            command=add_log
        )
        codeEntry.widget.bind(
            sequence="<Escape>",
            command=self.__unfocus
        )
        codeEntry.show()

        # The button which checks the code
        logInButton = Widget(
            Obj=ctk.CTkButton,
            master=logInFrame.widget,
            container=logInFrame.children,
            ID='personalCodeChecker',
            locator=ctk.CTkBaseClass.grid,
            forgetter=ctk.CTkBaseClass.grid_forget,
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
        logInButton.show()