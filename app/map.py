from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# jshint ignore:start
from kivy.properties import NumericProperty
# jshint ignore:end

from random import random as r
from functools import partial
from kivy.core.window import Window
import operator
import json
from level import Level

class Tile:
    def __init__(self, i, j, x, y, w, l):
        self.coord = (i,j)
        self.pos = (x, y)
        self.dim = (w, l)
        self.setStates(1, 1)                

    def setStates(self, state, endState):
        self.setState(state)
        self.setEndState(endState)

    def setState(self, state):
        self.state = state
        self.stateColor = self.getColor(state)

    def setEndState(self, endState):
        self.endState = endState
        self.endStateColor = self.getColor(endState)

    def getColor(self, state):
        if(state == 0):
            return [0.15,0.15,0.15]
        if(state == 1):
            return [0.5,0.5,0.5]
        if(state == 2):
            return [1,0,0]
        if(state == 3):
            return [0,1,0]
        if(state == 4):
            return [0,0,1]
        if(state == 5):
            return [1,1,1]

    def isClickOverState(self, parentWidget, pos):        
        newPos = tuple(map(operator.add, pos, (parentWidget.width / 4, 0)))
        return self.isClickOver(newPos)

    def isClickOverEndState(self, parentWidget ,pos):
        newPos = tuple(map(operator.add, pos, (-parentWidget.width / 4, 0)))
        return self.isClickOver(newPos)

    def isClickOver(self, pos):
        return pos[0] >= self.pos[0] and pos[0] <= self.pos[0]+self.dim[0] and pos[1] >= self.pos[1] and pos[1] <= self.pos[1]+self.dim[1]

class MapWidget(Widget):

    xx = NumericProperty(10.0)
    yy = NumericProperty(10.0)

    def __init__(self, **kwargs):
        self.drawEndState = True
        self.tiles = []
        
        self.paintTile = Tile(0,0,0,0, 20, 20)
        self.paintTile.setStates(2,2)

        self.paintOptions = []

        for i in range(6):
           paintExample = Tile(i, 0, i*25, 0, 20, 20)
           paintExample.setStates(i, i)
           self.paintOptions.append(paintExample)

        self.dimensions = (10, 10)

        super(MapWidget, self).__init__(**kwargs)
        
        emptyLevel = self.createEmptyLevel(self.dimensions)
        self.loadLevel(emptyLevel)


    def createEmptyLevel(self, dimension):
        sLevel = { 
            'Dimensions': {'x': dimension[0], 'y': dimension[1]},
            'Tiles': [],
            'Constraints': { 'MaxMoves': 0 }
        }

        for i in range(dimension[0]):
            for j in range(dimension[1]):
              sLevel['Tiles'].append({
                  'Coordinate': { 'x': i, 'y': j },
                  'State': 1,
                  'EndState': 1
              })
        
        return Level(sLevel)

    def reloadLevel(self):
        self.loadLevel(self.level)

    def loadLevel(self, level):
        self.level = level
        self.createMap(level.dimension[0], level.dimension[1])

        for tile in self.tiles:
            if( tile.coord in level.tiles ):
                levelTile = level.tiles[tile.coord]
                tile.setStates(levelTile.state, levelTile.endState)

        self.draw()

    def createMap(self, dw, dl):
        self.dimensions = (dw, dl)
        self.tiles = []

        self.xx = dw
        self.yy = dl

        w = 30
        l = 30    
        ds = 5

        for i in range(dw):
            for j in range(dl):
                wd = -(dw * (w+ds))/2 + (w+ds) * i
                wl = -(dl * (l+ds))/2 + (l+ds) * j
                tile = Tile(i, dl-j-1, wd, wl, w, l)
                self.tiles.append(tile)
        
        self.draw()

    def setPaintTileState(self, state):
        self.paintTile.setStates(state, state)
        self.draw()

    def draw(self, *largs):    
        with self.canvas:
            self.canvas.clear()
            
            pos = tuple(map(operator.add, self.paintTile.pos, (self.width/2 , self.height - self.height/8)))

            Color(self.paintTile.stateColor[0], self.paintTile.stateColor[1], self.paintTile.stateColor[2], mode='rgb')            
            Rectangle(pos=pos, size=self.paintTile.dim)

            ## Draw paint options
            for tile in self.paintOptions:
                Color(tile.stateColor[0], tile.stateColor[1], tile.stateColor[2], mode='rgb')
                pos = tuple(map(operator.add, tile.pos, (10, 90)))
                dim = tile.dim
                Rectangle(pos=pos, size=dim)

            ## State 
            for tile in self.tiles:
                Color(tile.stateColor[0], tile.stateColor[1], tile.stateColor[2], mode='rgb')
                pos = tuple(map(operator.add, tile.pos, ((self.width/2 + self.x)-self.width / 4, (self.height/2 + self.y))))
                dim = tile.dim
                Rectangle(pos=pos, size=dim)

            ## End state
            for tile in self.tiles:
                Color(tile.endStateColor[0], tile.endStateColor[1], tile.endStateColor[2], mode='rgb')
                pos = tuple(map(operator.add, tile.pos, ((self.width/2 + self.x)+self.width / 4, (self.height/2 + self.y))))
                dim = tile.dim
                Rectangle(pos=pos, size=dim)
            
    def on_touch_down(self, touch):
        self.checkTouchAndDraw(touch)

    def on_touch_move(self, touch):
        self.checkTouchAndDraw(touch)

    def checkTouchAndDraw(self, touch):
        newDraw = False
        relativeToCenter = tuple(map(operator.sub, (touch.x, touch.y), ((self.width/2 + self.x), (self.height/2 + self.y))))
        for tile in self.tiles:
            if(tile.isClickOverState(self, relativeToCenter)):
                tile.setState(self.paintTile.state)
                self.level.tiles[tile.coord].state = tile.state
                newDraw = True

            if(tile.isClickOverEndState(self, relativeToCenter)):
                tile.setEndState(self.paintTile.endState)
                self.level.tiles[tile.coord].endState = tile.endState
                newDraw = True
        
        if(newDraw):
            
            self.draw()