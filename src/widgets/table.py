from src.widgets.baseWidget import BaseWidget, ContainerWidget

from src.dataManager import Manager

from src.widgets.customs.customTableview import CustomTableview

from typing import Literal
from pathlib import Path, PosixPath




class Table(BaseWidget):
    '''
    Subclass of Widget. Represents a table (customised widget derived from Tkinter's Treeview).

    Attributes:
        _datafile (str | Path | PosixPath):     Name of the file storing the data
    '''

    _datafile: str | Path | PosixPath = None

    
    def __init__(self, parent: ContainerWidget, locator: Literal['pack', 'grid', 'place'],
        datafile: str | Path | PosixPath, ID: str = None, params: dict = {},
        position_params: dict = {}, active: bool = True, show: bool = False):
        '''
        Params:
            parent (ContainerWidget): The master of the new widget
            locator (Any): The method to locate the widget on the screen
            datafile (str | Path | PosixPath): Name of the file storing the data
            ID (str, Default=None): The identifier of the widget in the parent's container
            params (dict, Default={}): Parameters for the customisation of the widget:
                coldata: list[str | dict]   # The column headings (names) or column settings
                rowdata: list               # The row data
                bootstyle: str = 'DEFAULT'  # The table's theme (style)
                paginated: bool = False     # Whether to divide the information in several pages
                searchable: bool = False    # Whether to include a searchbar
                pagesize: int = 10          # If paginated=True, maximum number of rows per page
                height: int = 10            # Max number of rows in the table viewport without scroll
                yscrollbar: bool = False    # Whether to include a scrollbar to scroll vertically
                delimiter: str = ','        # Delimiter character for when exporting to CSV file

            position_params (dict, Default={}): Parameters for the placement of the widget
            active (bool, Default=True): Whether to show the widget when `show` method is called
            show (bool, Default=False): Whether to show the widget directly
        '''

        self._datafile = datafile

        super().__init__(
            Obj=CustomTableview,
            master=parent.widget,
            locator=locator,
            container=parent.content,
            ID=ID,
            params=params,
            position_params=position_params,
            active=active,
            show=show
        )

        self.reload_data()


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


    def clear(self) -> None:
        self.widget.delete_rows(visible=False)


    def reload_data(self) -> None:
        data = Manager.get_dataframe(as_list=True, filename=self._datafile)
        
        # Delete possible items
        self.clear()

        # Insert rows
        self.widget.insert_rows(index=0, rowdata=data)

        # Reload
        self.widget.load_table_data(clear_filters=True)