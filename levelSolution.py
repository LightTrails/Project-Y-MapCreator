import os
import json

path = 'C:\\git\\ProjectY-MapCreator\\solutions'
exportPath = 'C:\\git\\ProjectY-MapCreator\\solutionsexport'

class LevelSolution:
    def __init__(self, lvl):        
        self.solutionList = []
        self.solutionDict = dict()
        self.lvl = lvl
        self.currentWave = [(0, lvl.getHash2(), lvl.countScore())]
        self.currentDepth = 0
        self.numberOfSolutions = 0
        self.bestSolution = (None, None)
        self.optimalSolutionIndex = -1
        self.stars = [0,0,0]
        self.totalSolutions = 0
        self.solutionsByWave = [0]
        self.nextWaveElementsToVisit = 1
        
    def addSolution(self, lvl, cameFromIndex, action):
        hash = lvl.getHash2()
        score = lvl.countScore()
        
        solution = (hash, score, [(cameFromIndex, action)], self.currentDepth, None)
        
        newIndex = len(self.solutionList)

        self.solutionList.append(solution)
        self.solutionDict[hash] = newIndex

        if(self.bestSolution[0] == None or self.bestSolution[0] > score):
            
            if(score == 0):
                self.optimalSolutionIndex = newIndex
                self.markPathToNodeAsSolution(newIndex, 0)

            self.bestSolution = (score, newIndex)
        
        return newIndex

    def markPathToNodeAsSolution(self, solutionIndex, bestDepth):
        solutionsToVisit = [(solutionIndex, bestDepth)]
        newSolutions = 0

        while len(solutionsToVisit) > 0:
            nextNode = solutionsToVisit.pop()

            if(nextNode == -1):
                continue;
            
            nextSolution = self.solutionList[nextNode[0]]

            # Only visits none solution nodes and make them a solution node
            if(nextSolution[4] == None):
                currentSolution = self.solutionList[nextNode[0]]
                parents = currentSolution[2]
                newSolutions = newSolutions + 1

                for i in range(len(parents)):                    
                    solutionsToVisit.append((parents[i][0], nextNode[1]+1))

                self.solutionList[nextNode[0]] = (currentSolution[0], currentSolution[1], currentSolution[2], currentSolution[3], nextNode[1])

        self.totalSolutions = self.totalSolutions + newSolutions



    def createNextWave(self, callBack):
        nextWave = []
        
        if(len(self.currentWave) == 0):
            return

        percentage = int(self.nextWaveElementsToVisit / 20)

        for i in range(self.nextWaveElementsToVisit):
            if(percentage != 0 and i % percentage):
                callBack(i)
                
            wave = self.currentWave[i]
            currentWaveHash = wave[1]

            self.lvl.setStateBasedOnHash(currentWaveHash)
            actions = self.lvl.getAllActions()

            for action in actions:
                self.lvl.setStateBasedOnHash(currentWaveHash)
                self.lvl.applyAction(action)

                newPotentionalSolution = self.lvl.getHash2()

                

                if(newPotentionalSolution not in self.solutionDict):                    
                    solutionIndex = self.addSolution(self.lvl, wave[0], action)
                    solution = self.solutionList[solutionIndex]
                    if(solution[4] == None):
                        nextWave.append((solutionIndex, solution[0], solution[1]))
                else:
                    solutionIndex = self.solutionDict[newPotentionalSolution]
                    solution = self.solutionList[solutionIndex]
                    
                    # Is not as solution node
                    if(solution[4] == None):
                        solution[2].append((wave[0], action))
                    else:
                        solution[2].append((wave[0], action))
                        self.markPathToNodeAsSolution(wave[0], solution[4] + 1)

        self.solutionsByWave.append(self.totalSolutions)        
        nextWave.sort(key=lambda s: s[2])

        self.currentWave = nextWave
        self.nextWaveElementsToVisit = len(nextWave)
        self.currentDepth = self.currentDepth + 1


    def saveSolution(self, currentFileSolution):
        fileName = self.getCurrentLevelPath(currentFileSolution)
        
        solution = { 
            'solutionList': self.solutionList,
            'currentDepth': self.currentDepth,
            'bestSolution': self.bestSolution,
            'nextWave': self.currentWave,
            'stars': self.stars,
            'totalSolutions': self.totalSolutions,
            'solutionsByWave': self.solutionsByWave
        }

        json.dump(solution, open(fileName, "w"))
        

    def saveExport(self, currentFileSolution):
        fileName = self.getCurrentLevelExportPath(currentFileSolution)

        export = { }
        exportedSolutions = { }
        
        export['stars'] = self.stars
        export['solution'] = exportedSolutions

        maxDepthByStars = self.stars[2]

        filteredList = list(filter(lambda x: x[4] != None and x[4] <= maxDepthByStars, self.solutionList))
        sorted(filteredList, key=lambda x: x[4])
        
        for solution in filteredList[::-1]:
            for parentAndAction in solution[2]:                
                exportedSolutions[self.solutionList[parentAndAction[0]][0]] = parentAndAction[1]

        json.dump(export, open(fileName, "w"))
        

    def loadSolution(self, currentLevelSolution):
        fileName = self.getCurrentLevelPath(currentLevelSolution)

        if(not os.path.exists(fileName)):
            return

        file = open(fileName, "r")
        loadedSolution = json.load(file)
        self.solutionList = loadedSolution['solutionList']
        self.currentDepth = loadedSolution['currentDepth']
        self.bestSolution = loadedSolution['bestSolution']
        self.currentWave = loadedSolution['nextWave']
        self.stars = loadedSolution['stars']
        self.totalSolutions = loadedSolution['totalSolutions']
        self.solutionsByWave = loadedSolution['solutionsByWave']

        self.totalSolutionsLastWave = self.totalSolutions

        for i in range(len(self.solutionList)):
            self.solutionDict[self.solutionList[i][0]] = i

    def getCurrentLevelPath(self, currentLevelSolution):
        return path + '\\' + os.path.basename(currentLevelSolution).replace(".json", "") + "_solutions.json"

    def getCurrentLevelExportPath(self, currentLevelSolution):
        return exportPath + '\\' + os.path.basename(currentLevelSolution).replace(".json", "") + "_solutions.json"
    

    