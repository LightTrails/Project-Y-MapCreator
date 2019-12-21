from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from app.fileselector import FileSelector
from app.solver import Solver
from app.drawer import Drawer

class Panels(BoxLayout):
    
    def __init__(self, layout, map, sideMenu, **kwargs):
        super().__init__(**kwargs)

        self.sideMenu = sideMenu
        self.fileSelector = FileSelector(map, sideMenu)
        self.drawer = Drawer(map, sideMenu)
        self.solver = Solver(map, sideMenu)

        self.map = map
        
        self.btn1 = ToggleButton(text='Levels', group='panels', state='down')
        self.btn2 = ToggleButton(text='Draw Map', group='panels')
        self.btn3 = ToggleButton(text='Solver', group='panels')

        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)

        layout.add_widget(self.fileSelector)

        def OnStateChange(instance, value):
            if(value == 'down'):
                layout.clear_widgets()
                self.sideMenu.close();
                if(instance == self.btn1):
                    layout.add_widget(self.fileSelector)
                    self.fileSelector.openSideMenu()

                if(instance == self.btn2):
                    layout.add_widget(self.drawer)
                    

                if(instance == self.btn3):
                    layout.add_widget(self.solver)

        self.btn1.bind(state=OnStateChange)
        self.btn2.bind(state=OnStateChange)
        self.btn3.bind(state=OnStateChange)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if( keycode[1] == '1' and 'ctrl' in modifiers):
            self.fileSelector.load_level_by_number(1)
            return
        if( keycode[1] == 'numpadadd' and 'ctrl' in modifiers):
            self.fileSelector.loadNextLevel()
            return
        if( keycode[1] == 'numpadsubstract' and 'ctrl' in modifiers):
            self.fileSelector.loadPreviousLevel()
            return
        if( keycode[1] == '1' and 'shift' in modifiers):
            self.btn1._do_press()
            return
        if( keycode[1] == '2' and 'shift' in modifiers):
            self.btn2._do_press()
            return
        if( keycode[1] == '3' and 'shift' in modifiers):
            self.btn3._do_press()
            return
        if keycode[1] == '1':
            self.map.setPaintTileState(0)
            return
        if keycode[1] == '2':
            self.map.setPaintTileState(1)
            return
        if keycode[1] == '3':
            self.map.setPaintTileState(2)
            return            
        if keycode[1] == '4':
            self.map.setPaintTileState(3)
            return
        if keycode[1] == '5':
            self.map.setPaintTileState(4)
            return

        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
