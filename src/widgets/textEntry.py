from src.widgets.baseWidget import Widget, ContainerWidget

from ttkbootstrap import Entry as TkbEntry

from typing import Any, Literal




class TextEntry(Widget):
    '''
    Represents a text entry
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
            Obj=TkbEntry,
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

        self._widget.bind(sequence="<Escape>", func=parent.focus)


    def get(self) -> str:
        '''
        Gets the widget's value
        '''

        return self._widget.get()
           
    
    def set(self, value: str = None) -> None:
        '''
        Gets the widget's value to `value`
        '''

        # Clear entry
        if self._widget.get() != '':
            self._widget.delete(0, 'end')

        # Set new value
        self._widget.insert(0, value)
