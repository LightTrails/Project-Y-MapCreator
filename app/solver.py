from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label
from level import Level
from levelSolution import LevelSolution
from app.sideMenuItem import SideMenuItem
import threading
from kivy.clock import mainthread
from kivy.uix.progressbar import ProgressBar

class Solver(BoxLayout):
    def __init__(self, map, fileSelector, sideMenu, **kwargs):
        super().__init__(**kwargs)

        self.map = map
        self.results = []

        self.numSolutionsLabel = Label()
        self.currentDepth = Label()
        self.visitedStates = Label()
        self.newSolutions = Label()

        stats = GridLayout(cols=2)
        stats.add_widget(self.numSolutionsLabel)
        stats.add_widget(self.currentDepth)
        stats.add_widget(self.visitedStates)
        stats.add_widget(self.newSolutions)

        createdMoviesSlider = self.createSlider(self.setCutOffPoint)
        self.movesSlider = createdMoviesSlider[1]        

        createdBestSolutionSlider = self.createSlider(self.showNewSolutions)
        self.bestSolutionSlider = createdBestSolutionSlider[1]
        
        self.starButtons = []
        starsBoxLayout = BoxLayout()
        for i in range(3):
            def OnButtonClick(instance):
                index = self.starButtons.index(instance)
                self.lvlSolution.stars[index] = int(self.bestSolutionSlider.value)
                instance.text = str(self.lvlSolution.stars[index])

            starButton = Button(text="None", on_press=OnButtonClick)            
            self.starButtons.append(starButton)
            starsBoxLayout.add_widget(starButton)

        stars = BoxLayout(orientation="vertical")
        stars.add_widget(starsBoxLayout)
        stars.add_widget(createdBestSolutionSlider[0])

        self.moves_button = Button(text="Next Wave")
        self.moves_button.bind(on_press=self.createNextWaveAsync)

        saveExportButton = Button(text="Export Solution")
        saveExportButton.bind(on_press=self.exportSolution)

        saveSolutionButton = Button(text="Save Solution")
        saveSolutionButton.bind(on_press=self.saveSolution)

        loadSolutionButton = Button(text="Load Solution")
        loadSolutionButton.bind(on_press=self.loadSolution)

        self.progressBar = ProgressBar()
        self.progressBar.max = 1000
        self.progressBar.value = 500

        self.moves_box = BoxLayout(orientation="vertical")    
        self.moves_box.add_widget(self.moves_button)        
        self.moves_box.add_widget(createdMoviesSlider[0])

        self.fileSelector = fileSelector;
        self.activated = False        
        
        self.add_widget(stats)
        self.add_widget(stars)
        
        #self.add_widget(loadSolutionButton)
        self.add_widget(saveExportButton)
        self.add_widget(saveSolutionButton)
        
        self.add_widget(self.moves_box)

        self.sideMenu = sideMenu                
        self.solutionChain = []        
        
    def createSlider(self, callBack = None):
        slider = Slider(min=1, max=10, value=1)        
        label = TextInput(text=str(slider.value),size_hint=(0.2, 1))

        def OnSliderValueChange(instance, value):
            index = int(value)
            label.text = str(index)
            if(callBack != None):
                callBack(index)

        slider.bind(value=OnSliderValueChange)

        box = BoxLayout()
        box.add_widget(label)
        box.add_widget(slider)

        return (box, slider)

    def setCutOffPoint(self, index):
        if(index == 0):
            self.moves_button.text = "Next Wave"
            return
        
        nextWaveSolution = self.lvlSolution.currentWave[index-1]   
        self.moves_button.text = "Next Wave (Best Solution "+str(nextWaveSolution[2])+")"
        self.lvlSolution.nextWaveElementsToVisit = index
        self.renderSolution(nextWaveSolution[1])

    def showNewSolutions(self, index):        
        self.newSolutions.text = "Solutions: "+str(self.lvlSolution.solutionsByWave[index])

    def saveSolution(self, instance):
        if(self.fileSelector.currentFilePath != None):
            self.lvlSolution.saveSolution(self.fileSelector.currentFilePath)

    def exportSolution(self, instance):
        if(self.fileSelector.currentFilePath != None):
            self.lvlSolution.saveExport(self.fileSelector.currentFilePath)

    def loadSolution(self):
        if(self.fileSelector.currentFilePath != None):
            self.lvlSolution.loadSolution(self.fileSelector.currentFilePath)
            self.updateLabels()
            self.renderBestSolutionChain()
    
    def createNextWaveAsync(self, instance):
        self.moves_box.remove_widget(self.moves_button)
        self.moves_box.add_widget(self.progressBar, index=1)
        self.progressBar.value = 0
        self.progressBar.max = self.lvlSolution.nextWaveElementsToVisit
        threading.Thread(target=self.createNextWave).start()

    def createNextWave(self):
        self.lvlSolution.createNextWave(self.updateCallback)

        self.updateLabels()
        self.renderBestSolutionChain()
        self.enableMovesButton()

    @mainthread
    def updateCallback(self, value):
        self.progressBar.value = value

    @mainthread
    def enableMovesButton(self):
        self.moves_box.remove_widget(self.progressBar)
        self.moves_box.add_widget(self.moves_button, index=1)

    @mainthread
    def updateLabels(self):
        self.currentDepth.text = "Depth: "+str(self.lvlSolution.currentDepth)
        self.numSolutionsLabel.text = "Solutions: "+str(self.lvlSolution.totalSolutions)
        self.visitedStates.text = "States: "+str(len(self.lvlSolution.solutionList))
        for i in range(3):
            self.starButtons[i].text = str(self.lvlSolution.stars[i])

        self.movesSlider.max = len(self.lvlSolution.currentWave) + 0.1
        self.movesSlider.value = self.movesSlider.max

        self.bestSolutionSlider.max = self.lvlSolution.currentDepth + 0.1
        self.bestSolutionSlider.value = self.lvlSolution.currentDepth

    @mainthread
    def renderBestSolutionChain(self):
        self.sideMenu.clearItems()
        
        bestSolution = self.lvlSolution.bestSolution
        currentSolutionIndex = bestSolution[1]

        bestPath = []
        while True:
            currentSolution = self.lvlSolution.solutionList[currentSolutionIndex]            
            bestPath.append((currentSolution[0], currentSolution[1]))
                
            # If solution is root of solution tree
            if(currentSolution[2][0][0] == -1):
                break
            else:
                currentSolutionIndex = currentSolution[2][0][0]

        for path in bestPath[::-1]:
            self.addSideMenuOption(path[0], path[1])

    def addSideMenuOption(self, solutionHash, score):
        sideMenuItem = SideMenuItem(solutionHash, lambda drawState: self.renderSolution(drawState))
        sideMenuItem.setText(str(score))
        self.sideMenu.addSideMenuItem(sideMenuItem)
        sideMenuItem.select()

    def renderSolution(self, solutionHash):        
        renderLevel = self.lvlSolution.lvl
        renderLevel.setStateBasedOnHash(solutionHash)
        self.map.loadLevel(renderLevel)

    def loadLevel(self, lvl):
        self.map.loadLevel(lvl)

    def activate(self):
        self.activated = True
        self.sideMenu.clearItems()
        self.sideMenu.open()

        self.initialLvl = self.map.level        
        
        slvl = self.map.level.toLevel()
        lvl = Level(slvl)
        lvl.setReadOnly()

        self.lvlSolution = LevelSolution(lvl)        
        self.lvlSolution.addSolution(lvl, -1, None)
        
        self.updateLabels()
        self.renderBestSolutionChain()

        self.movesSlider.max = 1
        self.movesSlider.value = 1

        self.loadSolution()

    def deactivate(self):
        if(self.activated):
            self.lvlSolution = None
            self.loadLevel(self.initialLvl)
            self.activated = False

