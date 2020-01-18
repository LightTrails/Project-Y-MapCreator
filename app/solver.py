from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from level import Level
from app.sideMenuItem import SideMenuItem

class Solver(BoxLayout):
    def __init__(self, map, sideMenu, **kwargs):
        super().__init__(**kwargs)

        self.map = map
        self.results = []
                
        reset_button = Button(text="Reset")
        reset_button.bind(on_press=self.reset)

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
        moves_button.bind(on_press=self.pickRandomAction)

        moves_box = BoxLayout(orientation="vertical")
        moves_box.add_widget(moves_button)
        moves_box.add_widget(moves_slider)
        self.activated = False
        self.add_widget(reset_button)
        self.add_widget(moves_box)        
        self.sideMenu = sideMenu
        self.nextWaveOfOptions = []
        self.visitedStates = set()
        self.solutionChain = []
        self.currentIndex = 0
        

        
    def pickRandomAction(self, instance):
        results = []
        # numberOfMoves = int(self.slider.value)

        sortedList = sorted(self.nextWaveOfOptions, key = lambda item: item[2])

        currentWaveOfOptions = list(sortedList)
        self.nextWaveOfOptions.clear()

        maxIndex = int(self.slider.value)
        for waveOfOption in currentWaveOfOptions[0:maxIndex]:
            slvl = waveOfOption[3].toLevel()
            lvl = Level(slvl)
            
            actions = lvl.getAllActions()
            for action in actions:
                newCandidate = Level(slvl)
                newCandidate.applyAction(action)
                hash = newCandidate.getHash()
                if(hash not in self.visitedStates):
                    self.visitedStates.add(hash)
                    self.addToSolutionChain(newCandidate, waveOfOption[0])
                    
                    # self.appendNewState(newCandidate)
        
        self.slider.max = len(self.nextWaveOfOptions)
        self.slider.value = self.slider.max
        self.createBestChain()

    def loadLevel(self, lvl):
        self.map.loadLevel(lvl)

    def activate(self):
        self.activated = True
        self.sideMenu.clearItems()
        self.sideMenu.open()
        self.bestSolution = None

        self.visitedStates.clear()

        self.initialLvl = self.map.level
        self.nextWaveOfOptions.clear()
        
        slvl = self.map.level.toLevel()
        lvl = Level(slvl)
        lvl.setReadOnly()

        self.slider.max = 1
        self.slider.value = 1

        self.addToSolutionChain(lvl, -1)
        self.createBestChain()



    def addToSolutionChain(self, lvl, cameFromIndex):
        item = (self.currentIndex, cameFromIndex, lvl.countScore(), lvl)
        
        if(self.bestSolution == None or self.bestSolution[2] > item[2]):
            self.bestSolution = item

        self.solutionChain.append(item)
        self.currentIndex+=1
        self.nextWaveOfOptions.append(item)

    def createBestChain(self):
        currentPart = self.bestSolution

        chain = []

        while currentPart != None:            
            chain.append(currentPart)
            if(currentPart[1] != -1):
                currentPart = self.solutionChain[currentPart[1]]
            else:
                currentPart = None
        
        self.sideMenu.clearItems()

        for part in chain[::-1]:
            self.appendNewState(part[3])


    def appendNewState(self, lvl):
        sideMenuItem = SideMenuItem(lvl, lambda drawState: self.loadLevel(lvl))
        sideMenuItem.setText(str(lvl.countScore()))
        self.sideMenu.addSideMenuItem(sideMenuItem)
        sideMenuItem.select()
        self.map.loadLevel(lvl)

    def deactivate(self):
        if(self.activated):
            self.loadLevel(self.initialLvl)
            self.activated = False

    def reset(self, instance):
        self.map.level.reset()
        self.map.reloadLevel()
