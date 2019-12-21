from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Drawer(BoxLayout):
    def __init__(self, map, sideMenu, **kwargs):
        super().__init__(**kwargs)

        xti = TextInput(text=str(map.xx),size_hint=(0.2, 1))
        yti = TextInput(text=str(map.yy),size_hint=(0.2, 1))

        xslider = Slider(min=3, max=13, value=map.xx)
        yslider = Slider(min=3, max=13, value=map.yy)

        def SetValues(instance, value):
            if(int(xslider.value) != instance.xx):
                xslider.value = instance.xx

            if(int(yslider.value) != instance.yy):
                yslider.value = instance.yy
            
        def OnSliderValueChange(instance, value):
            dw = int(xslider.value)
            dl = int(yslider.value)

            xti.text = str(dw)
            yti.text = str(dl)
            
            if( int(map.xx) != dw or int(map.yy) != dl ):
                map.level.resize((dw, dl))
                map.reloadLevel()

        map.bind(xx=SetValues)
        map.bind(yy=SetValues)

        xslider.bind(value=OnSliderValueChange)
        yslider.bind(value=OnSliderValueChange)

        x = BoxLayout()
        x.add_widget(xti)
        x.add_widget(xslider)

        y = BoxLayout()
        y.add_widget(yti)
        y.add_widget(yslider)


        sliders = BoxLayout(orientation="vertical") 
        sliders.add_widget(x)
        sliders.add_widget(y)
        self.add_widget(sliders)
        #self.add_widget(colorButton)