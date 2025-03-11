import map
import agent as a
# Layout given by assignment
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

# Initialize the map layout
assignment_map = map.create_layout_from_list(6, 6, ASSIGNMENT_LAYOUT)
assignment_map.display()

agent = a.Agent(assignment_map,3,5)

print(agent.calculate_utility())