import customtkinter
from pathlib import Path

class App(customtkinter.CTk):
    def __init__(self, width: int = 640, height: int = 480, custom_theme: str = None):

        # set custom theme
        theme_path = Path(Path.cwd(), 'themes', f'{custom_theme}.json')
        if not custom_theme or not theme_path.exists():
            customtkinter.set_default_color_theme('blue')
        else:
            customtkinter.set_default_color_theme(theme_path)

        super().__init__()

        # window-related
        self.geometry(f"{width}x{height}")
        self.resizable(width=False, height=False)
        self.title('Clocker')