from collections import deque # Library for reduce time complixty
import heapq # used to create a priority queue.

class SearchAlgorithm:
    @staticmethod
    def bfs_maze(map_server):

        # Get maze size (rows, columns)
        rows, cols = map_server.getSize()

        # Starting and target positions (tuples: (row, col))
        start = map_server.start_pos
        target = map_server.target_pos

        # BFS queue — start with the starting position
        queue = deque([start])

        # Set of visited cells to avoid repeating work (cycle is harmfull)
        visited = set()
        visited.add(start)

        # Dictionary for reconstructing the final path
        parents = {
            start: None }

        # Possible movements:
        # (change_row, change_col, required_wall_index)
        directions = [
            (0, 1, 0, 2),   # Move RIGHT  → check Right wall
            (0, -1, 2, 0),  # Move LEFT   → check Left wall
            (-1, 0, 1, 3),  # Move UP     → check Top wall
            (1, 0, 3, 1)    # Move DOWN   → check Bottom wall
        ]

        # BFS Loop — runs until the queue is empty
        while queue:

            # Remove the first cell from the queue (FIFO)
            row, colmun = queue.popleft()

            # If we reached the target → end BFS
            if (row, colmun) == target:
                print("Target found!")
                SearchAlgorithm.print_path(parents, start, target)
                return

            # Get the cell information (walls, objects)
            cell = map_server.getRoom(row, colmun)

            # Try all 4 possible directions dr = change in row, dc = change in column, wall_idx = which wall corresponds to this direction
            for dr, dc, wall_idx in directions:

                # If there is a wall → cannot move in this direction
                if cell["walls"][wall_idx] == 1:
                    continue

                # New cell coordinates nr = new row, nc = new colmun
                nr = row + dr
                nc = colmun + dc

                # Check boundaries (must stay inside the maze)
                if (nr < 0 or nr >= rows or nc < 0 or nc >= cols):
                    continue

                # If this new cell was not visited → use it
                if (nr, nc) not in visited:
                    visited.add((nr, nc))           # Mark as visited
                    parents[(nr, nc)] = (row, colmun)      # Store parent (for path)
                    queue.append((nr, nc))          # Add to BFS queue

        # If queue becomes empty without reaching target
        print("No path found")

    @staticmethod
    def print_path(parents, start, goal):
        # List to store the final path
        path = []

        # Begin from goal and move backwards using parents
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parents[cur]

        # Reverse so path starts at "start" and ends at "goal"
        path.reverse()

        # Display path
        print("Path:", path)
            
    @staticmethod
    def heuristic(a, b): # a current postion , b is goal
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # calculate distence

    @staticmethod
    def get_neighbors(map_server, row, col): # Return valid neighbors based on walls
        neighbors = []
        cell = map_server.getRoom(row, col)

        # walls = [Right, Top, Left, Down]
        # Right
        if cell["walls"][0] == 0:
            neighbors.append((row, col + 1))
        # Top
        if cell["walls"][1] == 0:
            neighbors.append((row - 1, col))
        # Left
        if cell["walls"][2] == 0:
            neighbors.append((row, col - 1))
        # Down
        if cell["walls"][3] == 0:
            neighbors.append((row + 1, col))
        return neighbors

    @staticmethod
    def greedy(map_server):
        start = map_server.start_pos
        target = map_server.target_pos

        # Priority Queue: (heuristic, position)
        open_list = []
        heapq.heappush(open_list, (SearchAlgorithm.heuristic(start, target), start))

        visited = set()
        parent = {start: None}

        while open_list:
            current = heapq.heappop(open_list)
            if current == target:
                return SearchAlgorithm.reconstruct_path(parent, target)

            if current in visited:
                continue

            visited.add(current)
            for neighbor in SearchAlgorithm.get_neighbors(map_server, current[0], current[1]):
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = current
                    h = SearchAlgorithm.heuristic(neighbor, target)
                    heapq.heappush(open_list, (h, neighbor))
        return None

    @staticmethod
    def reconstruct_path(parent, target):
        path = []
        current = target

        while current is not None:
            path.append(current)
            current = parent[current]

        return path[::-1] # revers the path (back from target to start)
