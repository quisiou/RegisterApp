from typing import Any, Literal

from ttkbootstrap import Menu, Menubutton

class Dropdown:

    _button: Menubutton = None
    _menu: Menu = None
    _params: dict = None
    _locator: Any = None
    _forget: Any = None
    _active: bool = None

    def __init__(self, master: Any, container: dict, ID: str, locator: Literal['pack', 'grid', 'place'],
                options: list = [], button_params: dict = {}, menu_params: dict = {},
                position_params: dict = {}, active: bool = True, show: bool = False):

        assert ID not in container, 'ID already in use'

        self._button = Menubutton(master, **button_params)
        self._menu = Menu(master, **menu_params)
        self._params = position_params
        self._active = active

        if locator == 'pack':
            self._locator = Menubutton.pack
            self._forget = Menubutton.pack_forget

        elif locator == 'grid':
            self._locator = Menubutton.grid
            self._forget = Menubutton.grid_forget

        elif locator == 'place':
            self._locator = Menubutton.place
            self._forget = Menubutton.place_forget

        # Add options to the dropdown
        for opt in options:
            self._menu.add_radiobutton(
                label=opt
            )

        # Link the menu with the button
        self._button['menu'] = self._menu

        # add to the container
        container[ID] = self

        # show directly if wanted
        if show: self.show()


    def show(self) -> None:

        if self._active:
            self._locator(self._button, **self._params)


    def hide(self) -> None:

        if self._active:
            self._forget(self._button)


    @property
    def loc_params(self) -> dict:
        return self._params
    

    def active(self) -> bool:
        return self._active
    
    
    def activate(self) -> None:
        self._active = True


    def deactivate(self) -> None:
        self._active = False