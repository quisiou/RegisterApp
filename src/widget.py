from customtkinter import CTkBaseClass, CTkToplevel
from tkinter.ttk import Treeview

from pathlib import Path, PosixPath

from typing import Any

from src.dataManager import Manager
from utils.parameters import *

class Widget:
    '''
    Global widget class

    Attributes:
        _widget (CTkBaseClass, Default=None):       The Tkinter widget itself
        _params (dict, Default=None):               The Tkinter widget location parameters
        _locator (Any, Default=None):               The method to use to locate the widget on screen
        _forgetter (Any, Default=None):             The method to use to hide the widget from the screen
        _active (bool, Default=None):               Whether the widget is visible
        _children (dict, Default=None):             This widget's children widgets
        _default (Any, Default=None):               Default value of the Tkinter widget (`_widget`)
    '''

    _widget: CTkBaseClass = None
    _params: dict = None
    _locator: Any = None
    _forgetter: Any = None
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
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        assert ID not in container, 'ID already in use'

        self._widget = Obj(master, **params)
        self._locator = locator
        self._forgetter = forgetter
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
        '''
        Shows the widget (and its children) on the screen
        '''

        if self._active:
            self._locator(self._widget, **self._params)

        for k, w in self._children.items():
            w.show()


    def hide(self) -> None:
        '''
        Hides the widget (and its children) from the screen
        '''

        for k, w in self._children.items():
            w.hide()

        if self._active:
            self._forgetter(self._widget)

    
    def get(self) -> str | None:
        '''
        Gets the widget's value (the text in an Entry for example)
        '''

        try:
            return self._widget.get()
        
        except Exception as e:
            return None
           
    
    def clear(self) -> None:
        '''
        Clears the widget's value
        '''

        try:
            if self._widget.get() != '':
                self._widget.delete(first_index=0, last_index='end')
        except Exception as e:
            pass
        

    @property
    def widget(self) -> CTkBaseClass:
        '''
        The Tkinter widget
        '''

        return self._widget


    @property
    def loc_params(self) -> dict:
        '''
        The widget's location parameters
        '''

        return self._params
    

    @property
    def children(self) -> dict:
        '''
        The widget's children
        '''

        return self._children
    

    @property
    def default(self) -> Any:
        '''
        The widget's default value
        '''

        return self._default


    def active(self) -> bool:
        '''
        Whether the widget is visible
        '''

        return self._active
    
    
    def activate(self) -> None:
        '''
        Sets the widget to `visible`
        '''

        self._active = True


    def deactivate(self) -> None:
        '''
        Sets the widget to `invisible`
        '''

        self._active = False




class Table(Widget):
    '''
    Subclass of Widget. Represents a table (customised widget derived from Tkinter's Treeview)

    Attributes:
        _filters (dict, Default=None):      The applied filters to the table
    '''

    _filters: dict = None

    def __init__(self, master: Any, container: dict, ID: str, locator: Any, forgetter: Any, default: Any = None,
                params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (Any): The method to locate the widget on the screen
            forgetter (Any): The method to hide the widget from the screen
            default (Any, Default=None): Default (initial) value for the widget
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''


        super().__init__(
            Obj=Treeview,
            master=master,
            container=container,
            ID=ID,
            locator=locator,
            forgetter=forgetter,
            default=default,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )

    
    def clear(self) -> None:
        '''
        Deletes all entries in the table
        '''

        self._widget.delete(*self._widget.get_children())


    def insert_row(self, row_data: list | tuple, parent: str = '', index: int = 0) -> None:
        '''
        Inserts a new row into the table

        Params:
            row_data (list | tuple): The row to be inserted
            parent (str, Default=''): The parent row of the new one (if any)
            index (int, Default=0): The index where the new row will be placed
        '''
        
        self._widget.insert(
            parent=parent,
            index=index, # New rows are inserted at the beginning (top) of the table
            values=row_data
        )


    def load(self, filename: str | Path | PosixPath) -> None:
        '''
        Loads the information into the table, taking into account the possible filters to be applied

        :params (str | Path | PosixPath) filename: Name of the file storing the data
        '''
        
        data = Manager.get_dataframe(as_list=True, filename=filename)

        # Delete possible items
        self.clear()

        if self._filters is not None:
            data = Manager.filter_df(filename=filename, params=self._filters, as_list=True)

        # Insert rows
        for entry in data: self.insert_row(entry)


    def reload(self, filename: str | Path | PosixPath) -> None:
        '''
        Clear filters and load table again

        :params (str | Path | PosixPath) filename: Name of the file storing the data
        '''

        self._filters = None
        self.load(filename=filename)


    @property
    def filters(self) -> dict:
        '''
        The table's filters
        '''

        return self._filters


    @filters.setter
    def filters(self, value) -> None:
        self._filters = value
    



class Window(CTkToplevel):
    '''
    Represents a pop-up window, external from the main one (customised widget derived from Tkinter's TopLevel)

    Attributes:
        _content (dict, Default=None):      The window's children widgets
    '''

    _content: dict = None

    def __init__(self, fg_color: str | tuple = None):
        '''
        :params (str | tuple, Default=None) fg_color: The window's background color
        '''

        super().__init__(fg_color=fg_color)

        self._content = {}


    def __getitem__(self, key) -> Any:
        return self._content[key]


    @property
    def content(self) -> dict:
        '''
        Window's children widgets
        '''

        return self._content
