from ttkbootstrap.tableview import *
from ttkbootstrap.localization import MessageCatalog
from tkinter import Menu as TkMenu

class CustomTableview(Tableview):
    '''
    ttkbootstrap's Tableview, with modified filtering options
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


    # Replace the build method for the custom rows and columns
    def _build_tableview_widget(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self._searchable:
            self._build_search_frame()
            
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, side=TOP)

        self.view = ttk.Treeview(
            master=table_frame,
            columns=[x for x in range(len(coldata))],
            height=self._height,
            selectmode=EXTENDED,
            show=HEADINGS,
            bootstyle=f"{bootstyle}-table",
        )
        self.view.pack(fill=BOTH, expand=YES, side=LEFT)
        
        if self._yscrollbar:
            self.ybar = ttk.Scrollbar(
                master=table_frame, command=self.view.yview, orient=VERTICAL
            )
            self.ybar.pack(fill=Y, side=RIGHT)
            self.view.configure(yscrollcommand=self.ybar.set)
        
        self.hbar = ttk.Scrollbar(
            master=self, command=self.view.xview, orient=HORIZONTAL
        )
        self.hbar.pack(fill=X)
        self.view.configure(xscrollcommand=self.hbar.set)

        if self._paginated:
            self._build_pagination_frame()

        self.build_table_data(coldata, rowdata)

        self._rightclickmenu_cell = CustomTableCellRightClickMenu(self)
        self._rightclickmenu_head = CustomTableHeaderRightClickMenu(self)
        self._set_widget_binding()




class CustomTableCellRightClickMenu(TkMenu):
    """
    A right-click menu object for the tableview cells - INTERNAL

    (Modification of ttkbootstrap original `TableCellRightClickMenu`)
    """

    def __init__(self, master: CustomTableview):
        """
        :params CustomTableview master: The parent object
        """

        super().__init__(master, tearoff=False)
        self.master: CustomTableview = master
        self.view: ttk.Treeview = master.view
        self.cid = None
        self.iid = None

        self.__add_menus()


    def __add_menus(self) -> None:
        '''
        Adds the pop up menus to the tableview
        '''

        config = {
            "sortascending": {
                "label": f'''⬆  {MessageCatalog.translate("Sort Ascending")}''',
                "command": self.sort_column_ascending,
            },
            "sortdescending": {
                "label": f'''⬇  {MessageCatalog.translate("Sort Descending")}''',
                "command": self.sort_column_descending,
            },
            "clearfilter": {
                "label": f'''{MessageCatalog.translate("⎌")} {MessageCatalog.translate("Clear filters")}''',
                "command": self.master.reset_row_filters,
            },
            "filterbyvalue": {
                "label": f'''{MessageCatalog.translate("Filter by cell's value")}''',
                "command": self.filter_to_cell_value,
            },
            "hiderows": {
                "label": f'''{MessageCatalog.translate("Hide select rows")}''',
                "command": self.hide_selected_rows,
            },
            "showrows": {
                "label": f'''{MessageCatalog.translate("Show only select rows")}''',
                "command": self.filter_to_selected_rows,
            },
            "exportall": {
                "label": f'''{MessageCatalog.translate("Export all records")}''',
                "command": self.export_all_records,
            },
            "exportpage": {
                "label": f'''{MessageCatalog.translate("Export current page")}''',
                "command": self.export_current_page,
            },
            "exportselection": {
                "label": f'''{MessageCatalog.translate("Export current selection")}''',
                "command": self.export_current_selection,
            },
            "exportfiltered": {
                "label": f'''{MessageCatalog.translate("Export records in filter")}''',
                "command": self.export_records_in_filter,
            },
            "moveup": {
                "label": f'''↑ {MessageCatalog.translate("Move up")}''',
                "command": self.move_row_up
            },
            "movedown": {
                "label": f'''↓ {MessageCatalog.translate("Move down")}''',
                "command": self.move_row_down,
            },
            "movetotop": {
                "label": f'''⤒ {MessageCatalog.translate("Move to top")}''',
                "command": self.move_row_to_top,
            },
            "movetobottom": {
                "label": f'''⤓ {MessageCatalog.translate("Move to bottom")}''',
                "command": self.move_row_to_bottom,
            },
            "alignleft": {
                "label": f'''◧  {MessageCatalog.translate("Align left")}''',
                "command": self.align_column_left,
            },
            "aligncenter": {
                "label": f'''◫  {MessageCatalog.translate("Align center")}''',
                "command": self.align_column_center,
            },
            "alignright": {
                "label": f'''◨  {MessageCatalog.translate("Align right")}''',
                "command": self.align_column_right,
            }
        }

        sort_menu = TkMenu(self, tearoff=False)
        sort_menu.add_command(cnf=config["sortascending"])
        sort_menu.add_command(cnf=config["sortdescending"])
        self.add_cascade(menu=sort_menu, label=f'''⇅  {MessageCatalog.translate("Sort")}''')

        filter_menu = TkMenu(self, tearoff=False)
        filter_menu.add_command(cnf=config["clearfilter"])
        filter_menu.add_separator()
        filter_menu.add_command(cnf=config["filterbyvalue"])
        filter_menu.add_command(cnf=config["hiderows"])
        filter_menu.add_command(cnf=config["showrows"])
        self.add_cascade(menu=filter_menu, label=f'''⧨  {MessageCatalog.translate("Filter")}''')

        export_menu = TkMenu(self, tearoff=False)
        export_menu.add_command(cnf=config["exportall"])
        export_menu.add_command(cnf=config["exportpage"])
        export_menu.add_command(cnf=config["exportselection"])
        export_menu.add_command(cnf=config["exportfiltered"])
        self.add_cascade(menu=export_menu, label=f'''↔  {MessageCatalog.translate("Export")}''')

        move_menu = TkMenu(self, tearoff=False)
        move_menu.add_command(cnf=config["moveup"])
        move_menu.add_command(cnf=config["movedown"])
        move_menu.add_command(cnf=config["movetotop"])
        move_menu.add_command(cnf=config["movetobottom"])
        self.add_cascade(menu=move_menu, label=f'''⇵  {MessageCatalog.translate("Move")}''')

        align_menu = TkMenu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label=f'''↦  {MessageCatalog.translate("Align")}''')

    
    def tk_popup(self, event):
        """Display the menu below the selected cell.

        Parameters:

            event (Event):
                The click event that triggers menu.
        """
        # capture the column and item that invoked the menu
        self.event = event
        iid = self.view.identify_row(event.y)
        col = self.view.identify_column(event.x)

        # show the menu below the invoking cell
        rootx = self.view.winfo_rootx()
        rooty = self.view.winfo_rooty()
        try:
            bbox = self.view.bbox(iid, col)
        except:
            return
        try:
            super().tk_popup(rootx + bbox[0], rooty + bbox[1] + bbox[3])
        except IndexError:
            pass

    
    def sort_column_ascending(self):
        """Sort the column in ascending order."""
        self.master.sort_column_data(self.event, sort=ASCENDING)

    
    def sort_column_descending(self):
        """Sort the column in descending order."""
        self.master.sort_column_data(self.event, sort=DESCENDING)

    
    def filter_to_cell_value(self):
        """Hide all records except for records where the current
        column exactly matches the current cell value."""
        self.master.filter_column_to_value(self.event)

    
    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows."""
        self.master.filter_to_selected_rows()

    
    def export_all_records(self):
        """Export all records to a csv file"""
        self.master.export_all_records()

    
    def export_current_page(self):
        """Export records on current page"""
        self.master.export_current_page()

    
    def export_current_selection(self):
        """Export rows currently selected"""
        self.master.export_current_selection()

    
    def export_records_in_filter(self):
        """Export rows currently filtered"""
        self.master.export_records_in_filter()

    
    def hide_selected_rows(self):
        """Hide the selected rows"""
        self.master.hide_selected_rows()

    
    def move_row_to_top(self):
        """Move the row to the top of the data set"""
        self.master.move_selected_rows_to_top()

    
    def move_row_to_bottom(self):
        """Move the row to the bottom of the dataset"""
        self.master.move_selected_rows_to_bottom()

    
    def move_row_up(self):
        """Move the selected above the previous sibling"""
        self.master.move_selected_row_up()

    
    def move_row_down(self):
        """Move the selected row below the next sibling"""
        self.master.move_row_down()

    
    def align_column_left(self):
        "Left align the column text"
        self.master.align_column_left(self.event)

    
    def align_column_right(self):
        """Right align the column text"""
        self.master.align_column_right(self.event)

    
    def align_column_center(self):
        """Center align the column text"""
        self.master.align_column_center(self.event)




class CustomTableHeaderRightClickMenu(TkMenu):
    """
    A right-click menu object for the tableview header - INTERNAL
    
    (Modification of ttkbootstrap original `TableHeaderRightClickMenu`)
    """

    def __init__(self, master: CustomTableview):
        """
        :params CustomTableview master: The parent object
        """

        super().__init__(master, tearoff=False)
        self.master: CustomTableview = self.master
        self.view: ttk.Treeview = master.view
        self.event = None
        self.columnvars = []
        self._show_menu = None

        self.__add_menus()

    
    def __add_menus(self) -> None:
        '''
        Adds the pop up menus to the tableview
        '''

        config = {
            "movetoright": {
                "label": f'''→  {MessageCatalog.translate("Move to right")}''',
                "command": self.move_column_right,
            },
            "movetoleft": {
                "label": f'''←  {MessageCatalog.translate("Move to left")}''',
                "command": self.move_column_left,
            },
            "movetofirst": {
                "label": f'''⇤  {MessageCatalog.translate("Move to first")}''',
                "command": self.move_column_to_first,
            },
            "movetolast": {
                "label": f'''⇥  {MessageCatalog.translate("Move to last")}''',
                "command": self.move_column_to_last,
            },
            "alignleft": {
                "label": f'''◧  {MessageCatalog.translate("Align left")}''',
                "command": self.align_heading_left,
            },
            "alignright": {
                "label": f'''◨  {MessageCatalog.translate("Align right")}''',
                "command": self.align_heading_right,
            },
            "aligncenter": {
                "label": f'''◫  {MessageCatalog.translate("Align center")}''',
                "command": self.align_heading_center,
            },
            "resettable": {
                "label": f'''{MessageCatalog.translate("⎌")}  {MessageCatalog.translate("Reset table")}''',
                "command": self.master.reset_table,
            },
            "hidecolumn": {
                "label": f'''◑  {MessageCatalog.translate("Hide column")}''',
                "command": self.hide_column,
            }
        }

        self.add_command(cnf=config["resettable"])

        # HIDE & SHOW
        self._build_show_menu()
        self.add_cascade(menu=self._show_menu, label=f'''±  {MessageCatalog.translate("Columns")}''')
        self.add_separator()

        # MOVE MENU
        move_menu = TkMenu(self, tearoff=False)
        move_menu.add_command(cnf=config["movetoleft"])
        move_menu.add_command(cnf=config["movetoright"])
        move_menu.add_command(cnf=config["movetofirst"])
        move_menu.add_command(cnf=config["movetolast"])
        self.add_cascade(menu=move_menu, label=f'''⇄  {MessageCatalog.translate("Move")}''')

        align_menu = TkMenu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label=f'''↦  {MessageCatalog.translate("Align")}''')
        self.add_command(cnf=config["hidecolumn"])


    def tk_popup(self, event):
        # capture the column and item that invoked the menu
        self.event = event
        self._build_show_menu()

        # show the menu below the invoking cell
        rootx = self.view.winfo_rootx()
        rooty = self.view.winfo_rooty()
        super().tk_popup(rootx + event.x, rooty + event.y + 10)

    
    def _build_show_menu(self):
        """Build the show menu based on currently available columns"""
        if self._show_menu is not None:
            self._show_menu.delete(0, END)
        else:
            self._show_menu = TkMenu(self, tearoff=False)

        self._show_menu.add_command(
            label=MessageCatalog.translate("Show All"), command=self.show_all_columns
        )
        self._show_menu.add_separator()

        displaycolumns = [x.cid for x in self.master.tablecolumns_visible]
        for column in self.master.tablecolumns:
            varname = f"column_{column.cid}"
            # self.columnvars.append(tk.Variable(name=varname, value=True))
            self._show_menu.add_checkbutton(
                label=column._headertext,
                command=lambda w=column: self.toggle_columns(w.cid),
                variable=varname,
                onvalue=True,
                offvalue=False,
            )
            if column.cid in displaycolumns:
                self.setvar(varname, True)
            else:
                self.setvar(varname, False)

    
    def toggle_columns(self, cid):
        """Toggles the visibility of the selected column"""
        variable = f"column_{cid}"
        toggled = self.getvar(variable)
        if toggled:
            self.master.unhide_selected_column(cid=int(cid))
        else:
            self.master.hide_selected_column(cid=int(cid))

    
    def show_all_columns(self):
        """Show all columns"""
        for var in self.columnvars:
            var.set(value=True)
        self.master.reset_column_filters()

    
    def move_column_left(self):
        """Move column one position to the left"""
        self.master.move_column_left(self.event)

    
    def move_column_right(self):
        """Move column on position to the right"""
        self.master.move_column_right(self.event)

    
    def move_column_to_first(self):
        """Move column to leftmost position"""
        self.master.move_column_to_first(self.event)

    
    def move_column_to_last(self):
        """Move column to rightmost position"""
        self.master.move_column_to_last(self.event)

    
    def align_heading_left(self):
        """Left align the column header"""
        self.master.align_heading_left(self.event)

    
    def align_heading_right(self):
        """Right align the column header"""
        self.master.align_heading_right(self.event)

    
    def align_heading_center(self):
        """Center align the column header"""
        self.master.align_heading_center(self.event)

    
    def hide_column(self):
        """Hide the selected column"""
        eo = self.master._get_event_objects(self.event)
        eo.column.hide()
