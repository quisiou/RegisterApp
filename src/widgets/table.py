from src.widgets.baseWidget import BaseWidget, ContainerWidget

from ttkbootstrap.tableview import Tableview

from typing import Any, Literal




class Table(BaseWidget):
    '''
    Subclass of Widget. Represents a table (customised widget derived from Tkinter's Treeview).
    The following are the posible tableview's parameters:

    Parameters:
        coldata (list[str | dict]):             The column headings (names) or column settings
        rowdata (list):                         The row data
        bootstyle (str, Default='DEFAULT'):     The table's theme (style)
        paginated (bool, Default=False):        Whether to divide the information in several pages
        searchable (bool, Default=False):       Whether to include a searchbar
        pagesize (int, Default=10):             If `paginated=True`, maximum number of rows per page
        height (int, Default=10):               Maximum number of rows fit in the table viewport (then have to scroll)
        yscrollbar (bool, Default=False):       Whether to include a scrollbar to scroll vertically
        delimiter (str, Default=','):           Delimiter character for when exporting to CSV file
    '''

    
    def __init__(self, parent: ContainerWidget, locator: Literal['pack', 'grid', 'place'],
        ID: str = None, params: dict = {}, position_params: dict = {},
        active: bool = True, show: bool = False):
        '''
        Params:
            parent (ContainerWidget): The master of the new widget
            locator (Any): The method to locate the widget on the screen
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget
            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        super().__init__(
            Obj=Tableview,
            master=parent.widget,
            locator=locator,
            container=parent.content,
            ID=ID,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )


    def show(self) -> None:
        '''
        Shows the widget on the screen
        '''

        if self._active:
            self._locator(self._widget, **self._params)


    def hide(self) -> None:
        '''
        Hides the widget from the screen
        '''

        if self._active:
            self._forgetter(self._widget)