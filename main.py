import map
import agent as a
ASSIGNMENT_LAYOUT = [
    (0, 0, 'P'),
    (0, 1, 'W'),
    (0, 2, 'P'),
    (0, 5, 'P'),
    (1, 1, 'M'),
    (1, 3, 'P'),
    (1, 4, 'W'),
    (1, 5, 'M'),
    (2, 2, 'M'),
    (2, 4, 'P'),
    (3, 2, 'S'),
    (3, 3, 'M'),
    (3, 5, 'P'),
    (4, 1, 'W'),
    (4, 2, 'W'),
    (4, 3, 'W'),
    (4, 4, 'M')
]
# Initialize the map layout
assignment_map = map.create_layout_from_list(6, 6, ASSIGNMENT_LAYOUT)
assignment_map.display()

agent = a.Agent(assignment_map,3,2)