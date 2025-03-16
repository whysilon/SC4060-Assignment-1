import numpy as np
import map
# Reward Dictionary
REWARD = {
    'G' : 1,
    'B' : -1,
    'N' : -0.05,
    'S' : -0.05,
    'W' : -0.05
}

# Cardinal Directions (Useful to compare with the action)
CARDINAL_DIRECTIONS = ('North', 'East', 'South', 'West')

# Probability of agent movements
#      0.8
#       ^
# 0.1 <   > 0.1

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
        # In accordance to CARDINAL_DIRECTIONS
        moveset_utility = [0,0,0,0]
        # Utility Matrix
        self.utility_matrix = np.full((self.maze.cols, self.maze.rows), None)
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                self.utility_matrix[i][j] = moveset_utility.copy()
        
        
    def check_move(self, action):
        # Remember current position
        next_position_x, next_position_y = self.position_x, self.position_y
        # Move agent based on action
        if action == "East":
            next_position_y += 1
        elif action == "West":
            next_position_y -= 1
        elif action == "North":
            next_position_x -= 1
        elif action == "South":
            next_position_x += 1
        else:
            raise ValueError("Invalid action")
        
        # Assumption that it is legal for agent to move out of bounds
        # However, it will act like a wall and put the player back in the same position
        if next_position_y < 0 or next_position_y >= self.maze.cols:
            return False
        if next_position_x < 0 or next_position_x >= self.maze.rows:
            return False
        # Check if agent hit a wall
        elif self.maze.layout[next_position_x][next_position_y] == 'W':
            return False
        return True
    
    def move(self, action):
        if action == 'East':
            return self.position_x, self.position_y + 1
        elif action == 'West':
            return self.position_x, self.position_y -1
        elif action == 'North':
            return self.position_x - 1, self.position_y
        elif action == 'South':
            return self.position_x + 1, self.position_y
        else:
            raise ValueError("Invalid action")

    def calculate_utility(self, utility_matrix):
        # Calculate each utility of next possible state and
        # Using Bellman equation to get actual utility of state
        state_utility = []
        print(self.position_x, self.position_y)
        for action in CARDINAL_DIRECTIONS:
            reward = self.get_reward(self.position_x, self.position_y, action)
            utility = self.get_utility(utility_matrix,self.position_x, self.position_y, action)
            total = reward + (DISCOUNT_FACTOR * utility)
            state_utility.append(total)
        return state_utility

    
    def get_reward(self, x, y, action):
        if self.check_move(action):
            new_x, new_y = self.move(action)
            return REWARD[self.maze.layout[new_x][new_y]]
        else:
            return REWARD[self.maze.layout[x][y]]
    
    def get_utility(self, utility_matrix, x, y, action):
        # Initialise utility
        action_pos = CARDINAL_DIRECTIONS.index(action)
        utility = 0
        # Get the utility of the next state
        if self.check_move(CARDINAL_DIRECTIONS[action_pos]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[action_pos])
            utility += PROBABILITY_OF_SUCCESS * max(utility_matrix[new_x][new_y])
        else:
            # Fail to move means stay in the same position
            utility += PROBABILITY_OF_SUCCESS * max(utility_matrix[x][y])
        # Check the utility of the next state if agent moves to the right of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4])
            utility += PROBABILITY_OF_FAILURE * max(utility_matrix[new_x][new_y])
        else:
            utility += PROBABILITY_OF_FAILURE * max(utility_matrix[x][y])
        # Check the utility of the next state if agent moves to the left of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4])
            utility += PROBABILITY_OF_FAILURE * max(utility_matrix[new_x][new_y])
        else:
            utility += PROBABILITY_OF_FAILURE * max(utility_matrix[x][y])

        return utility
    
    def update_position(self, action):
        action_pos = CARDINAL_DIRECTIONS.index(action)
        # Check randomly if successful, rand() produces a float 0 to 1
        if(np.random.rand() < PROBABILITY_OF_SUCCESS):
            pass
        else:
            # Randomly choose a direction either left or right of the intended direction
            action_pos = action_pos + np.random.choice([-1, 1])
            action_pos = action_pos % 4
        # Move the agent based on action
        if self.check_move(CARDINAL_DIRECTIONS[action_pos]):
            self.position_x, self.position_y = self.move(CARDINAL_DIRECTIONS[action_pos])
        else:
            # If agent hits a wall, stay in the same position
            pass
    
    def value_iteration(self, iterations, epsilon):
        # epsilon is the maxmium allowed change in utility of any state in iteration
        for iteration in range(iterations):
            initial_utility = np.copy(self.utility_matrix)
            # delta is the actual change in utlity of any state
            delta = 0
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    self.position_x, self.position_y = row, col
                    if self.maze.layout[row][col] == 'W':
                        # Skip Value Iteration if tile is a wall
                        continue
                    new_utility = self.calculate_utility(initial_utility)
                    for dir in range(len(CARDINAL_DIRECTIONS)):
                        delta = max(delta, abs(initial_utility[row][col][dir]) - new_utility[dir])
                        initial_utility[row][col][dir] = new_utility[dir]

            self.utility_matrix = initial_utility
            if delta < epsilon:
                print(f"Converged after {iteration} iterations.")
                break
        print(self.utility_matrix)
        self.determine_policy()
        

    def determine_policy(self):
        #Initialise map of same size
        policy = np.full((self.maze.cols, self.maze.rows), None)
        value_map = np.full((self.maze.cols, self.maze.rows), None)
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                # print(self.utility_matrix[row][col])
                policy[row][col] = CARDINAL_DIRECTIONS[np.argmax(self.utility_matrix[row][col])]
                value_map[row][col] = round(max(self.utility_matrix[row][col]),3)
        print(policy)
        print(value_map)