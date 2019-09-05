from PIL import Image
import numpy as np
from level import Level


colorSchema = { 0: [255, 255, 255], 1: [0,0,255], 2: [0,255,0], 3: [255,0,0] }

def showLevel(level):
    w, h = level.dimension[0] * 10, level.dimension[1] * 10
    data = np.zeros((h, w * 2 + 10, 3), dtype=np.uint8)

    for coord in level.tiles:
        for i in range(10):
            for j in range(10):
                data[j + coord[1]* 10, i + coord[0] * 10 ] = colorSchema[level.tiles[coord].state]
                data[j + coord[1]* 10, i + coord[0] * 10 + 10 + w ] = colorSchema[level.tiles[coord].endState]

    img = Image.fromarray(data, 'RGB')
    img.show()