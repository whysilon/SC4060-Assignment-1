import numpy as np
import map
# Reward Dictionary
REWARD = {
    'G' : 1,
    'B' : -1,
    'N' : -0.05,
    'S' : -0.05,
}

# Cardinal Directions (Useful to compare with the action)
CARDINAL_DIRECTIONS = ('North', 'East', 'South', 'West')

PROBABILITY_OF_SUCCESS = 0.8
PROBABILITY_OF_FAILURE = 0.1

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
        self.utility_matrix = np.full((self.maze.cols, self.maze.rows), None)
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                self.utility[i][j] = moveset_utility.copy()
        
        
    def check_move(self, action):
        # Remember current position
        next_position_X, next_position_Y = self.position_X, self.position_Y
        # Move agent based on action
        if action == "East":
            next_position_X += 1
        elif action == "West":
            next_position_X -= 1
        elif action == "North":
            next_position_Y -= 1
        elif action == "South":
            next_position_Y += 1
        else:
            raise ValueError("Invalid action")
        
        # Check if agent hit a wall
        if self.maze.layout[next_position_X][next_position_Y] == 'W':
            return False
        # Assumption that it is legal for agent to move out of bounds
        # However, it will act like a wall and put the player back in the same position
        elif next_position_X < 0 or next_position_X >= self.maze.cols or next_position_Y < 0 or next_position_Y >= self.maze.rows:
            return False
        return True
    
    def move(self, action):
        if action == 'East':
            return self.position_x + 1, self.position_y
        elif action == 'West':
            return self.position_x - 1, self.position_y
        elif action == 'North':
            return self.position_x, self.position_y - 1
        elif action == 'South':
            return self.position_x, self.position_y + 1
        else:
            raise ValueError("Invalid action")

    def calculate_utility(self, x, y):
        # Using Bellman equation to get utility of state
        state_utility = self.get_reward(self.maze.layout[x][y]) + DISCOUNT_FACTOR * 
        return state_utility

    
    def get_reward(self, x, y):
        return REWARD[self.maze.layout[x][y]]
    
    def get_utility(self, x, y, action):
        # Initialise utility
        utility = 0
        action_pos = CARDINAL_DIRECTIONS.index(action)
        # Get the utility of the next state
        if self.check_move(CARDINAL_DIRECTIONS[action_pos]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[action_pos])
            utility += PROBABILITY_OF_SUCCESS * self.utility_matrix[new_x][new_y]
        else:
            # Fail to move means stay in the same position
            utility += PROBABILITY_OF_SUCCESS * self.utility_matrix[x][y]
        # Check the utility of the next state if agent moves to the right of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4])
            utility += PROBABILITY_OF_FAILURE * self.utility_matrix[new_x][new_y]
        else:
            utility += PROBABILITY_OF_FAILURE * self.utility_matrix[x][y]
        # Check the utility of the next state if agent moves to the left of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4])
            utility += PROBABILITY_OF_FAILURE * self.utility_matrix[new_x][new_y]
        else:
            utility += PROBABILITY_OF_FAILURE * self.utility_matrix[x][y]

        return utility
