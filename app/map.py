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
from app.drawStates import drawStates

class Tile:
    def __init__(self, i, j, x, y, w, l):
        self.coord = (i,j)
        self.pos = (x, y)
        self.dim = (w, l)
        self.downWallColor = None
        self.rightWallColor = None
        self.downWallState = None
        self.rightWallState = None
        self.setFromDrawStates(drawStates[0])

    def setFromDrawStates(self, drawState):        
        self.downWallColor = None
        self.rightWallColor = None
        self.downWallState = None
        self.rightWallState = None
        
        self.setState(drawState.state)
        self.setEndState(drawState.state)

        if(self.stateColor == None):
            self.stateColor = [0,0,0,1]

        if(drawState.rightWall):
            self.setRightWall(drawState.wallState)
        else:
            self.setDownWall(drawState.wallState)

    def setFromLevelTile(self, levelTile):
        self.setState(levelTile.state)
        self.setEndState(levelTile.endState)                
        self.setRightWall(levelTile.rightWall)        
        self.setDownWall(levelTile.downWall)

    def setDownWall(self, wallState):
        self.downWallState = wallState
        self.downWallColor = self.getWallColor(wallState)        

    def setRightWall(self, wallState):        
        self.rightWallState = wallState
        self.rightWallColor = self.getWallColor(wallState)

    def toggleWallState(self, otherTile):
        if(otherTile.downWallState != None):
            self.downWallState = otherTile.downWallState if self.downWallState == None else None
            self.downWallColor = otherTile.downWallColor

        if(otherTile.rightWallState != None):
            self.rightWallState = otherTile.rightWallState if self.rightWallState == None else None
            self.rightWallColor = otherTile.rightWallColor

    def setState(self, state):
        self.state = state
        self.stateColor = self.getColor(state)

    def setEndState(self, endState):
        self.endState = endState
        self.endStateColor = self.getColor(endState)

    def getColor(self, state):
        for drawState in drawStates:
            if(state == drawState.state):
                return drawState.color

    def getWallColor(self, wallState):
        for drawState in drawStates:
            if(wallState == drawState.wallState):
                return drawState.wallColor

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
        self.paintTile.setFromDrawStates(drawStates[1])

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
                  'State': 0,
                  'EndState': 0
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
                tile.setFromLevelTile(levelTile)

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

    def setPaintTileState(self, drawState):
        self.paintTile.setFromDrawStates(drawState)
        self.draw()

    def draw(self, *largs):
        with self.canvas:
            self.canvas.clear()
            
            pos = tuple(map(operator.add, self.paintTile.pos, (self.width/2 , self.height - self.height/8)))

            Color(self.paintTile.stateColor[0], self.paintTile.stateColor[1], self.paintTile.stateColor[2], mode='rgb')            
            dim = self.paintTile.dim
            Rectangle(pos=pos, size=dim)

            if(self.paintTile.rightWallState != None):
                Color(self.paintTile.rightWallColor[0], self.paintTile.rightWallColor[1], self.paintTile.rightWallColor[2], mode='rgb')
                rightWallPos = (pos[0]+dim[0], pos[1])
                rightWallDim = (5, dim[1])
                Rectangle(pos=rightWallPos, size=rightWallDim)

            if(self.paintTile.downWallState != None):
                Color(self.paintTile.downWallColor[0], self.paintTile.downWallColor[1], self.paintTile.downWallColor[2], mode='rgb')
                downWallPos = (pos[0], pos[1]-5)
                downWallDim = (dim[0], 5)
                Rectangle(pos=downWallPos, size=downWallDim)

            ## State 
            for tile in self.tiles:
                Color(tile.stateColor[0], tile.stateColor[1], tile.stateColor[2], mode='rgb')
                pos = tuple(map(operator.add, tile.pos, ((self.width/2 + self.x)-self.width / 4, (self.height/2 + self.y))))
                dim = tile.dim
                Rectangle(pos=pos, size=dim)
                
                if(tile.rightWallState != None):
                    Color(tile.rightWallColor[0], tile.rightWallColor[1], tile.rightWallColor[2], mode='rgb')
                    rightWallPos = (pos[0]+dim[0], pos[1])
                    rightWallDim = (5, dim[1])
                    Rectangle(pos=rightWallPos, size=rightWallDim)
                
                if(tile.downWallState != None):
                    Color(tile.downWallColor[0], tile.downWallColor[1], tile.downWallColor[2], mode='rgb')
                    downWallPos = (pos[0], pos[1]-5)
                    downWallDim = (dim[0], 5)
                    Rectangle(pos=downWallPos, size=downWallDim)

            ## End state
            for tile in self.tiles:
                Color(tile.endStateColor[0], tile.endStateColor[1], tile.endStateColor[2], mode='rgb')
                pos = tuple(map(operator.add, tile.pos, ((self.width/2 + self.x)+self.width / 4, (self.height/2 + self.y))))
                dim = tile.dim
                Rectangle(pos=pos, size=dim)
                
                if(tile.rightWallState != None):
                    Color(tile.rightWallColor[0], tile.rightWallColor[1], tile.rightWallColor[2], mode='rgb')
                    rightWallPos = (pos[0]+dim[0], pos[1])
                    rightWallDim = (5, dim[1])
                    Rectangle(pos=rightWallPos, size=rightWallDim)
                
                if(tile.downWallState != None):
                    Color(tile.downWallColor[0], tile.downWallColor[1], tile.downWallColor[2], mode='rgb')
                    downWallPos = (pos[0], pos[1]-5)
                    downWallDim = (dim[0], 5)
                    Rectangle(pos=downWallPos, size=downWallDim)
            
    def on_touch_down(self, touch):
        self.checkTouchAndDraw(touch, True)

    def on_touch_move(self, touch):
        self.checkTouchAndDraw(touch, False)

    def checkTouchAndDraw(self, touch, clickEvent):
        if(self.level.readOnly):            
            return

        newDraw = False
        relativeToCenter = tuple(map(operator.sub, (touch.x, touch.y), ((self.width/2 + self.x), (self.height/2 + self.y))))
        for tile in self.tiles:
            if(tile.isClickOverState(self, relativeToCenter)):
                if(self.paintTile.state != None):
                    tile.setState(self.paintTile.state)
                
                if(clickEvent == True):
                    tile.toggleWallState(self.paintTile)
                
                self.level.tiles[tile.coord].updateFromMapTile(tile)
                newDraw = True

            if(tile.isClickOverEndState(self, relativeToCenter)):
                if(self.paintTile.endState != None):
                    tile.setEndState(self.paintTile.endState)

                if(clickEvent == True):
                    tile.toggleWallState(self.paintTile)
                
                self.level.tiles[tile.coord].updateFromMapTile(tile)
                newDraw = True
        
        if(newDraw):
            self.draw()