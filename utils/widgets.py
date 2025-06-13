from customtkinter import CTkBaseClass
from typing import Any

def add_widget_to_container(widget: CTkBaseClass, container: dict, id: str) -> None:
    '''
    Includes a widget in the container's list of children

    Params:
        widget (CTkBaseClass): The widget to include
        container (dict): The container where the widget will be added
        id (str): The identifier of the widget in the container
    '''

    assert id not in container, 'ID already in use'
    container[id] = widget


def create_widget(Widget: Any, master: Any, container: dict, id: str, locator: callable,
    params: dict = {}, position_params: dict = {}, out: bool = False) -> None:
    '''
    Creates a new widget, includes it in the container and places it on the screen.

    Params:
        Widget (Any): The widget class (any of the possible widgets)
        master (Any): The master of the new widget
        container (dict): The container where the widget will be added
        id (str): The identifier of the widget in the container
        locator (callable): The method to locate the widget on the screen
        params (dict, Default={}): Parameters for the customisation of the widget
        position_params (dict, Default={}): Parameters for the placement of the widget
        out (bool, Default=False): Whether to return the widget or not

    :returns output (Any): The created widget
    '''

    assert id not in container, 'ID already in use'

    myWidget = Widget(master, **params)
    locator(myWidget, **position_params)

    add_widget_to_container(myWidget, container, id)

    if out: return myWidget