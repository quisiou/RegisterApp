from src.widgets.baseWidget import ContainerWidget

from ttkbootstrap import Frame as TkbFrame
from ttkbootstrap import Window as TkbWindow

from typing import Literal




class Frame(ContainerWidget):
    '''
    Represents a Frame, where widgets can be located
    '''

    def __init__(self, parent: ContainerWidget | TkbWindow, locator: Literal['pack', 'grid', 'place'], ID: str = None,
            params: dict = {}, position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            parent (ContainerWidget | ttkbootstrap.Window): The parent of the new widget
            locator (Any): The method to locate the widget on the screen
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        super().__init__(
            Obj=TkbFrame,
            master=parent.widget if type(parent) == ContainerWidget else parent,
            container=parent.content,
            ID=ID,
            locator=locator,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )
