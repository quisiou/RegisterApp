from typing import Any, Literal
from abc import ABC, abstractmethod

from tkinter import Widget as TkWidget




class BaseWidget(ABC):
    '''
    Global abstract class which represents a Widget

    Attributes:
        _widget (tkinter.Widget, Default=None):     The Tkinter widget itself
        _params (dict, Default=None):               The Tkinter widget location parameters
        _locator (callable, Default=None):          The method to use to locate the widget on screen
        _forgetter (callable, Default=None):        The method to use to hide the widget from the screen
        _active (bool, Default=None):               Whether the widget is visible
    '''

    _widget: TkWidget = None
    _params: dict = None
    _locator: callable = None
    _forgetter: callable = None
    _active: bool = None


    def __init__(self, Obj: Any, master: Any, locator: Literal['pack', 'grid', 'place'],
            container: dict = None, ID: str = None, params: dict = {},
            position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            locator (Any): The method to locate the widget on the screen
            container (dict, Default=None): The container where the widget will be added
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        assert ID not in container, 'ID already in use'

        self._widget = Obj(master, **params)
        self._params = position_params
        self._active = active

        # Select locator
        if locator == 'pack':
            self._locator = TkWidget.pack
            self._forgetter = TkWidget.pack_forget

        elif locator == 'grid':
            self._locator = TkWidget.grid
            self._forgetter = TkWidget.grid_forget

        else:
            self._locator = TkWidget.place
            self._forgetter = TkWidget.place_forget

        # add to the container
        container[ID] = self


    def focus(self, event=None) -> None:
        '''
        Takes the focus

        :params (Any, Default=None) event: The event which triggered this method
        '''
        
        self._widget.focus_set()


    @abstractmethod
    def show(self) -> None:
        '''
        Shows the widget (and its children) on the screen
        '''
        pass


    @abstractmethod
    def hide(self) -> None:
        '''
        Hides the widget (and its children) from the screen
        '''
        pass


    @property
    def widget(self) -> TkWidget:
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




class Widget(BaseWidget, ABC):
    '''
    Global abstract class which represents a user-interactive Widget (therefore, has a value stored)

    Attributes:
        _default (Any, Default=None):               Default value of the widget's holder variable (`_var`)
    '''

    _default: Any = None


    def __init__(self, Obj: Any, master: Any, locator: Literal['pack', 'grid', 'place'],
            container: dict = None, ID: str = None, params: dict = {}, position_params: dict = {},
            active: bool = True, show: bool = False, default: Any = None):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            locator (Any): The method to locate the widget on the screen
            container (dict, Default=None): The container where the widget will be added
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
            default (Any, Default=None): Default (initial) value for the widget
        '''

        super().__init__(
            Obj=Obj,
            master=master,
            locator=locator,
            container=container,
            ID=ID,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )

        self._default = default

        # show directly if wanted
        if show:
            self.show()

    
    def show(self) -> None:
        '''
        Shows the widget (and its children) on the screen
        '''

        if self._active:
            self._locator(self._widget, **self._params)

    
    def hide(self) -> None:
        '''
        Hides the widget (and its children) from the screen
        '''

        if self._active:
            self._forgetter(self._widget)


    @abstractmethod
    def get(self) -> Any:
        '''
        Gets the widget's value
        '''
        return None
           
    
    @abstractmethod
    def set(self, value: Any = None) -> None:
        '''
        Gets the widget's value to `value`
        '''
        pass


    def restore(self) -> None:
        '''
        Restore widget's value to the default one
        '''

        if self.get() != self._default:
            self.set(value=self._default)
        

    @property
    def default(self) -> Any:
        '''
        The widget's default value
        '''

        return self._default




class ContainerWidget(BaseWidget, ABC):
    '''
    Global abstract class which represents a Widget which can contain other widgets inside

    Attributes:
        _content (dict, Default=None):             This widget's children widgets
    '''

    _content: dict = None


    def __init__(self, Obj: Any, master: Any, locator: Literal['pack', 'grid', 'place'],
            container: dict = None, ID: str = None, params: dict = {},
            position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            Obj (Any): The widget class (any of the possible widgets)
            master (Any): The master of the new widget
            locator (Any): The method to locate the widget on the screen
            container (dict, Default=None): The container where the widget will be added
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        super().__init__(
            Obj=Obj,
            master=master,
            locator=locator,
            container=container,
            ID=ID,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )
        
        self._content = {}

        # show directly if wanted
        if show:
            self.show()


    def show(self) -> None:
        '''
        Shows the widget (and its children) on the screen
        '''

        if self._active:
            self._locator(self._widget, **self._params)

        for k, w in self._content.items():
            w.show()

    
    def hide(self) -> None:
        '''
        Hides the widget (and its children) from the screen
        '''

        for k, w in self._content.items():
            w.hide()

        if self._active:
            self._forgetter(self._widget)


    @property
    def content(self) -> dict:
        '''
        The widget's children
        '''

        return self._content
