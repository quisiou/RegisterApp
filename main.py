from src.app import App
from src.dataManager import Manager

from utils.parameters import WINDOW_WIDTH, WINDOW_HEIGHT, DATA_DIR

if __name__ == '__main__':

    # print(DATA_DIR)

    Manager.setup()
    
    app = App(custom_theme='dark-blue')

    app.mainloop()
