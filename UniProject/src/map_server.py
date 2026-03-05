import json
import random

# ============================================================
# Part 1 :Setup & Infrastructure
# ============================================================

# 1.1:Class Definition & Constructor
class MapServer:
    def __init__ (self, rows=10, cols=10, start_x=0, start_y=0, object_x=None, object_y=None, target_x=None, target_y=None):

        self.rows = rows
        self.cols = cols

        #this is for storing coordinates
        self.start_pos  = (start_x,start_y)
        self.target_pos = (target_x,target_y)
        self.object_pos = (object_x,object_y)
        # in case user did not enter object or target coords
        if target_x is None or target_y is None:
            self.target_pos = (random.randint(0, self.rows - 1),
                               random.randint(0, self.cols - 1))

        if object_x is None or object_y is None:
            self.object_pos = (random.randint(0, self.rows - 1),
                               random.randint(0, self.cols - 1))
        self.maze = []

#1.2: Helper Getters
    def getSize(self):
        return (self.rows ,self.cols)

    def getRoom(self,row,col):
        if((row>=self.rows) or (row<0) or (col>=self.cols) or (col<0)): #this checks if the given row & col within our boundary
            return None 
        else:
            return self.maze[row][col]

# ============================================================
# Part 2 :Preparing JSON methods to read from /load a JSON file
# ============================================================

#2.1: Saving to JSON
    def save_to_file(self,filename):
        mazeData = {
            "rows": self.rows,
            "cols": self.cols,
            "start": self.start_pos,
            "target": self.target_pos,
            "object": self.object_pos,
            "maze": self.maze
        }
        with open(filename,"w") as file:
            json.dump(mazeData, file, indent=4) # this method writes the dictionary info in the given file in JSON format

#2.2: Loading from JSON
    def load_from_file(self,filename):
        with open(filename,"r") as file:
            mazeData = json.load(file) # this method converts the JSON to valid dictionary format
            self.rows   = mazeData["rows"]
            self.cols   = mazeData["cols"]
            self.start_pos  = tuple(mazeData["start"]) # convert it back to tuples
            self.target_pos = tuple(mazeData["target"])
            self.object_pos = tuple(mazeData["object"])
            self.maze   = mazeData["maze"]

# ============================================================
# Part 3 - The Core Logic (building the maze)
# ============================================================

# 3.1: Initialization ; filling the maze with walls
    def generate_maze(self):
        self.maze = []  # Good practice: Clear old maze if re-generating
        for row in range(self.rows):
            row_list = []  # Create the temporary row list
            for col in range(self.cols):
                info = {
                    "walls": [1, 1, 1, 1], # Right , Top, Left , Down
                    "obj": 0,
                    "coords": (row, col),  # I chose (row, col) format not col, row as given in the PDF because it is confusing
                    "cost": 1
                }
                # assign : start object, target, and object to be moved before adding them to the maze
                if (row, col) == self.start_pos:
                    info["obj"] = 2  # start point
                elif (row, col) == self.target_pos:
                    info["obj"] = -1  # target point
                elif (row, col) == self.object_pos:
                    info["obj"] = 1  # object

                row_list.append(info)  #  Append cell to the ROW list
            self.maze.append(row_list)  #  Append the finished row to the MAZE

        #3.2: The Recursive Carver (DFS) : this method will keep digging the walls that we just have initialized
        #here we keep track of our visited cells, eventually no cell has been visited yet..
        self.visited = []
        for row in range(self.rows):
            row_list = []
            for col in range(self.cols):
                row_list.append(False)
            self.visited.append(row_list)

        self.carve(self.start_pos[0],self.start_pos[1])

    def carve(self,row,col):
        self.visited[row][col] = True #1. mark the node as visited
        # (row_change_value, column_change_value,cur_wall,neighbor_wall)
        Directions = [(0, 1, 0, 2), # means we moved to the Right Cell
                        (0,-1, 2, 0),   # .....                 Left Cell
                        (-1, 0, 1, 3),  # Up
                        (1, 0, 3, 1)    #Down
                    ]
        random.shuffle(Directions) #  shuffle them so we pick different direction every time we want to discover unvisited cell

        #here we will loop through possible directions
        for  row_change, col_change, my_wall_index, neighbor_wall_index in Directions:
            new_row = row + row_change
            new_col = col + col_change

            # 1. check bounds
            if new_row < 0 or new_row >= self.rows or new_col < 0 or new_col >= self.cols:
                continue
            # 2. check visited
            if self.visited[new_row][new_col]:
                continue

            # 3. now we will break walls to from the cells that we have chosen
            self.maze[row][col]["walls"][my_wall_index] = 0
            self.maze[new_row][new_col]["walls"][neighbor_wall_index] = 0

            # 4. now call the method recursively
            self.carve(new_row,new_col)

    def assign_objects (self,start_x, start_y, object_x, object_y, target_x, target_y):
        if not self.maze:
            self.generate_maze()
        # Safety check if we called this method beore creating the maze ..
        self.start_pos = (start_x, start_y)
        self.target_pos = (target_x, target_y)
        self.object_pos = (object_x, object_y)

        for row in range(self.rows):
            for col in range(self.cols):
                self.maze[row][col]["obj"] = 0

        self.maze[self.target_pos[0]][self.target_pos[1]]["obj"] = -1
        self.maze[self.object_pos[0]][self.object_pos[1]]["obj"] = 1
        self.maze[self.start_pos[0]][self.start_pos[1]]["obj"] = 2