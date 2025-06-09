import customtkinter as ctk

from src.frame import Frame

from pathlib import Path

from utils.widgets import *

class App(ctk.CTk):
    '''
    Main application class
    '''

    __children: dict = None

    def __init__(self, width: int = 500, height: int = 200, custom_theme: str = None):

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


    def __unfocus(self, e=None):
        self.focus()


    def __initialize(self) -> None:

        def check_code(e=None):
            print(mainFrame.children['personalCodeEntry'].get())
            self.__unfocus(e)


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

        # The entry for the personal code
        codeEntry = create_widget(
            Widget=ctk.CTkEntry,
            master=mainFrame.widget,
            container=mainFrame.children,
            id='personalCodeEntry',
            locator=ctk.CTkBaseClass.grid,
            params={
                'placeholder_text': 'Introducir el código',
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
        codeEntry.bind(
            sequence="<Return>",
            command=check_code
        )
        codeEntry.bind(
            sequence="<Escape>",
            command=self.__unfocus
        )

        # The button which checks the code
        create_widget(
            Widget=ctk.CTkButton,
            master=mainFrame.widget,
            container=mainFrame.children,
            id='personalCodeChecker',
            locator=ctk.CTkBaseClass.grid,
            params={
                'command': check_code,
                'text': 'Comprobar'
            },
            position_params={
                'row': 0,
                'column': 1,
                'padx': self._current_width / 100,
                'pady': self._current_height / 100
            }
        )