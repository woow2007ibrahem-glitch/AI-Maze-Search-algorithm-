from src.map_server import MapServer
from src.maze_viewer import MazeViewer
from src.search_algorithms import SearchAlgorithm

def main():
    # # 1. Initialize MapServer
    my_map = MapServer(rows=10, cols=10, start_x=0, start_y=0)
    
    # # 2. Generate the initial maze
    my_map.generate_maze()
     
    # # 3. Launch the Viewer
    # The viewer now has a Menu Bar (File/Test) to save, load, and re-assign!
    app = MazeViewer(my_map)

    # 4. Greedy algorithm + BFS

    # BFS: Start → Object
    path_start_to_object = SearchAlgorithm.bfs_maze(my_map)

    # Greedy: Object → Target
    path_object_to_target = SearchAlgorithm.greedy_object_to_target(my_map)
    if path_start_to_object and path_object_to_target:
        full_path = path_start_to_object + path_object_to_target[1:]
        print("Final Path")
        print(full_path)
    else:
        print("Path not found")

if __name__ == "__main__":
    main()