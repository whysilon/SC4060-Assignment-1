import numpy as np

class Agent:
    def __init__(self, map, startX=0, startY=0 ):
        #Initialize agent at starting position
        self.positionX = startX
        self.positionY = startY
        self.map = map
