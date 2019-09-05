import json
from level import Level
import displayImage

levelDictionary = json.load(open("c:\\Debug\\Level1.json", "r"))

results = []

numberOfMoves = 10

for i in range(100):
    lvl = Level(levelDictionary)
    lvl.pickAndReverseNumberOfActions(numberOfMoves)
    results.append((lvl.countNonEmptyStates(), lvl))

results.sort(key=lambda l: l[0])
best = results[0]
#displayImage.showLevel(best[1])

levelDirectory = best[1].toLevel( { 'MaxMoves': numberOfMoves } )

json.dump(levelDirectory, open("c:\\Debug\\Level1.json", "w"))