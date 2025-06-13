from customtkinter import CTkBaseClass, CTkFrame
from typing import Any

class Widget():
    '''
    Global widget class
    '''

    __widget: CTkBaseClass = None
    __params: dict = None
    __locator: callable = None
    __forget: callable = None
    __active: bool = None

    def __init__(self, Obj: Any, master: Any, container: dict, ID: str, locator: callable,
        forgetter: callable, params: dict = {}, position_params: dict = {}):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (callable): The method to locate the widget on the screen
            forgetter (callable): The method to hide the widget from the screen
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
        '''

        assert ID not in container, 'ID already in use'

        self.__widget = Obj(master, **params)
        self.__locator = locator
        self.__forget = forgetter
        self.__params = position_params
        self.__active = False

        # Add it to the container
        container[ID] = self


    def show(self) -> None:

        # May be interesting to show all children, and so on...
        self.__locator(self.__widget, **self.__params)
        self.__active = True


    def hide(self) -> None:

        # May be interesting to hide all children, and so on...
        self.__forget(self.__widget)
        self.__active = False

    
    def get(self) -> str | None:
        try:
            return self.__widget.get()
        except Exception as e:
            return None
        

    @property
    def widget(self) -> CTkBaseClass:
        return self.__widget


    @property
    def loc_params(self) -> dict:
        return self.__params
    


class Frame(Widget):
    '''
    Frame widget, derived from global `Widget` class
    '''

    __children: dict

    def __init__(self, master: Any, container: dict, ID: str, locator: callable,
        forgetter: callable, params: dict = {}, position_params: dict = {}):
        '''
        Params:
            master (Any): The master of the new widget
            container (dict): The container where the widget will be added
            ID (str): The identifier of the widget in the container
            locator (callable): The method to locate the widget on the screen
            forgetter (callable): The method to hide the widget from the screen
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
        '''

        super().__init__(
            Obj=CTkFrame,
            master=master,
            container=container,
            ID=ID,
            locator=locator,
            forgetter=forgetter,
            params=params,
            position_params=position_params
        )

        self.__children = {}


    @property
    def children(self) -> dict:
        return self.__children