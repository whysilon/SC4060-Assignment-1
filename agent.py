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

    def initalise_utility_matrix(self):
        # Initialize the utility matrix with zeroes
        utility_matrix = np.full((self.maze.cols, self.maze.rows), None)
        moveset_utility = np.zeros(len(CARDINAL_DIRECTIONS))
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                utility_matrix[i][j] = moveset_utility.copy()
        return utility_matrix

    def initialise_policy_map(self):
        # Initialize policy map with their first possible move
        policy_map = np.full((self.maze.cols, self.maze.rows), CARDINAL_DIRECTIONS[0])
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if self.maze.layout[row][col] == 'W':
                    policy_map[row][col] = None
                policy_map[row][col] = self.get_possible_moves(row, col)[0]
        return policy_map

    def get_possible_moves(self, x, y):
        possible_moves = []
        # Move agent based on action
        for action in CARDINAL_DIRECTIONS:
            if self.check_move(action, x, y):
                possible_moves.append(action)
        return possible_moves
            
    def check_move(self, action, x, y):
        # Remember current position
        next_position_x, next_position_y = x, y
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
    
    def move(self, action, x, y):
        # Move agent based on action
        if action == 'East':
            return x, y + 1
        elif action == 'West':
            return x, y - 1
        elif action == 'North':
            return x - 1, y
        elif action == 'South':
            return x + 1, y
        else:
            raise ValueError("Invalid action")

    def get_next_utility(self, utility_matrix, x, y, action):
        # Get utility of the next state
        if self.check_move(action, x, y):
            new_x, new_y = self.move(action,x,y)
            return utility_matrix[new_x][new_y]
        else:
            return utility_matrix[x][y]
    
    def get_reward(self, x, y, action):
        if self.check_move(action, x, y):
            new_x, new_y = self.move(action, x, y)
            return REWARD[self.maze.layout[new_x][new_y]]
        else:
            return REWARD[self.maze.layout[x][y]]
    
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
            self.position_x, self.position_y = self.move(CARDINAL_DIRECTIONS[action_pos], self.position_x, self.position_y)
        else:
            # If agent hits a wall, stay in the same position
            pass
    
    def value_iteration(self, iterations, epsilon):
        # epsilon is the maxmium allowed change in utility of any state in iteration
        utility_matrix = self.initalise_utility_matrix()
        utility_history = {}
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                utility_history[(row, col)] = []
        for iteration in range(iterations):
            initial_utility = utility_matrix.copy()
            # delta is the actual change in utlity of any state
            delta = 0
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    if self.maze.layout[row][col] == 'W':
                        # Skip Value Iteration if tile is a wall
                        for dir in range(len(CARDINAL_DIRECTIONS)):
                            # Set all values to negative inf
                            initial_utility[row][col][dir] = -np.inf
                        continue
                    state_utility = []
                    possible_moves = self.get_possible_moves(row, col)
                    for action in CARDINAL_DIRECTIONS:
                        utility = 0
                        action_pos = CARDINAL_DIRECTIONS.index(action)
                        if action in possible_moves:
                            reward = self.get_reward(row, col, action)
                            next_utility = self.get_next_utility(utility_matrix, row, col, action)
                            utility += PROBABILITY_OF_SUCCESS * max(next_utility)
                            next_utility = self.get_next_utility(utility_matrix, row, col, CARDINAL_DIRECTIONS[(action_pos + 1) % 4])
                            utility += PROBABILITY_OF_FAILURE * max(next_utility)
                            next_utility =  self.get_next_utility(utility_matrix, row, col, CARDINAL_DIRECTIONS[(action_pos - 1) % 4])
                            utility += PROBABILITY_OF_FAILURE * max(next_utility)
                            total = reward + (DISCOUNT_FACTOR * utility)
                            state_utility.append(total)
                        else:
                            state_utility.append(0)
                    for dir in range(len(CARDINAL_DIRECTIONS)):
                        delta = max(delta, abs((initial_utility[row][col][dir]) - state_utility[dir]))
                        initial_utility[row][col][dir] = state_utility[dir]

            utility_matrix[:] = initial_utility
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    utility_history[(row, col)].append(max(utility_matrix[row][col]))
            if delta < epsilon:
                print(f"Converged after {iteration} iterations. Delta: {delta}")
                break
        return utility_matrix, utility_history
        # print(utility_matrix)
        
    def policy_iteration(self, iterations, epsilon):
        utility_matrix = self.initalise_utility_matrix()
        policy_map = self.initialise_policy_map()
        utility_history = {}
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                utility_history[(row, col)] = []
        for iteration in range(iterations):
            policy_changed = False
            # Step 1: Policy Evaluation => Computing Utility of all states with policy's move
            utility_matrix, policy_map, utility_history = self.policy_evaluation(epsilon, utility_matrix, policy_map, utility_history   )
                
            # Step 2: Policy Improvement => Calculate new policy based on updated utilities
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    if self.maze.layout[row][col] == 'W':
                        continue
                    old_action = policy_map[row][col]
                    new_values = []
                    possible_moves = self.get_possible_moves(row, col)
                    for action in CARDINAL_DIRECTIONS:
                        if action in possible_moves:
                            new_value = self.get_q_value(utility_matrix, policy_map, row, col , action)
                            new_values.append(new_value)
                        else:
                            new_values.append(-np.inf)
                    max_value_action_pos = np.argmax(new_values)
                    policy_map[row][col] = CARDINAL_DIRECTIONS[max_value_action_pos]
                    if policy_map[row][col] != old_action:
                        policy_changed = True
                    else:
                        # print(row,col)
                        # print(policy_map[row][col], old_action)
                        # print(new_values)
                        pass

            if not policy_changed:
                print(f"Converged after {iteration} iterations.")
                break
        return utility_matrix, policy_map, utility_history
            
    def policy_evaluation(self, epsilon, utility_matrix, policy_map, utility_history):

        while True:
            initial_utility = utility_matrix.copy()
            delta = 0.0

            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    # Go through the policy first
                    action = policy_map[row][col]
                    if self.maze.layout[row][col] == 'W':
                            # Skip if current tile is a wall
                            for dir in range(len(CARDINAL_DIRECTIONS)):
                                # Set all values to negative inf
                                initial_utility[row][col][dir] = -np.inf
                            continue
                    action_pos = CARDINAL_DIRECTIONS.index(action)
                    old_value = initial_utility[row][col][action_pos]
                    new_value = self.get_q_value(utility_matrix, policy_map, row, col, action)
                    initial_utility[row][col][action_pos] = new_value
                    delta = max(delta, abs(old_value - new_value))
            utility_matrix[:] = initial_utility
            for row in range(self.maze.rows):
                for col in range(self.maze.cols):
                    action = policy_map[row][col]
                    action_pos = CARDINAL_DIRECTIONS.index(action)
                    utility_history[(row, col)].append(utility_matrix[row][col][action_pos])
            if(delta < epsilon):
                break
        # print(utility_matrix)
        # print(policy_map)
        return utility_matrix, policy_map, utility_history
    
    def get_q_value(self, utility_matrix, policy_map, x, y, action):
        next_x, next_y = self.move(action, x, y)
        next_state_action = policy_map[next_x][next_y]
        next_state = self.get_next_utility(utility_matrix, x, y, action)
        next_utility = next_state[CARDINAL_DIRECTIONS.index(next_state_action)]
        reward = self.get_reward(x, y, action)
        new_value = reward + (DISCOUNT_FACTOR * next_utility)
        return new_value

    def determine_policy(self, utility_matrix):
        #Initialise map of same size
        # print(utility_matrix)
        policy = np.full((self.maze.cols, self.maze.rows), None)
        value_map = np.full((self.maze.cols, self.maze.rows), None)
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                # print(utility_matrix[row][col])
                if np.isneginf(np.argmax(utility_matrix[row][col])):
                    continue
                policy[row][col] = CARDINAL_DIRECTIONS[np.argmax(utility_matrix[row][col])]
                value_map[row][col] = round(max(utility_matrix[row][col]),3)
        return policy, value_map