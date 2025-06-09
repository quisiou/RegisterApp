import customtkinter as ctk
from typing import Any, Literal

class Frame():

    __frame: ctk.CTkFrame
    __widgets: dict

    def __init__(self, root: Any, pos: Literal['grid', 'pack', 'place'],
            params: dict = {}, position_params: dict = {}):
        
        self.__frame = ctk.CTkFrame(root, **params)
        self.__widgets = {}

        # Location of the frame
        match pos:
            case 'grid':
                self.__frame.grid(**position_params)
                
            case 'pack':
                self.__frame.pack(**position_params)

            case 'place':
                self.__frame.place(**position_params)


    @property
    def frame(self) -> ctk.CTkFrame:
        return self.__frame
    

    @property
    def widgets(self) -> dict:
        return self.__widgets
    