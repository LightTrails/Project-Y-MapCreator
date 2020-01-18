import random

def is_candidate(value, items):
    return value != 0 and len(items) > 0 and any(x.state != value for x in items) and not any(x.endState == 0 for x in items)

class Level():
    def __init__(self, sLevel):
        dimension = sLevel['Dimensions']
        self.dimension = (int(dimension['x']), int(dimension['y']))
        self.tiles = { }

        self.constraints = { 'MaxMoves': sLevel['Constraints']['MaxMoves'] }

        self.turns = []
        self.readOnly = False
        for tile in sLevel['Tiles']:
            t = Tile(tile)
            self.tiles[t.coordinate] = t
        
            
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                currentTile = self.tiles[(i, j)]
                currentTile.setupNeighbours( 
                    self.tiles[(i, j-1)] if (j-1) >= 0 else None,
                    self.tiles[(i, j+1)] if (j+1) < self.dimension[1] else None,
                    self.tiles[(i-1, j)] if (i-1) >= 0 else None,
                    self.tiles[(i+1, j)] if (i+1) < self.dimension[0] else None)

    def setReadOnly(self):
        self.readOnly = True

    def resize(self, newDimensions):
        oldDimension = self.dimension

        if( oldDimension[0] < newDimensions[0] ):
            for i in range(newDimensions[0] - oldDimension[0]):
                for j in range(newDimensions[1]):
                    newTile = Tile({'Coordinate': {'x': i + oldDimension[0], 'y': j}, 'State': 0})
                    self.tiles[newTile.coordinate] = newTile

        if( oldDimension[0] > newDimensions[0] ):
            for i in range(oldDimension[0] - newDimensions[0]):
                for j in range(oldDimension[1]):
                    del self.tiles[(oldDimension[0] - i - 1 ,j)]

        if( oldDimension[1] < newDimensions[1] ):
            for i in range(newDimensions[0]):
                for j in range(newDimensions[1] - oldDimension[1]):
                    newTile = Tile({'Coordinate': {'x': i, 'y': j+ oldDimension[1]}, 'State': 0})
                    self.tiles[newTile.coordinate] = newTile
 
        if( oldDimension[1] < newDimensions[1] ):
            for i in range(oldDimension[0]):
                for j in range(oldDimension[1] - newDimensions[1]):
                    del self.tiles[(i ,oldDimension[1]-j-1)]

        self.dimension = newDimensions


    def reset(self):
        for tile in self.tiles:
            ctile = self.tiles[tile]
            ctile.state = ctile.endState

    def getAllActions(self):
        allCordinates = []

        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                allCordinates.append((i, j))

        actionCandidates = []

        for coordinate in allCordinates:
            currentTile = self.tiles[coordinate]            
            if(currentTile.state == 0):
                continue

            if(is_candidate(currentTile.state, currentTile.createUpList())):
                actionCandidates.append((coordinate, 'up', currentTile.state))

            if(is_candidate(currentTile.state, currentTile.createDownList())):
                actionCandidates.append((coordinate, 'down', currentTile.state))

            if(is_candidate(currentTile.state, currentTile.createRightList())):
                actionCandidates.append((coordinate, 'right', currentTile.state))

            if(is_candidate(currentTile.state, currentTile.createLeftList())):
                actionCandidates.append((coordinate, 'left', currentTile.state))

        return actionCandidates

    def applyAction(self, action):
        currentTile = self.tiles[action[0]]
        if(action[1] == 'up'):
            for tile in currentTile.createUpList():
                tile.state = action[2]
                
        if(action[1] == 'down'):
            for tile in currentTile.createDownList():
                tile.state = action[2]

        if(action[1] == 'right'):
            for tile in currentTile.createRightList():
                tile.state = action[2]

        if(action[1] == 'left'):
            for tile in currentTile.createLeftList():
                tile.state = action[2]

    def __str__(self):
        return str(self.dimension)
        
    def countScore(self):
        return sum([ 1 if self.tiles[tileCoordinates].state != self.tiles[tileCoordinates].endState else 0 for tileCoordinates in self.tiles ])

    def getHash(self):
        listToHash = []
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                listToHash.append((i, j, self.tiles[(i,j)].state))

        return hash(frozenset(listToHash))

    def countNonEmptyStates(self):
        return sum([ 1 if self.tiles[tileCoordinates].state != 0 else 0 for tileCoordinates in self.tiles ])

    def addTurn(self, coordinate, direction):
        self.turns.append({ 'coordinate': coordinate, 'direction': direction })

    def toLevel(self):   
        tileList = [ self.tiles[tileCoordinates].saveState() for tileCoordinates in self.tiles ] 
        actualTiles = filter(lambda tile: tile['Coordinate']['x'] < self.dimension[0] and tile['Coordinate']['y'] < self.dimension[1], tileList)
        return {
                'Dimensions': { 'x': self.dimension[0], 'y': self.dimension[1] },
                'Tiles': list(actualTiles),
                'Constraints': { 'MaxMoves': self.constraints['MaxMoves'] }
               }

class Tile():
    def __init__(self, sTile):
        coordinates = sTile['Coordinate']
        self.coordinate = (int(coordinates['x']), int(coordinates['y']))

        self.state = sTile['State'] if 'State' in sTile else 0
        self.endState = sTile['EndState'] if 'EndState' in sTile else 0

        self.rightWall = sTile['RightWall'] if 'RightWall' in sTile else None
        self.downWall = sTile['DownWall'] if 'DownWall' in sTile else None

    def setupNeighbours(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right    

    def updateFromMapTile(self, mapTile):
        self.state = mapTile.state
        self.endState = mapTile.endState
        self.downWall = mapTile.downWallState
        self.rightWall = mapTile.rightWallState

    def createUpList(self):
        result = []
        nextTile = self.up if self.up != None and self.up.downWall != 0 else None
        while nextTile != None:
            result.append(nextTile)
            nextTile = nextTile.up if nextTile.up != None and nextTile.up.downWall != 0 else None

        return result

    def createDownList(self):
        result = []
        nextTile = self.down if self.downWall != 0 else None
        while nextTile != None:
            result.append(nextTile)
            nextTile = nextTile.down if nextTile.downWall != 0 else None
        
        return result

    def createLeftList(self):
        result = []
        nextTile = self.left if self.left != None and self.left.rightWall != 0 else None
        while nextTile != None:
            result.append(nextTile)
            nextTile = nextTile.left if nextTile.left != None and nextTile.left.rightWall != 0 else None

        return result

    def createRightList(self):
        result = []
        nextTile = self.right if self.rightWall != 0 else None
        while nextTile != None:
            result.append(nextTile)
            nextTile = nextTile.right if nextTile.rightWall != 0 else None

        return result

    def saveState(self):
        saveState = { 'Coordinate': {'x': self.coordinate[0], 'y': self.coordinate[1] } }

        if( self.state != 0):
            saveState['State'] = self.state

        if( self.endState != 0):
            saveState['EndState'] = self.endState

        if( self.rightWall != None):
            saveState['RightWall'] = self.rightWall

        if( self.downWall != None):
            saveState['DownWall'] = self.downWall

        return saveState
        