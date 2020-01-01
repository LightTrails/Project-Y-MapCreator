
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class SideMenu(BoxLayout):
    def __init__(self, map, **kwargs):
        super().__init__(**kwargs)
        self.width = 0
        self.scrollView = ScrollView(do_scroll_y=True)
        self.scrollView.clear_widgets()
        self.sideMenuItems = []

        self.boxView = BoxLayout(orientation="vertical", size_hint_y=None)
        self.boxView.bind(minimum_height=self.boxView.setter('height'))

        self.scrollView.add_widget(self.boxView)

        self.add_widget(self.scrollView)

    def close(self):
        self.width = 0

    def open(self):
        self.width = 200

    def resetColors(self):
        for sideMenuItem in self.sideMenuItems:
            sideMenuItem.resetColor()

    def clearItems(self):
        self.boxView.clear_widgets()
        self.sideMenuItems = []

    def addSideMenuItem(self, sideMenuItem):
        self.boxView.add_widget(sideMenuItem)
        self.sideMenuItems.append(sideMenuItem)
        sideMenuItem.setSideMenu(self)

    def clearAndAddSideMenuItems(self, sideMenuItems):
        self.clearItems()
        for sideMenu in sideMenuItems:
            self.addSideMenuItem(sideMenu)
