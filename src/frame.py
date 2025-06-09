import customtkinter as ctk
from typing import Any, Literal

class Frame():

    __widget: ctk.CTkFrame
    __children: dict

    def __init__(self, master: Any, locator: callable,
            params: dict = {}, position_params: dict = {}):
        
        self.__widget = ctk.CTkFrame(master, **params)
        self.__children = {}

        # Location of the frame
        locator(self.__widget, **position_params)


    @property
    def widget(self) -> ctk.CTkFrame:
        return self.__widget
    

    @property
    def children(self) -> dict:
        return self.__children
    