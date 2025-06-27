from customtkinter import CTkBaseClass, CTkToplevel

from typing import Any

from utils.parameters import *

class Widget:
    '''
    Global widget class
    '''

    _widget: CTkBaseClass = None
    _params: dict = None
    _locator: Any = None
    _forget: Any = None
    _active: bool = None
    _children: dict = None

    def __init__(self, Obj: Any, master: Any, container: dict, ID: str, locator: Any, forgetter: Any,
                params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (Any): The method to locate the widget on the screen
            forgetter (Any): The method to hide the widget from the screen
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=False): Whether to show directly the widget
        '''

        assert ID not in container, 'ID already in use'

        self._widget = Obj(master, **params)
        self._locator = locator
        self._forget = forgetter
        self._params = position_params
        self._active = active
        self._children = {}

        # add to the container
        container[ID] = self

        # show directly if wanted
        if show: self.show()


    def __getitem__(self, key):
        return self._children[key]
    

    def show(self) -> None:

        if self._active:
            self._locator(self._widget, **self._params)

        for k, w in self._children.items():
            w.show()


    def hide(self) -> None:

        for k, w in self._children.items():
            w.hide()

        if self._active:
            self._forget(self._widget)

    
    def get(self) -> str | None:
        try:
            return self._widget.get()
        except Exception as e:
            return None
           
    
    def clear(self) -> None:
        try:
            if self._widget.get() != '':
                self._widget.delete(first_index=0, last_index='end')
        except Exception as e:
            pass
        

    @property
    def widget(self) -> CTkBaseClass:
        return self._widget


    @property
    def loc_params(self) -> dict:
        return self._params
    

    @property
    def children(self) -> dict:
        return self._children
    

    def active(self) -> bool:
        return self._active
    
    
    def activate(self) -> None:
        self._active = True


    def deactivate(self) -> None:
        self._active = False



class Window(CTkToplevel):

    _content: dict = None

    def __init__(self, fg_color = None):

        super().__init__(fg_color=fg_color)

        self._content = {}


    @property
    def content(self) -> dict:
        return self._content