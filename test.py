import heapq

# Constants
WIDTH, HEIGHT = 10, 10

# Initialize grid with obstacles (1 for obstacles, 0 for empty cells)
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
obstacles = [(1, 1), (2, 3), (3, 5), (4, 7)]

for obstacle in obstacles:
    x, y = obstacle
    grid[y][x] = 1



# A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal, grid):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current_node
            neighbor = x + dx, y + dy

            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and not grid[neighbor[1]][neighbor[0]]:
                new_cost = cost_so_far[current_node] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current_node

    return None




# Test the algorithm
start = (0, 0)
goal = (9, 9)

path = astar(start, goal, grid)

if path:
    print("Path found:", path[1:])
else:
    print("No path found")
