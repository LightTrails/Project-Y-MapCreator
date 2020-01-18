class DrawState():
    def __init__(self, state = None, color = None, wallState = None, rightWall = True, wallColor = None, text = ""):
        self.state = state
        self.color = color
        self.text = text
        self.wallColor = wallColor
        self.rightWall = rightWall
        self.wallState = wallState


drawStates = [
    DrawState(state=0, color = [0.15,0.15,0.15, 1]),
    DrawState(state=1, color = [1,0,0,1]),
    DrawState(state=2, color = [0,1,0,1]),
    DrawState(state=3, color = [0,0,1,1]),
    DrawState(wallState=0, rightWall=True, wallColor=[0.50,0.50,0.50,1], text="Right"),
    DrawState(wallState=0, rightWall=False, wallColor=[0.50,0.50,0.50,1], text="Down"),
    DrawState(wallState=1, rightWall=True, wallColor=[1.0,0.5,0.5,1], text="Right"),
    DrawState(wallState=1, rightWall=False, wallColor=[1,0.5,0.5,1], text="Down"),
    DrawState(wallState=2, rightWall=True, wallColor=[0.5,1,0.5,1], text="Right"),
    DrawState(wallState=2, rightWall=False, wallColor=[0.5,1,0.5,1], text="Down"),
    DrawState(wallState=3, rightWall=True, wallColor=[0.5,0.5,1,1], text="Right"),
    DrawState(wallState=3, rightWall=False, wallColor=[0.5,0.5,1,1], text="Down"),
]
