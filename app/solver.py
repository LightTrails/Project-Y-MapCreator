from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from level import Level

class Solver(BoxLayout):
    def __init__(self, map, sideMenu, **kwargs):
        super().__init__(**kwargs)
        
        self.map = map

        def on_checkbox_active(checkbox, value):
            if value:
                self.map.drawEndState = False
                self.map.reloadLevel()
            else:
                self.map.drawEndState = True
                self.map.reloadLevel()

        def createLevel(instance):
            results = []
            numberOfMoves = int(self.slider.value)

            slvl = self.map.level.toLevel()

            for _ in range(10):
                lvl = Level(slvl)
                lvl.pickAndReverseNumberOfActions(numberOfMoves)
                results.append((lvl.countNonEmptyStates(), lvl))

            results.sort(key=lambda l: l[0])
            best = results[0][1]

            self.map.level = best
            self.map.reloadLevel()

        def reset(instance):
            self.map.level.reset()
            self.map.reloadLevel()

        checkbox = CheckBox()
        checkbox.bind(active=on_checkbox_active)

        reset_button = Button(text="Reset")
        reset_button.bind(on_press=reset)
        
        slider = Slider(min=1, max=10, value=1)
        self.slider = slider

        label = TextInput(text=str(slider.value),size_hint=(0.2, 1))

        def OnSliderValueChange(instance, value):
            label.text = str(int(value))

        self.slider.bind(value=OnSliderValueChange)

        moves_slider = BoxLayout()
        moves_slider.add_widget(label)
        moves_slider.add_widget(slider)

        moves_button = Button(text="Moves")
        moves_button.bind(on_press=createLevel)

        moves_box = BoxLayout(orientation="vertical")
        moves_box.add_widget(moves_button)
        moves_box.add_widget(moves_slider)
        
        self.add_widget(reset_button)
        self.add_widget(moves_box)
        self.add_widget(checkbox)


        
        

        