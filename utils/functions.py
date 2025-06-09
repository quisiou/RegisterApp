from customtkinter import CTkBaseClass

def add_widget_to_container(widget: CTkBaseClass, container: dict, id: str):

    assert id not in container, 'ID already in use'
    container[id] = widget


def set_window_frame_color(color: str):
    pass