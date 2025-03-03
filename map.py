class MapLayout:
    # Initialize Map with 0s
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.layout = [[0 for _ in range(cols)] for _ in range(rows)]

    def display(self):
        for row in self.layout:
            print(" ".join(map(str, row)))

if __name__ == "__main__":
    rows, cols = 5, 5  # Define the size of the map
    map_layout = MapLayout(rows, cols)
    map_layout.display()