from src.widgets.baseWidget import Widget, ContainerWidget

from ttkbootstrap import Button as TkbButton

from typing import Any, Literal




class Button(Widget):
    '''
    Represents a normal, clickable button
    '''


    def __init__(self, parent: ContainerWidget, locator: Literal['pack', 'grid', 'place'], ID: str = None,
            params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False, default: Any = None):
        '''
        Params:
            parent (ContainerWidget): The parent of the new widget
            locator (Any): The method to locate the widget on the screen
            forgetter (Any): The method to hide the widget from the screen
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly,
            default (Any, Default=None): Default (initial) value for the widget
        '''

        super().__init__(
            Obj=TkbButton,
            master=parent.widget,
            container=parent.content,
            ID=ID,
            locator=locator,
            params=params,
            position_params=position_params,
            active=active,
            show=show,
            default=default
        )


    def get(self) -> None:
        '''
        Buttons don't return a value
        '''
        return None
           
    
    def set(self, value: str = None) -> None:
        '''
        Buttons don't have a value to be set
        '''
        return None
