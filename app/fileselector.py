from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import json
import glob, os
from app.sideMenuItem import SideMenuItem
from level import Level

path = 'C:\\git\\ProjectZ\\Assets\\Resources\\Levels'

class FileSelector(BoxLayout):
    def __init__(self, map, sideMenu,**kwargs):

        super().__init__(**kwargs)
        self.sideMenu = sideMenu
        self.orientation = "vertical"
        self.map = map        

        self.currentLevelNumber = -1

        self.optionView = BoxLayout(orientation="vertical", size_hint_y=None)
        self.optionView.bind(minimum_height=self.optionView.setter('height'))

        #main_button = Button(text='None Selected')
        #main_button.bind(on_release=self.setDropdownInSideMenu)
        #self.add_widget(main_button)

        new_button = Button(text='Save as New Level')    
        new_button.bind(on_press=self.save_new_level)

        save_button = Button(text='Save')     
        save_button.disabled = True   
        save_button.bind(on_press=self.save_current_level)

        self.save_button = save_button

        boxLayout = BoxLayout()
        boxLayout.add_widget(new_button)
        boxLayout.add_widget(save_button)

        self.add_widget(boxLayout)

        #self.mainbutton = main_button
        #self.dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        #self.dropdown.bind(on_select=self.load_level)
        self.set_based_on_levels()
        self.openSideMenu()

    def openSideMenu(self):
        self.sideMenu.open()

    def save_new_level(self, instance):        
        levelDirectory = self.map.level.toLevel()
        level = self.get_level_name_by_number(self.nextMaxLevel)
        json.dump(levelDirectory, open(path + '\\'+ level +".json", "w"))
        self.set_based_on_levels()        

    def save_current_level(self, instance):        
        if(self.currentFilePath):
            levelDirectory = self.map.level.toLevel()
            json.dump(levelDirectory, open(self.currentFilePath, "w"))

    def loadNextLevel(self):
        nextLevel = self.currentLevelNumber + 1

        if(nextLevel < self.nextMaxLevel and nextLevel > 0):
            self.load_level_by_number(nextLevel)

    def loadPreviousLevel(self):
        previous = self.currentLevelNumber - 1

        if(previous > 0 and previous < self.nextMaxLevel):
            self.load_level_by_number(previous)

    def load_level(self, instance, option):
        self.load_level_by_name(option)

    def load_level_by_name(self, name):
        self.currentFilePath = path + "\\"+name+".json"
        self.currentLevelNumber = int(name.replace('Level', ''))
        self.save_button.disabled = False

        file = open(self.currentFilePath, "r")
        levelDirectory = json.load(file)
        level = Level(levelDirectory)
        self.map.loadLevel(level)

    def load_level_by_number(self, number):
        levelName = self.get_level_name_by_number(number)

    def get_level_name_by_number(self, number):
        return 'Level{:03d}'.format(number)

    def set_based_on_levels(self):
        self.sideMenu.clearItems()
        self.nextMaxLevel = 1
        last = ''
        
        for file in os.listdir(path):
            if file.endswith(".json"):
                name = file.replace('.json', '')
                last = name
                sideMenuItem = SideMenuItem(name, lambda sideMenuItem: self.load_level_by_name(sideMenuItem.text))
                self.sideMenu.addSideMenuItem(sideMenuItem)                

        self.nextMaxLevel = int(last.replace('Level', '')) + 1