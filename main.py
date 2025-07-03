# from src.app import App
from src.bootstrapApp import App as TkbApp
from src.dataManager import Manager

from utils.parameters import WINDOW_WIDTH, WINDOW_HEIGHT

if __name__ == '__main__':

    Manager.setup()
    
    # app = App(custom_theme='dark-blue')

    app = TkbApp(
        title='Clocker',
        size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        minsize=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
        themename='darkly'
    )

    app.mainloop()