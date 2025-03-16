import numpy as np
import map
from copy import deepcopy
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
        self.policy_map = np.full((self.maze.cols, self.maze.rows), CARDINAL_DIRECTIONS[0])
        # Possible moveset per state
        # In accordance to CARDINAL_DIRECTIONS
        moveset_utility = np.zeros(4)
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
        for action in CARDINAL_DIRECTIONS:
            reward = self.get_reward(self.position_x, self.position_y, action)
            utility = self.bellman_update(utility_matrix,self.position_x, self.position_y, action)
            total = reward + (DISCOUNT_FACTOR * utility)
            state_utility.append(total)
        return state_utility

    
    def get_reward(self, x, y, action):
        if self.check_move(action):
            new_x, new_y = self.move(action)
            return REWARD[self.maze.layout[new_x][new_y]]
        else:
            return REWARD[self.maze.layout[x][y]]
    
    def bellman_update(self, utility_matrix, x, y, action):
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
            initial_utility = deepcopy(self.utility_matrix)
            # delta is the actual change in utlity of any state
            delta = 0
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    self.position_x, self.position_y = row, col
                    if self.maze.layout[row][col] == 'W':
                        # Skip Value Iteration if tile is a wall
                        for dir in range(len(CARDINAL_DIRECTIONS)):
                            # Set all values to negative inf
                            initial_utility[row][col][dir] = -np.inf
                        continue
                    new_utility = self.calculate_utility(self.utility_matrix)
                    for dir in range(len(CARDINAL_DIRECTIONS)):
                        delta = max(delta, abs((initial_utility[row][col][dir]) - new_utility[dir]))
                        initial_utility[row][col][dir] = new_utility[dir]

            self.utility_matrix = initial_utility
            if delta < epsilon:
                print(f"Converged after {iteration} iterations. Delta: {delta}")
                break
        # print(self.utility_matrix)
        
    def policy_iteration(self, iterations, epsilon):
        for iteration in range(iterations):
            policy_changed = False
            # Step 1: Policy Evaluation => Computing Utility of all states with policy's move
            while True:
                initial_utility = deepcopy(self.utility_matrix)
                delta = 0.0
                for row in range(self.maze.rows):
                    for col in range(self.maze.cols):
                        # Go through the policy first
                        self.position_x, self.position_y = row, col
                        action = self.policy_map[row][col]
                        action_pos = CARDINAL_DIRECTIONS.index(action)
                        old_value = initial_utility[row][col][action_pos]
                        if self.maze.layout[row][col] == 'W':
                                # Skip if current tile is a wall
                                for dir in range(len(CARDINAL_DIRECTIONS)):
                                    # Set all values to negative inf
                                    initial_utility[row][col][dir] = -np.inf
                                continue
                        new_value = self.policy_evaluation(row, col, self.policy_map[row][col], self.utility_matrix)
                        initial_utility[row][col][action_pos] = new_value
                        delta = max(delta, abs(old_value - new_value))
                print(initial_utility)
                break
                self.utility_matrix = initial_utility
                if(delta < epsilon):
                    break
            # Step 2: Policy Improvement => Calculate new policy based on updated utilities
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    if self.maze.layout[row][col] == 'W':
                        continue
                    old_action = self.policy_map[row][col]
                    new_values = []
                    for action in CARDINAL_DIRECTIONS:
                        new_value = self.policy_evaluation(row, col, action, initial_utility)
                        new_values.append(new_value)
                    max_value_action_pos = np.argmax(new_values)
                    self.policy_map[row][col] = CARDINAL_DIRECTIONS[max_value_action_pos]
                    if self.policy_map[row][col] != old_action:
                        policy_changed = True
                    else:
                        # print(row,col)
                        # print(self.policy_map[row][col], old_action)
                        # print(new_values)
                        pass
            if not policy_changed:
                # print(iteration)
                # print(initial_utility)
                return iteration




    def policy_evaluation(self, row, col, action, utility_matrix):
        reward = self.get_reward(row, col, action) 
        utility = self.get_utility(row, col, action, utility_matrix)
        return reward + DISCOUNT_FACTOR * utility

    def get_utility(self, x, y, action, utility_matrix):
        # To get the utility of the next state
        action_pos = CARDINAL_DIRECTIONS.index(action)
        utility = 0
        # Get the utility of the next state
        if self.check_move(CARDINAL_DIRECTIONS[action_pos]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[action_pos])
            next_action_pos = CARDINAL_DIRECTIONS.index(self.policy_map[new_x][new_y])
            # Take the utility from the next move as defined by the policy
            utility += PROBABILITY_OF_SUCCESS * utility_matrix[new_x][new_y][next_action_pos]
        else:
            # Fail to move means stay in the same position
            utility += PROBABILITY_OF_SUCCESS * utility_matrix[x][y][action_pos]
        # Check the utility of the next state if agent moves to the right of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos + 1) % 4])
            next_action_pos = CARDINAL_DIRECTIONS.index(self.policy_map[new_x][new_y])
            utility += PROBABILITY_OF_FAILURE * utility_matrix[new_x][new_y][next_action_pos]
        else:
            utility += PROBABILITY_OF_FAILURE * utility_matrix[x][y][action_pos]
        # Check the utility of the next state if agent moves to the left of the
        # intended direction
        if self.check_move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4]):
            new_x, new_y = self.move(CARDINAL_DIRECTIONS[(action_pos - 1) % 4])
            next_action_pos = CARDINAL_DIRECTIONS.index(self.policy_map[new_x][new_y])
            utility += PROBABILITY_OF_FAILURE * utility_matrix[new_x][new_y][next_action_pos]
        else:
            utility += PROBABILITY_OF_FAILURE * utility_matrix[x][y][action_pos]

        return utility
    
    def determine_policy(self):
        #Initialise map of same size
        policy = np.full((self.maze.cols, self.maze.rows), None)
        value_map = np.full((self.maze.cols, self.maze.rows), None)
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                # print(self.utility_matrix[row][col])
                if np.isneginf(np.argmax(self.utility_matrix[row][col])):
                    continue
                policy[row][col] = CARDINAL_DIRECTIONS[np.argmax(self.utility_matrix[row][col])]
                value_map[row][col] = round(max(self.utility_matrix[row][col]),3)
        return policy, value_map