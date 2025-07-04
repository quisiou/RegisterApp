import ttkbootstrap as tkb
from ttkbootstrap.dialogs import Messagebox

from src.widgets.frame import Frame
from src.widgets.textEntry import TextEntry
from src.widgets.button import Button
from src.widgets.table import Table

from pathlib import Path, PosixPath

from typing import Any

from utils.parameters import *

from src.dataManager import Manager

class App(tkb.Window):
    '''
    Main application class

    Attributes:
        _children (dict, Default=None):     This widget's children widgets
        _cookies (dict, Default=None):      Information to be stored throughout the execution of the app
    '''
    
    _content: dict = None
    _cookies: dict = None

    def __init__(self, title: str = "ttkbootstrap", themename: str = "litera",
        iconphoto: str | Path | PosixPath=None, size: tuple[int, int] = None,
        position: tuple[int, int] = None, minsize: tuple[int, int] = None,
        maxsize: tuple[int, int] = None, resizable: tuple[bool, bool] = None,
        hdpi: bool = True, scaling: float = None, transient: Any = None,
        overrideredirect: bool = False, alpha: float = 1, **kwargs):
        '''
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            themename (str):
                The name of the ttkbootstrap theme to apply to the
                application.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method
                and the image will be the default icon for all windows.
                A ttkbootstrap image is used by default. To disable
                this default behavior, set the value to `None` and use
                the `Tk.iconphoto` or `Tk.iconbitmap` methods directly.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate. If `None`,
                the window will be placed on the center of the screen.
                Internally this is passed to the `Window.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (Tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Window.resizable` method.

            hdpi (bool):
                Enable high-dpi support for Windows OS. This option is
                enabled by default.

            scaling (float):
                Sets the current scaling factor used by Tk to convert
                between physical units (for example, points, inches, or
                millimeters) and pixels. The number argument is a
                floating point number that specifies the number of pixels
                per point on window's display.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Window.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is passed to the
                `Window.overrideredirect(1)` method.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs:
                Any other keyword arguments that are passed through to tkinter.Tk() constructor
                List of available keywords available at: https://docs.python.org/3/library/tkinter.html#tkinter.Tk
        '''
        
        super().__init__(title, themename, iconphoto, size, position, minsize,
            maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha, **kwargs)
        
        if position is None:
            self.place_window_center()
        
        self._content = {}

        # Create all the widgets for the application
        self.__initialize()


    def __getitem__(self, key):
        return self._content[key]


    def __setitem__(self, key, value):
        self._content[key] = value


    @property
    def content(self) -> dict:
        return self._content


    def __change_to_main(self, current_frame: Frame) -> None:
        '''
        Change to mainFrame

        :params Frame current_frame: The frame the user is in this moment
        '''

        current_frame.hide()
        self['mainFrame'].show()


    def __initialize_staff_table(self) -> None:
        '''
        Initializes the staff table frame
        '''
        
        staffTableFrame = Frame(
            parent=self,
            locator='pack',
            ID='staffTableFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'fill': tkb.BOTH,
                'expand': True,
                'anchor': tkb.CENTER
            }
        )

        colnames = Manager.get_columns('staff')
        rows = Manager.get_dataframe(filename=STAFF_FILE, as_list=True)

        staffTable = Table(
            parent=staffTableFrame,
            locator='pack',
            ID='staffTable',
            params={
                'coldata': colnames,
                'rowdata': rows,
                'searchable': True
            },
            position_params={
                'fill': tkb.BOTH,
                'expand': True,
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100
            }
        )

        buttonsFrame = Frame(
            parent=staffTableFrame,
            locator='pack',
            ID='buttonsFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'fill': tkb.BOTH
            }
        )

        Button(
            parent=buttonsFrame,
            locator='pack',
            ID='returnButton',
            params={
                'text': 'Volver',
                'command': lambda: self.__change_to_main(current_frame=staffTableFrame),
                'style': 'info.Outline.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.LEFT
            }
        )

        Button(
            parent=buttonsFrame,
            locator='pack',
            ID='addWorkerButton',
            params={
                'text': 'Añadir',
                'command': lambda: print('Añadido!'),
                'style': 'info.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.RIGHT
            }
        )


    def __initialize_main(self) -> None:
        '''
        Initializes the main screen's widgets (once logged in)
        '''

        def log_out() -> None:
            '''
            Closes the user's session
            '''

            self['mainFrame'].hide()
            self['logInFrame'].show()

            # Filters in tables do not save between frames, so no need to clear them
            self._cookies = None

        
        def add_log() -> None:
            '''
            Registers a new entry in the log history
            '''

            starts = Manager.begin_shift(self._cookies['user'])
            
            doLog = Messagebox.yesno(
                message=f'¿{"Comenzar" if starts else "Finalizar"} la jornada?',
                title='Fichar hora',
                alert=False,
                parent=self
            )

            if doLog != 'No':
                Manager.add_entry(self._cookies['user'])


        def check_staff() -> None:
            '''
            Change to staff table frame
            '''

            self['mainFrame'].hide()
            self['staffTableFrame'].show()


        mainFrame = Frame(
            parent=self,
            locator='pack',
            ID='mainFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'fill': tkb.BOTH,
                'expand': True,
                'anchor': tkb.CENTER
            }
        )

        containerFrame = Frame(
            parent=mainFrame,
            locator='pack',
            ID='containerFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'expand': True,
                'anchor': tkb.CENTER
            }
        )

        addLogButton = Button(
            parent=containerFrame,
            locator='pack',
            ID='addLogButton',
            params={
                'text': 'Fichar',
                'command': add_log,
                'style': 'info.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            }
        )

        checkLogButton = Button(
            parent=containerFrame,
            locator='pack',
            ID='checkLogButton',
            params={
                'text': 'Registros',
                'command': lambda: print('Mirar registros'),
                'style': 'info.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            }
        )

        checkStaffButton = Button(
            parent=containerFrame,
            locator='pack',
            ID='checkStaffButton',
            params={
                'text': 'Personal',
                'command': check_staff,
                'style': 'info.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            }
        )

        Button(
            parent=containerFrame,
            locator='pack',
            ID='logOutButton',
            params={
                'text': 'Cerrar sesión',
                'command': log_out,
                'style': 'info.Outline.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            }
        )

        # Add the admin and non-admin widgets
        if 'adminWidgets' not in self._content.keys():
            self['adminWidgets'] = []
        self['adminWidgets'].extend([checkLogButton, checkStaffButton])

        if 'nonAdminWidgets' not in self._content.keys():
            self['nonAdminWidgets'] = []
        self['nonAdminWidgets'].append(addLogButton)


    def __initialize_login(self) -> None:
        '''
        Initializes the login screen's widgets (initial frame)
        '''

        def log_in(*credential_entries):
            '''
            Tries to log in given some credentials

            Params:
                credentials: The credentials needed to try to log in
            '''

            self.focus()

            idNumber, password = [entry.get() for entry in credential_entries]

            try:
                isAdmin = Manager.log_in(num=idNumber, passwd=password)

                self._cookies = {
                    'user': idNumber,
                    'password': password,
                    'admin': isAdmin
                }

                if 'adminWidgets' in self._content.keys():
                    for w in self['adminWidgets']:
                        w.activate() if isAdmin else w.deactivate()

                if 'nonAdminWidgets' in self._content.keys():
                        for w in self['nonAdminWidgets']:
                            w.deactivate() if isAdmin else w.activate()

                self.__change_to_main(current_frame=self['logInFrame'])

                for entry in credential_entries:
                    entry.restore()

            except Manager.ManagerException as e:
                Messagebox.show_error(message=str(e), title='Error', parent=self)


        logInFrame = Frame(
            parent=self,
            locator='pack',
            ID='logInFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'fill': tkb.BOTH,
                'expand': True,
                'anchor': tkb.CENTER
            },
            show=True
        )
        
        containerFrame = Frame(
            parent=logInFrame,
            locator='pack',
            ID='containerFrame',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'expand': True,
                'anchor': tkb.CENTER
            },
            show=True
        )

        idEntry = TextEntry(
            parent=containerFrame,
            locator='pack',
            ID='idEntry',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            },
            show=True
        )
    
        passwordEntry = TextEntry(
            parent=containerFrame,
            locator='pack',
            ID='passwordEntry',
            params={
                
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            },
            show=True
        )

        Button(
            parent=containerFrame,
            locator='pack',
            ID='logInButton',
            params={
                'text': 'Iniciar sesión',
                'command': lambda: log_in(idEntry, passwordEntry),
                'style': 'info.TButton'
            },
            position_params={
                'padx': WINDOW_HEIGHT / 100,
                'pady': WINDOW_HEIGHT / 100,
                'side': tkb.TOP,
                'anchor': tkb.CENTER
            },
            show=True
        )
        idEntry.widget.bind(sequence='<Return>', func=lambda e: log_in(idEntry, passwordEntry))
        passwordEntry.widget.bind(sequence='<Return>', func=lambda e: log_in(idEntry, passwordEntry))


    def __initialize(self) -> None:
        '''
        Initializes all the required widgets and frames for the application
        '''

        ###############
        # Staff Table #
        ###############

        self.__initialize_staff_table()


        ##############################
        # The main frame (logged in) #
        ##############################

        self.__initialize_main()


        ################
        # Log-In Stuff #
        ################

        self.__initialize_login()
    