
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Rectangle

class SideMenuItem(Button):
    def __init__(self, state, callBack, **kwargs):
        self.selected = False

        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height=28
        self.contentState = state
                
        self.callBack = callBack
        self.bind(on_press = self.onClick)
        self.bind(on_size=self.on_size)
        

    def setText(self, text):
        self.text = text

    def setSideColor(self, sideColor):
        self.background_color = sideColor

    def on_size(self, *args):
        self.drawSelected()

    def drawSelected(self):
        self.canvas.after.clear()
        if(self.selected):
            with self.canvas.after:            
                Color(1, 1, 0, 1)
                Rectangle(pos=self.pos, size=(self.size[0]*0.03, self.size[1]))

    def onClick(self, instance):
        self.selectWithCallback()

    def selectWithCallback(self):
        self.callBack(self.contentState)
        self.select()

    def select(self):
        self.sideMenu.resetColors()
        self.selected = True
        self.drawSelected()
        # self.background_color = [1,0.5,0.5,1]

    def setSideMenu(self, sideMenu):
        self.sideMenu = sideMenu

    def resetColor(self):
        self.selected = False
        self.drawSelected()
        #self.background_color = [1,1,1,1]

