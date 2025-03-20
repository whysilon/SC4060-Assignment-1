import matplotlib.pyplot as plt
import numpy as np
import map
import agent as a
# Layout given by assignment
# G = +1
# W = wall
# B = -1
# S = start

ASSIGNMENT_LAYOUT = [
    (0, 0, 'G'),
    (0, 1, 'W'),
    (0, 2, 'G'),
    (0, 5, 'G'),
    (1, 1, 'B'),
    (1, 3, 'G'),
    (1, 4, 'W'),
    (1, 5, 'B'),
    (2, 2, 'B'),
    (2, 4, 'G'),
    (3, 2, 'S'),
    (3, 3, 'B'),
    (3, 5, 'G'),
    (4, 1, 'W'),
    (4, 2, 'W'),
    (4, 3, 'W'),
    (4, 4, 'B')
]

def plot_policy(agent: a.Agent, policy_map, value_map, title):
    arrow_map = {
        'North': '↑',  
        'South': '↓',  
        'East': '→',   
        'West': '←'    
    }
    colour_map = {
        'W' : 'black',
        'S' : 'green',
        'B' : 'brown',
        'G' : 'lightgreen',
        'N' : 'white',
    }
    fig, ax = plt.subplots(figsize=(agent.maze.rows,agent.maze.cols))
    for r in range(agent.maze.rows):
        for c in range(agent.maze.cols):
            action = policy_map[r][c]
            tile_colour = colour_map[agent.maze.layout[r][c]]
            ax.add_patch(plt.Rectangle((c - 0.5, agent.maze.rows - 1 - r - 0.5), 1, 1, color=tile_colour))
            if agent.maze.layout[r][c] == 'W':
                # If Wall, dont add arrow onto tile
                continue
            if action in arrow_map:
                ax.text(c, agent.maze.rows - 1 - r, arrow_map[action], ha='center', va='center', fontsize=14, color='black')
                ax.text(c, agent.maze.rows - 1 - r - 0.2, value_map[r][c],ha='center', va='center', fontsize=10, color='black')
    ax.set_xticks(np.arange(agent.maze.cols))
    ax.set_yticks(np.arange(agent.maze.rows))
    ax.set_xticks(np.arange(agent.maze.cols + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(agent.maze.rows + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.title(title)
    plt.show()

# Initialize the map layout
assignment_map = map.create_layout_from_list(6, 6, ASSIGNMENT_LAYOUT)
assignment_map.display()

# Value Iteration Agent
value_iter_agent = a.Agent(assignment_map,3,2)
value_iter_agent.value_iteration(1000,0.1)
policy, maxValueMap = value_iter_agent.determine_policy()
plot_policy(value_iter_agent, policy, maxValueMap, "Optimal Policy Map")

# Policy Iteration
# policy_iter_agent = a.Agent(assignment_map,3,2)
# policy = policy_iter_agent.policy_iteration(2, 0.01)
# _ , maxValueMap = policy_iter_agent.determine_policy()
# plot_policy(policy_iter_agent, policy_iter_agent.policy_map, maxValueMap, "Optimal Policy Map")