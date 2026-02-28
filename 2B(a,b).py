from collections import deque
import heapq
import time

# States from Q1
START = "123B46758"
GOAL = "1234567B8"

def get_neighbors(state):
    blank = state.index('B')
    row, col = divmod(blank, 3)
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            swap_idx = nr*3 + nc
            s_list = list(state)
            s_list[blank], s_list[swap_idx] = s_list[swap_idx], s_list[blank]
            neighbors.append(''.join(s_list))
    return neighbors

def h1(state, goal):
    return sum(1 for s,g in zip(state, goal) if s != g and s != 'B')

def h2(state, goal):
    dist = 0
    for tile in '12345678':
        i = state.index(tile)
        gi = goal.index(tile)
        dist += abs(i//3 - gi//3) + abs(i%3 - gi%3)
    return dist

# 2A BFS
def bfs(start, goal):
    st = time.time()
    q = deque([start])
    visited = {start: None}
    while q:
        state = q.popleft()
        if state == goal:
            path = []
            cur = state
            while cur:
                path.append(cur)
                cur = visited[cur]
            path.reverse()
            return True, len(path)-1, len(visited), time.time()-st
        for nb in get_neighbors(state):
            if nb not in visited:
                visited[nb] = state
                q.append(nb)
    return False, 0, len(visited), time.time()-st

# 2B Greedy + A*
def greedy(start, goal, h):
    st = time.time()
    pq = []
    heapq.heappush(pq, (h(start, goal), start))
    visited = {start: None}
    while pq:
        _, state = heapq.heappop(pq)
        if state == goal:
            path = []
            cur = state
            while cur:
                path.append(cur)
                cur = visited[cur]
            path.reverse()
            return True, len(path)-1, len(visited), time.time()-st
        for nb in get_neighbors(state):
            if nb not in visited:
                visited[nb] = state
                heapq.heappush(pq, (h(nb, goal), nb))
    return False, 0, len(visited), time.time()-st

def a_star(start, goal, h):
    st = time.time()
    pq = []
    g_cost = {start: 0}
    heapq.heappush(pq, (h(start, goal), 0, start))
    visited = {start: None}
    while pq:
        f, g, state = heapq.heappop(pq)
        if state == goal:
            path = []
            cur = state
            while cur:
                path.append(cur)
                cur = visited[cur]
            path.reverse()
            return True, g, len(visited), time.time()-st
        for nb in get_neighbors(state):
            new_g = g + 1
            if nb not in g_cost or new_g < g_cost[nb]:
                g_cost[nb] = new_g
                f_new = new_g + h(nb, goal)
                heapq.heappush(pq, (f_new, new_g, nb))
                visited[nb] = state
    return False, 0, len(visited), time.time()-st

# RUN ALL
print("=== 2A.a BFS ===")
succ, moves, exp, t = bfs(START, GOAL)
print(f"Success: {succ}, Min moves: {moves}, States: {exp}, Time: {t:.3f}s")

print("\n=== 2B.a GREEDY h1 ===")
succ, moves, exp, t = greedy(START, GOAL, h1)
print(f"Success: {succ}, Moves: {moves}, States: {exp}, Time: {t:.3f}s")

print("\n=== 2B.b A* h1 ===")
succ, cost, exp, t = a_star(START, GOAL, h1)
print(f"Success: {succ}, Cost: {cost}, States: {exp}, Time: {t:.3f}s")

print("\n=== 2B.b A* h2 ===")
succ, cost, exp, t = a_star(START, GOAL, h2)
print(f"Success: {succ}, Cost: {cost}, States: {exp}, Time: {t:.3f}s")
