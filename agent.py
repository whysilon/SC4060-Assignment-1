import numpy as np
import map

class Agent:
    def __init__(self, maze: map.Maze, startX=0, startY=0 ):
        #Initialize agent at starting position
        self.positionX = startX
        self.positionY = startY
        self.maze = maze
        
        
    def move(self, action):
        # Remember current position
        curPosX, curPosY = self.positionX, self.positionY
        # Move agent based on action
        if action == "East":
            self.positionX += 1
        elif action == "West":
            self.positionX -= 1
        elif action == "North":
            self.positionY -= 1
        elif action == "South":
            self.positionY += 1
        else:
            raise ValueError("Invalid action")
        
        # Check if agent hit a wall
        if self.maze.layout[self.positionX][self.positionY] == 'W':
            self.positionX, self.positionY = curPosX, curPosY
            return False
        # Check if agent is out of bounds
        elif self.positionX < 0 or self.positionX >= self.maze.cols or self.positionY < 0 or self.positionY >= self.maze.rows:
            self.positionX, self.positionY = curPosX, curPosY
            return False

        return True
    
