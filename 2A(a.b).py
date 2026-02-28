from collections import deque
import time


START = "123B46758"
GOAL = "1234567B8"

def get_neighbors(state):
    """Actions from 1b"""
    blank = state.index('B')
    row, col = divmod(blank, 3)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]  # up down left right
    neighbors = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            swap_idx = nr*3 + nc
            s_list = list(state)
            s_list[blank], s_list[swap_idx] = s_list[swap_idx], s_list[blank]
            neighbors.append(''.join(s_list))
    return neighbors

def bfs(start, goal):
    """2A.a: Breadth First Search - minimum moves"""
    start_time = time.time()
    queue = deque([start])
    visited = {start: None}  # State tracking from Q3
    path_cost = {start: 0}   # Path cost from 1d
    while queue:
        state = queue.popleft()
        if state == goal:
            # Reconstruct path
            path = []
            current = state
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return (True, path, len(visited), path_cost[state],
                   time.time() - start_time)
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                visited[neighbor] = state
                path_cost[neighbor] = path_cost[state] + 1  # 1d
                queue.append(neighbor)
    return (False, [], len(visited), 0, time.time() - start_time)

def dfs(start, goal, max_depth=100):
    """2A.b: Depth First Search"""
    start_time = time.time()
    stack = [(start, 0)]  # (state, depth)
    visited = {start: None}
    path_cost = {start: 0}
    while stack:
        state, depth = stack.pop()
        if state == goal:
            path = []
            current = state
            while current:
                path.append(current)
                current = visited[current]
            path.reverse()
            return (True, path, len(visited), path_cost[state],
                   time.time() - start_time)
        if depth < max_depth:
            for neighbor in get_neighbors(state):
                if neighbor not in visited:
                    visited[neighbor] = state
                    path_cost[neighbor] = path_cost[state] + 1
                    stack.append((neighbor, depth + 1))
    return (False, [], len(visited), 0, time.time() - start_time)

# Run and print results
print("=== BFS Results ===")
success, path, explored, cost, runtime = bfs(START, GOAL)
print(f"Success/Failure: {success}")
print(f"(Sub)Optimal Path length: {len(path)-1 if success else 'N/A'}")
print(f"Total States Explored: {explored}")
print(f"Total Time Taken: {runtime:.3f}s")

print("\n=== DFS Results ===")
success, path, explored, cost, runtime = dfs(START, GOAL)
print(f"Success/Failure: {success}")
print(f"Path length: {len(path)-1 if success else 'N/A'}")
print(f"Total States Explored: {explored}")
print(f"Total Time Taken: {runtime:.3f}s")
