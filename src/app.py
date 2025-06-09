import customtkinter as ctk
from src.frame import Frame

from pathlib import Path
from typing import Any

class App(ctk.CTk):
    '''
    Main application class
    '''

    __content: dict = None

    def __init__(self, width: int = 1280, height: int = 720, custom_theme: str = None):

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
        self.__content = {}

        # Create the main frame of the application
        self.__create_main_frame()

        print(self.__content['main'].widgets)


    def __add_frame(self, root: Any, id: str, params: dict = {}) -> None:

        assert id not in self.__content, 'ID already in use'

        self.__content[id] = Frame(root, params)


    def __create_main_frame(self) -> None:
        frame_params = {

        }

        self.__add_frame(self, 'main', frame_params)