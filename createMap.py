from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
import operator
from kivy.core.window import Window
import json
from level import Level
from app.map import MapWidget

from app.fileselector import FileSelector
from app.solver import Solver
from app.drawer import Drawer

from app.panels import Panels
from app.sideMenu import SideMenu

path = 'C:\\git\\ProjectY\\Assets\\Resources\\Levels'

class CreateMap(App):
    def build(self):
        map = MapWidget()
        map.bind(pos=map.draw, size=map.draw)

        layout = BoxLayout(size_hint=(1, None), height=65)

        sideMenu = SideMenu(map, size_hint=(None, 1))

        panels = Panels(layout, map, sideMenu, size_hint=(1, None), height=25)

        root = BoxLayout(orientation='vertical')
        mainArea = BoxLayout(orientation='horizontal')

        mainArea.add_widget(map)
        mainArea.add_widget(sideMenu)

        root.add_widget(panels)
        root.add_widget(mainArea)
        root.add_widget(layout)

        self.map = map
        return root

if __name__ == '__main__':
    #initial_center = Window.center
    Window.size = (1600, 1000)

    Window.left = 100   
    Window.top = 100

    CreateMap().run()
