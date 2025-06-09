from customtkinter import CTkBaseClass
from typing import Any, Literal

def add_widget_to_container(widget: CTkBaseClass, container: dict, id: str):

    assert id not in container, 'ID already in use'
    container[id] = widget


def create_widget(Widget: Any, master: Any, container: dict, id: str, locator: callable,
    params: dict = {}, position_params: dict = {}, out: bool = False) -> None:

    assert id not in container, 'ID already in use'

    myWidget = Widget(master, **params)
    locator(myWidget, **position_params)

    add_widget_to_container(myWidget, container, id)

    if out: return myWidget