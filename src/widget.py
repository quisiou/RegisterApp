from customtkinter import CTkBaseClass, CTkFrame
from typing import Any

class Widget:
    '''
    Global widget class
    '''

    _widget: CTkBaseClass = None
    _params: dict = None
    _locator: Any = None
    _forget: Any = None
    _active: bool = None

    def __init__(self, Obj: Any, master: Any, container: dict, ID: str, locator: Any,
        forgetter: Any, params: dict = {}, position_params: dict = {}, active: bool = False):
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

        # add to the container
        container[ID] = self

        # show directly if wanted
        if active: self.show()

    
    def show(self) -> None:

        self._locator(self._widget, **self._params)


    def hide(self) -> None:

        self._forget(self._widget)

    
    def get(self) -> str | None:
        try:
            return self._widget.get()
        except Exception as e:
            return None
        

    @property
    def widget(self) -> CTkBaseClass:
        return self._widget


    @property
    def loc_params(self) -> dict:
        return self._params
    

    @property
    def active(self) -> bool:
        return self._active
    
    
    @active.setter
    def activate(self) -> None:
        self._active = True
        self.show()


    @active.setter
    def deactivate(self) -> None:
        self._active = False
        self.hide()
    


class Frame(Widget):
    '''
    Frame widget, derived from global `Widget` class
    '''

    _children: dict

    def __init__(self, master: Any, container: dict, ID: str, locator: Any,
        forgetter: Any, params: dict = {}, position_params: dict = {}, active: bool = False):
        '''
        Params:
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (Any): The method to locate the widget on the screen
            forgetter (Any): The method to hide the widget from the screen
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=False): Whether to show directly the widget
        '''

        self._children = {}

        super().__init__(
            Obj=CTkFrame,
            master=master,
            container=container,
            ID=ID,
            locator=locator,
            forgetter=forgetter,
            params=params,
            position_params=position_params,
            active=active
        )


    @property
    def children(self) -> dict:
        return self._children
    

    def show(self) -> None:

        self._locator(self._widget, **self._params)

        for k, w in self._children.items():
            w.show()


    def hide(self) -> None:

        self._forget(self._widget)

        for k, w in self._children.items():
            w.hide()
