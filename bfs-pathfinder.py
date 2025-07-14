from collections import deque

def bfs_shortest_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))

    return None
print("Enter the maze row by row, using 1 for paths and 0 for walls (e.g., 10101):")
maze = []

while True:
    row = input("Enter a row (or press Enter to finish): ")
    if not row:
        if maze:
            break
        else:
            print("You must enter at least one row.")
    else:
        maze.append(list(map(int, row)))
if not maze or any(len(row) != len(maze[0]) for row in maze):
    print("Invalid maze. All rows must have the same number of columns.")
else:
    try:
        start = tuple(map(int, input("Enter the start point as x,y: ").split(",")))
        end = tuple(map(int, input("Enter the end point as x,y: ").split(",")))
        path = bfs_shortest_path(maze, start, end)
        if path:
            print("Shortest path found:", path)
        else:
            print("No path found.")
    except (ValueError, IndexError):
        print("Invalid input for start or end point.")