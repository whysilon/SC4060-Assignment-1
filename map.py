class Maze:
    # Initialize Map with 0s
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.layout = [['N' for _ in range(cols)] for _ in range(rows)]

    def display(self):
        for row in self.layout:
            print(" ".join(map(str, row)))


def create_layout_with_input(row,col):
    print("Initializing the map layout")
    layout = Maze(row,col)
    while True:
        # Get the type of node
        user_input = input("Enter the type of node ('S' for start, 'W' for Wall, 'P' for Plus, 'M' for Minus, 'E' to end): ")
        # Get the coordinates
        if (user_input == 'E'):
            break
        coord_input = input("Enter the Coordinates (0-indexed): ")
        x, y = map(int, coord_input.split())
        # Set the node type:
        layout.layout[x][y] = user_input
    return layout
    
def create_layout_from_list(row, col, plan):
    print("Initializing the map layout")
    layout = Maze(row,col)
    for x,y,node in plan:
        layout.layout[x][y] = node

    return layout

if __name__ == "__main__":
    rows, cols = 5, 5  # Define the size of the map
    map_layout = Maze(rows, cols)
    map_layout.display()