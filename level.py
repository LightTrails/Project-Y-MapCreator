import random

def is_candidate(value, items):
    return value != 0 and len(items) > 0 and all(x.state == value or x.state == 0 for x in items)

class Level():
    def __init__(self, sLevel):
        dimension = sLevel['Dimensions']
        self.dimension = (int(dimension['x']), int(dimension['y']))
        self.tiles = { }

        self.constraints = { 'MaxMoves': sLevel['Constraints']['MaxMoves'] }

        self.turns = []

        for tile in sLevel['Tiles']:
            t = Tile(tile)
            self.tiles[t.coordinate] = t
        
            
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                currentTile = self.tiles[(i, j)]
                currentTile.setupNeighbourLists( [ self.tiles[(i+1+k, j)] for k in range(self.dimension[0]-1-i) ], 
                                                 [ self.tiles[(i-1-k, j)] for k in range(i) ], 
                                                 [ self.tiles[(i, j+1+k)] for k in range(self.dimension[1]-1-j) ], 
                                                 [ self.tiles[(i, j-1-k)] for k in range(j) ] )

    def resize(self, newDimensions):
        oldDimension = self.dimension

        if( oldDimension[0] < newDimensions[0] ):
            for i in range(newDimensions[0] - oldDimension[0]):
                for j in range(newDimensions[1]):
                    newTile = Tile({'Coordinate': {'x': i + oldDimension[0], 'y': j}, 'State': 1})
                    self.tiles[newTile.coordinate] = newTile

        if( oldDimension[0] > newDimensions[0] ):
            for i in range(oldDimension[0] - newDimensions[0]):
                for j in range(oldDimension[1]):
                    del self.tiles[(oldDimension[0] - i - 1 ,j)]

        if( oldDimension[1] < newDimensions[1] ):
            for i in range(newDimensions[0]):
                for j in range(newDimensions[1] - oldDimension[1]):
                    newTile = Tile({'Coordinate': {'x': i, 'y': j+ oldDimension[1]}, 'State': 1})
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

    def pickAndReverseNumberOfActions(self, numberOfActions):   
        for _ in range(numberOfActions):
            action = self.pickAction()
            if(action != None):
                self.applyReverseAction(action)


    def pickAction(self):
        allCordinates = []

        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                allCordinates.append((i, j))

        actionCandidates = []

        for coordinate in allCordinates:
            currentTile = self.tiles[coordinate]            
            if(currentTile.state == 0):
                continue

            up = list(filter(lambda tile: tile.state != 0, currentTile.up))
            down = list(filter(lambda tile: tile.state != 0, currentTile.down))
            left = list(filter(lambda tile: tile.state != 0, currentTile.left))
            right = list(filter(lambda tile: tile.state != 0, currentTile.right))

            if(is_candidate(currentTile.state, up)):
                actionCandidates.append((coordinate, 'up', len(up)))

            if(is_candidate(currentTile.state, down)):
                actionCandidates.append((coordinate, 'down', len(down)))

            if(is_candidate(currentTile.state, right)):
                actionCandidates.append((coordinate, 'right', len(right)))

            if(is_candidate(currentTile.state, left)):
                actionCandidates.append((coordinate, 'left', len(left)))

        actionCandidates.sort(key= lambda e: e[2], reverse=True)
        bestActionCandidates = actionCandidates[:10]
        random.shuffle(bestActionCandidates)
        
        return bestActionCandidates[0] if len(bestActionCandidates) > 0 else None        

    def applyReverseAction(self, reverseAction):
        currentTile = self.tiles[reverseAction[0]]
        if(reverseAction[1] == 'up'):
            for tile in currentTile.up:
                tile.state = 0
                
        if(reverseAction[1] == 'down'):
            for tile in currentTile.down:
                tile.state = 0

        if(reverseAction[1] == 'right'):
            for tile in currentTile.right:
                tile.state = 0

        if(reverseAction[1] == 'left'):
            for tile in currentTile.left:
                tile.state = 0

    def __str__(self):
        return str(self.dimension)
        
    def countNonEmptyStates(self):
        return sum([ 1 if self.tiles[tileCoordinates].state != 0 else 0 for tileCoordinates in self.tiles ])


    def addTurn(self, coordinate, direction):
        self.turns.append({ 'coordinate': coordinate, 'direction': direction })

    def toLevel(self):    
        return {
                'Dimensions': { 'x': self.dimension[0], 'y': self.dimension[1] },
                'Tiles': [ self.tiles[tileCoordinates].saveState() for tileCoordinates in self.tiles ],
                'Constraints': { 'MaxMoves': self.constraints['MaxMoves'] }
               }



class Tile():
    def __init__(self, sTile):
        coordinates = sTile['Coordinate']
        self.coordinate = (int(coordinates['x']), int(coordinates['y']))
        self.state = sTile['State'] if 'State' in sTile else sTile['EndState']
        self.endState = sTile['EndState'] if 'EndState' in sTile else sTile['State']

    def setupNeighbourLists(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def saveState(self):
        #if(self.state == 0):
        #    self.state = random.randint(1,2)

        return { 'State': self.state, 'EndState': self.endState, 'Coordinate': {'x': self.coordinate[0], 'y': self.coordinate[1] } }
        