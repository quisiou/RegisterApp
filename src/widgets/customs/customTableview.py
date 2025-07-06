from ttkbootstrap.tableview import *

class CustomTableview(Tableview):
    '''
    ttkbootstrap's Tableview, with reduced and modified filtering options
    '''

    def __init__(self, master=None, bootstyle=DEFAULT, coldata=[], rowdata=[],
            paginated=False, searchable=False, yscrollbar=False, autofit=False,
            autoalign=True, stripecolor=None, pagesize=10, height=10, delimiter=","):
        '''
        Parameters:

            master (Widget):
                The parent widget.

            bootstyle (str):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            coldata (List[str | Dict]):
                An iterable containing either the heading name or a
                dictionary of column settings. Configurable settings
                include >> text, image, command, anchor, width, minwidth,
                maxwidth, stretch. Also see `Tableview.insert_column`.

            rowdata (List):
                An iterable of row data. The lenth of each row of data
                must match the number of columns. Also see
                `Tableview.insert_row`.

            paginated (bool):
                Specifies that the data is to be paginated. A pagination
                frame will be created below the table with controls that
                enable the user to page forward and backwards in the
                data set.

            pagesize (int):
                When `paginated=True`, this specifies the number of rows
                to show per page.

            searchable (bool):
                If `True`, a searchbar will be created above the table.
                Press the <Return> key to initiate a search. Searching
                with an empty string will reset the search criteria, or
                pressing the reset button to the right of the search
                bar. Currently, the search method looks for any row
                that contains the search text. The filtered results
                are displayed in the table view.
                
            yscrollbar (bool):
                If `True`, a vertical scrollbar will be created to the right
                of the table.

            autofit (bool):
                If `True`, the table columns will be automatically sized
                when loaded based on the records in the current view.
                Also see `Tableview.autofit_columns`.

            autoalign (bool):
                If `True`, the column headers and data are automatically
                aligned. Numbers and number headers are right-aligned
                and all other data types are left-aligned. The auto
                align method evaluates the first record in each column
                to determine the data type for alignment. Also see
                `Tableview.autoalign_columns`.

            stripecolor (Tuple[str, str]):
                If provided, even numbered rows will be color using the
                (background, foreground) specified. You may specify one
                or the other by passing in **None**. For example,
                `stripecolor=('green', None)` will set the stripe
                background as green, but the foreground will remain as
                default. You may use standand color names, hexadecimal
                color codes, or bootstyle color keywords. For example,
                ('light', '#222') will set the background to the "light"
                themed ttkbootstrap color and the foreground to the
                specified hexadecimal color. Also see
                `Tableview.apply_table_stripes`.

            height (int):
                Specifies how many rows will appear in the table's viewport.
                If the number of records extends beyond the table height,
                the user may use the mousewheel or scrollbar to navigate
                the data.

            delimiter (str):
                The character to use as a delimiter when exporting data
                to CSV.
        '''

        super().__init__(master=master, bootstyle=bootstyle, coldata=coldata, rowdata=rowdata,
            paginated=paginated, searchable=searchable, yscrollbar=yscrollbar, autofit=autofit,
            autoalign=autoalign, stripecolor=stripecolor, pagesize=pagesize, height=height, delimiter=delimiter)
        

    # Rewrite the filter method: Filters stack on each other, so there can be more than one at the same time
    def filter_column_to_value(self, event=None, cid=None, value=None):
        """Hide all records except for records where the current
        column exactly matches the provided value. This method may
        be triggered by a window event or by specifying the column id.

        Parameters:

            event (Event):
                A window click event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.

            value (Any):
                The criteria used to filter the column.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            index = eo.column.tableindex
            value = value or eo.row.values[index]
        elif cid is not None:
            column: TableColumn = self.cidmap.get(cid)
            index = column.tableindex
        else:
            return

        self.unload_table_data() # Hide data for now

        new_filtered = []

        if self._filtered:
            for row in self.tablerows_filtered:
                if row.values[index] == value:
                    new_filtered.append(row)

            self.tablerows_filtered.clear()
            for row in new_filtered:
                self.tablerows_filtered.append(row)
                
            new_filtered.clear()
            
        else:
            self.tablerows_filtered.clear()
            for row in self.tablerows:
                if row.values[index] == value:
                    self.tablerows_filtered.append(row)

        self._filtered = True

        self._rowindex.set(0)
        self.load_table_data() # Show new processed data
