import kivy
from kivy.app import App
#from hoursDB import *


class MainWin():
    pass


class MainApp(App):
    def build(self):
        return MainWin()


if __name__ == "__main__":
    MainApp().run()