# import ttkbootstrap as tb
# from ttkbootstrap import ttk

# from pathlib import Path, PosixPath

# from typing import Any

# from utils.parameters import *

# class App(tb.Window):
#     '''
#     Main application class

#     Attributes:
#         _children (dict, Default=None):     This widget's children widgets
#         _cookies (dict, Default=None):      Information to be stored throughout the execution of the app
#     '''
    
#     _content: dict = None
#     _cookies: dict = None

#     def __init__(self, title: str = "ttkbootstrap", themename: str = "litera",
#         iconphoto: str | Path | PosixPath=None, size: tuple[int, int] = None,
#         position: tuple[int, int] = None, minsize: tuple[int, int] = None,
#         maxsize: tuple[int, int] = None, resizable: tuple[bool, bool] = None,
#         hdpi: bool = True, scaling: float = None, transient: Any = None,
#         overrideredirect: bool = False, alpha: float = 1, **kwargs):
#         '''
#         Parameters:

#             title (str):
#                 The title that appears on the application titlebar.

#             themename (str):
#                 The name of the ttkbootstrap theme to apply to the
#                 application.

#             iconphoto (str):
#                 A path to the image used for the titlebar icon.
#                 Internally this is passed to the `Tk.iconphoto` method
#                 and the image will be the default icon for all windows.
#                 A ttkbootstrap image is used by default. To disable
#                 this default behavior, set the value to `None` and use
#                 the `Tk.iconphoto` or `Tk.iconbitmap` methods directly.

#             size (Tuple[int, int]):
#                 The width and height of the application window.
#                 Internally, this argument is passed to the
#                 `Window.geometry` method.

#             position (Tuple[int, int]):
#                 The horizontal and vertical position of the window on
#                 the screen relative to the top-left coordinate. If `None`,
#                 the window will be placed on the center of the screen.
#                 Internally this is passed to the `Window.geometry`
#                 method.

#             minsize (Tuple[int, int]):
#                 Specifies the minimum permissible dimensions for the
#                 window. Internally, this argument is passed to the
#                 `Window.minsize` method.

#             maxsize (Tuple[int, int]):
#                 Specifies the maximum permissible dimensions for the
#                 window. Internally, this argument is passed to the
#                 `Window.maxsize` method.

#             resizable (Tuple[bool, bool]):
#                 Specifies whether the user may interactively resize the
#                 toplevel window. Must pass in two arguments that specify
#                 this flag for _horizontal_ and _vertical_ dimensions.
#                 This can be adjusted after the window is created by using
#                 the `Window.resizable` method.

#             hdpi (bool):
#                 Enable high-dpi support for Windows OS. This option is
#                 enabled by default.

#             scaling (float):
#                 Sets the current scaling factor used by Tk to convert
#                 between physical units (for example, points, inches, or
#                 millimeters) and pixels. The number argument is a
#                 floating point number that specifies the number of pixels
#                 per point on window's display.

#             transient (Union[Tk, Widget]):
#                 Instructs the window manager that this widget is
#                 transient with regard to the widget master. Internally
#                 this is passed to the `Window.transient` method.

#             overrideredirect (bool):
#                 Instructs the window manager to ignore this widget if
#                 True. Internally, this argument is passed to the
#                 `Window.overrideredirect(1)` method.

#             alpha (float):
#                 On Windows, specifies the alpha transparency level of the
#                 toplevel. Where not supported, alpha remains at 1.0. Internally,
#                 this is processed as `Toplevel.attributes('-alpha', alpha)`.

#             **kwargs:
#                 Any other keyword arguments that are passed through to tkinter.Tk() constructor
#                 List of available keywords available at: https://docs.python.org/3/library/tkinter.html#tkinter.Tk
#         '''
        
#         super().__init__(title, themename, iconphoto, size, position, minsize,
#             maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha, **kwargs)
        
#         if position is None:
#             self.place_window_center()
        
#         self._content = {}

#         self.bind(sequence="<Escape>", func=self.__unfocus)

#         # Create all the widgets for the application
#         self.__initialize()


#     def __unfocus(self, event=None) -> None:
#         '''
#         Unfocuses the actual focused widget (by focusing the main window)

#         :params (Any, Default=None) event: The event which triggered this method
#         '''

#         self.focus()


#     def __initialize_login(self) -> None:
#         logInFrame = tb.Frame(self)
#         logInFrame.pack(pady=40)

#         entry = tb.Entry(logInFrame)
#         entry.pack(pady=40)


#     def __initialize(self) -> None:
#         '''
#         Initializes all the required widgets and frames for the application
#         '''

#         ################
#         # Log-In Stuff #
#         ################

#         self.__initialize_login()