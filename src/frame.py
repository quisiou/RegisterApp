import customtkinter as ctk
from typing import Any

class Frame():

    __frame: ctk.CTkFrame
    __widgets: dict

    def __init__(self, root: Any, params: dict = {}):
        self.__frame = ctk.CTkFrame(root, **params)
        self.__widgets = {}


    def add_entry(self, id: str, params: dict = {}) -> None:

        assert id not in self.__widgets, 'ID already in use'
        
        self.__widgets[id] = ctk.CTkEntry(self.__frame, **params)

    @property
    def frame(self) -> ctk.CTkFrame:
        return self.__frame
    
    @property
    def widgets(self) -> dict:
        return self.__widgets