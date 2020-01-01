
from kivy.uix.button import Button
from kivy.graphics import Color

class SideMenuItem(Button):
    def __init__(self, text, callBack, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height=28
        self.text = text
        self.callBack = callBack
        self.bind(on_press = self.onClick)


    def onClick(self, instance):
        self.callBack(self)
        self.sideMenu.resetColors()
        self.background_color = [1,0.5,0.5,1]

    def setSideMenu(self, sideMenu):
        self.sideMenu = sideMenu

    def resetColor(self):
        self.background_color = [1,1,1,1]

