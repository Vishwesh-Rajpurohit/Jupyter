import time
from heapq import heappush, heappop



# ---------------------------------------------------------
def parse_board(line):

    valid_chars = [c for c in line if c in '12345678B']

    # Pack into a 3x3 tuple so it can be hashed in our Visited set
    board = (
        tuple(valid_chars[0:3]),
        tuple(valid_chars[3:6]),
        tuple(valid_chars[6:9])
    )
    return board


# ---------------------------------------------------------
# Manhattan Distance Heuristic (h_2)
# ---------------------------------------------------------
def get_manhattan(state, goal):
    distance = 0

    goal_positions = {}
    for r in range(3):
        for c in range(3):
            goal_positions[goal[r][c]] = (r, c)

    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 'B':  # We don't count the blank space
                goal_r, goal_c = goal_positions[val]
                distance += abs(r - goal_r) + abs(c - goal_c)
    return distance


# ---------------------------------------------------------
# Generate valid moves (Up, Down, Left, Right)
# ---------------------------------------------------------
def get_neighbors(state):
    neighbors = []
    # Find the blank 'B'
    b_row, b_col = -1, -1
    for r in range(3):
        for c in range(3):
            if state[r][c] == 'B':
                b_row, b_col = r, c
                break

    # Possible moves: Up, Down, Left, Right
    moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]

    for dr, dc, move_name in moves:
        new_r, new_c = b_row + dr, b_col + dc

        # Check if move stays inside the 3x3 grid
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            # Convert tuple to list of lists so we can swap
            new_state = [list(row) for row in state]
            # Swap 'B' with the target tile
            new_state[b_row][b_col], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[b_row][b_col]
            # Convert back to tuple
            new_state_tuple = tuple(tuple(row) for row in new_state)
            neighbors.append((new_state_tuple, move_name))

    return neighbors


# ---------------------------------------------------------
# A* Search Algorithm Core
# ---------------------------------------------------------
def solve_puzzle(start, goal):
    # Priority queue stores: (f_score, g_score, current_state, path_taken)
    queue = []
    start_h = get_manhattan(start, goal)
    heappush(queue, (start_h, 0, start, []))

    visited = set()
    states_explored = 0

    while queue:
        f, g, current, path = heappop(queue)

        if current in visited:
            continue

        visited.add(current)
        states_explored += 1

        # Check if we reached the goal state
        if current == goal:
            return True, path, states_explored

        # Explore neighbors
        for neighbor_state, move_name in get_neighbors(current):
            if neighbor_state not in visited:
                new_g = g + 1  # Path cost is 1 per move
                new_h = get_manhattan(neighbor_state, goal)
                new_f = new_g + new_h
                new_path = path + [move_name]

                heappush(queue, (new_f, new_g, neighbor_state, new_path))

    # If queue empties and no goal found
    return False, [], states_explored


# ---------------------------------------------------------
# Main Execution - Reads File and Prints Required Output
# ---------------------------------------------------------
def main():
    try:
        # Read the file line by line
        with open("input.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip() != ""]

        if len(lines) < 2:
            print("Error: input.txt must have at least two lines (start state and goal state).")
            return

        start_state = parse_board(lines[0])
        goal_state = parse_board(lines[1])

    except FileNotFoundError:
        print("Error: 'input.txt' not found! Please create it in the same folder.")
        return

    # Start the timer
    start_time = time.time()

    # Run the search
    success, path, explored_count = solve_puzzle(start_state, goal_state)

    # Stop the timer
    end_time = time.time()
    total_time = end_time - start_time

    # --- ---
    print("\n--- Manuscript Sorting Results ---")
    if success:
        print("Success/Failure: Success")
    else:
        print("Success/Failure: Failure")

    print("Heuristic/Parameters used: A* Search with Manhattan Distance (h2)")

    if success:
        print(f"The (Sub)Optimal Path: {' -> '.join(path)}")
    else:
        print("The (Sub)Optimal Path: None")

    print(f"Total States Explored: {explored_count}")
    print(f"Total Time Taken: {total_time:.5f} seconds\n")


if __name__ == "__main__":
    main()

