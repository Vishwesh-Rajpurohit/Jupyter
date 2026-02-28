
import time
import random
import math

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

def ida_dfs(state, g, bound, h, goal, path_set):
    f = g + h(state, goal)
    if f > bound:
        return f, False
    if state == goal:
        return f, True
    min_exceed = float('inf')
    path_set.add(state)
    for nb in get_neighbors(state):
        if nb not in path_set:
            exceed, found = ida_dfs(nb, g+1, bound, h, goal, path_set)
            if found:
                return exceed, True
            min_exceed = min(min_exceed, exceed)
    path_set.remove(state)
    return min_exceed, False

def ida_star(start, goal, h):
    bound = h(start, goal)
    iter_count = 0
    st = time.time()
    while True:
        iter_count += 1
        exceed, found = ida_dfs(start, 0, bound, h, goal, set())
        if found:
            return True, iter_count, time.time() - st
        if exceed == float('inf'):
            return False, iter_count, time.time() - st
        bound = exceed

def annealing(start, goal, h):
    st = time.time()
    current = start
    best = start
    best_score = h(best, goal)
    temp = 5.0
    alpha = 0.95
    visits = 1
    iters = 0
    while temp > 0.1 and iters < 2000:
        iters += 1
        nbs = get_neighbors(current)
        if not nbs: break
        next_state = random.choice(nbs)
        delta = h(next_state, goal) - h(current, goal)
        if delta < 0 or random.random() < math.exp(-delta/temp):
            current = next_state
            visits += 1
        if h(current, goal) < best_score:
            best = current
            best_score = h(current, goal)
        temp *= alpha
    success = best == goal
    return success, visits, time.time() - st

print("IDA* h1:")
succ, iters, t = ida_star(START, GOAL, h1)
print(f"Success: {succ}, Iters: {iters}, Time: {t:.3f}s")

print("\nAnnealing h2:")
succ, visits, t = annealing(START, GOAL, h2)
print(f"Success: {succ}, Visits: {visits}, Time: {t:.3f}s")
