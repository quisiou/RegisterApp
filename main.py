from src.app import App
from src.dataManager import Manager

if __name__ == '__main__':
    Manager.setup()
    app = App(custom_theme='dark-blue')
    app.mainloop()