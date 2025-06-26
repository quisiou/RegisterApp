from customtkinter import CTkToplevel

from src.widget import *
from utils.parameters import *

class Window(CTkToplevel):

    _children: dict = None

    def __init__(self, fg_color = None):

        super().__init__(fg_color=fg_color)
        
        self._children = {}