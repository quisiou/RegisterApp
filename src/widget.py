from customtkinter import CTkBaseClass, CTkToplevel
from tkinter.ttk import Treeview

from pathlib import Path, PosixPath

from typing import Any, Literal

from src.dataManager import Manager
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
    _default: Any = None

    def __init__(self, Obj: Any, master: Any, container: dict, ID: str, locator: Any, forgetter: Any,
            default: Any = None, params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (Any): The method to locate the widget on the screen
            forgetter (Any): The method to hide the widget from the screen
            default (Any, Default=None): Default (initial) value for the widget
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
        self._default = default

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
    

    @property
    def default(self) -> Any:
        return self._default


    def active(self) -> bool:
        return self._active
    
    
    def activate(self) -> None:
        self._active = True


    def deactivate(self) -> None:
        self._active = False




class Table(Widget):

    _filters: dict = None

    def __init__(self, master: Any, container: dict, ID: str, locator: Any, forgetter: Any,
                params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False):
        
        super().__init__(
            Obj=Treeview,
            master=master,
            container=container,
            ID=ID,
            locator=locator,
            forgetter=forgetter,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )

    
    def clear(self):
        self._widget.delete(*self._widget.get_children())


    def insert_row(self, row_data: list | tuple, parent: str = '', index: int = 0) -> None:
        self._widget.insert(
            parent='',
            index=0, # New rows are inserted at the beginning (top) of the table
            values=row_data
        )


    def load(self, path: Path | PosixPath) -> None:

        data = Manager.get_dataframe(as_list=True, path=path)

        # Delete possible items
        self.clear()

        if self._filters is not None:
            data = Manager.filter_df(path=path, params=self._filters, as_list=True)

        # Insert rows
        for entry in data: self.insert_row(entry)


    def reload(self, path: Path | PosixPath) -> None:
        '''
        Clear filters and load table again

        :params (Path | PosixPath) path: File path where data is stored
        '''

        self._filters = None
        self.load(path=path)


    @property
    def filters(self) -> dict:
        return self._filters


    @filters.setter
    def filters(self, value) -> None:
        self._filters = value
    



class Window(CTkToplevel):

    _content: dict = None

    def __init__(self, fg_color = None):

        super().__init__(fg_color=fg_color)

        self._content = {}


    def __getitem__(self, key) -> Any:
        return self._content[key]


    @property
    def content(self) -> dict:
        return self._content




# Maybe if using ttkbootstrap in the future
# class Dropdown:

#     from ttkbootstrap import Menu, Menubutton

#     _button: Menubutton = None
#     _menu: Menu = None
#     _params: dict = None
#     _locator: Any = None
#     _forget: Any = None
#     _active: bool = None

#     def __init__(self, master: Any, container: dict, ID: str, locator: Literal['pack', 'grid', 'place'],
#                 options: list = [], button_params: dict = {}, menu_params: dict = {},
#                 position_params: dict = {}, active: bool = True, show: bool = False):

#         assert ID not in container, 'ID already in use'

#         self._button = Dropdown.Menubutton(master, **button_params)
#         self._menu = Dropdown.Menu(master, **menu_params)
#         self._params = position_params
#         self._active = active

#         if locator == 'pack':
#             self._locator = Dropdown.Menubutton.pack
#             self._forget = Dropdown.Menubutton.pack_forget

#         elif locator == 'grid':
#             self._locator = Dropdown.Menubutton.grid
#             self._forget = Dropdown.Menubutton.grid_forget

#         elif locator == 'place':
#             self._locator = Dropdown.Menubutton.place
#             self._forget = Dropdown.Menubutton.place_forget

#         # Add options to the dropdown
#         for opt in options:
#             self._menu.add_radiobutton(
#                 label=opt
#             )

#         # Link the menu with the button
#         self._button['menu'] = self._menu

#         # add to the container
#         container[ID] = self

#         # show directly if wanted
#         if show: self.show()


#     def show(self) -> None:

#         if self._active:
#             self._locator(self._button, **self._params)


#     def hide(self) -> None:

#         if self._active:
#             self._forget(self._button)


#     @property
#     def loc_params(self) -> dict:
#         return self._params
    

#     def active(self) -> bool:
#         return self._active
    
    
#     def activate(self) -> None:
#         self._active = True


#     def deactivate(self) -> None:
#         self._active = False
