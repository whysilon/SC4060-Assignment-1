import numpy as np
import map
# Reward Dictionary
REWARD = {
    'G' : 1,
    'B' : -1,
    'N' : -0.05,
    'S' : -0.05,
}
DISCOUNT_FACTOR = 0.99
class Agent:
    def __init__(self, maze: map.Maze, start_x=0, start_y=0 ):
        #Initialize agent at starting position
        self.position_x = start_x
        self.position_y = start_y
        self.maze = maze
        # Possible moveset per state
        moveset_utility = {
            "East" : 0,
            "West" : 0,
            "North" : 0,
            "South" : 0
        }
        # Utility Matrix
        self.utility = np.full((self.maze.cols, self.maze.rows), None)
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                self.utility[i][j] = moveset_utility.copy()
        
        
    def move(self, action):
        # Remember current position
        cur_position_X, cur_position_Y = self.position_X, self.position_Y
        # Move agent based on action
        if action == "East":
            self.position_X += 1
        elif action == "West":
            self.position_X -= 1
        elif action == "North":
            self.position_Y -= 1
        elif action == "South":
            self.position_Y += 1
        else:
            raise ValueError("Invalid action")
        
        # Check if agent hit a wall
        if self.maze.layout[self.position_X][self.position_Y] == 'W':
            self.position_X, self.position_Y = cur_position_X, cur_position_Y
            return False
        # Assumption that it is legal for agent to move out of bounds
        # However, it will act like a wall and put the player back in the same position
        elif self.position_X < 0 or self.position_X >= self.maze.cols or self.position_Y < 0 or self.position_Y >= self.maze.rows:
            self.position_X, self.position_Y = cur_position_X, cur_position_Y
            return False

        return True
    

    def calculate_utility(self, x, y):
        # Using Bellman equation to get utility of state
        utility = self.get_reward(self.maze.layout[x][y]) + DISCOUNT_FACTOR * 1
        return utility

    def get_reward(self, x, y):
        return REWARD[self.maze.layout[x][y]]
