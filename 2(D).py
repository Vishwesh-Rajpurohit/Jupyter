import copy

# Target positions for each manuscript to calculate Manhattan Distance
# Goal State mapping: 1 2 3 / 4 5 6 / 7 B 8
GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 2)
}


class AdversarialPuzzle:
    def __init__(self, start_state):
        self.start_state = start_state
        self.minimax_nodes = 0
        self.alphabeta_nodes = 0

    def get_manhattan_utility(self, state):
        """Utility function: Negative Manhattan distance (MAX wants 0, MIN wants highly negative)"""
        distance = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 'B':
                    goal_r, goal_c = GOAL_POSITIONS[val]
                    distance += abs(r - goal_r) + abs(c - goal_c)
        return -distance

    def get_neighbors(self, state):
        """Generates valid adjacent board states by moving the 'B' blank space."""
        neighbors = []
        b_r, b_c = -1, -1

        # Find 'B'
        for r in range(3):
            for c in range(3):
                if state[r][c] == 'B':
                    b_r, b_c = r, c
                    break

        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_r, new_c = b_r + dr, b_c + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_state = [row[:] for row in state]  # Deep copy
                # Swap
                new_state[b_r][b_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[b_r][b_c]
                neighbors.append(new_state)

        return neighbors

    def minimax(self, state, depth, is_max_player):
        """Standard Minimax algorithm bounded by depth."""
        self.minimax_nodes += 1

        # Terminal condition: Depth limit reached or Goal state reached (utility == 0)
        utility = self.get_manhattan_utility(state)
        if depth == 0 or utility == 0:
            return utility

        if is_max_player:
            best_val = float('-inf')
            for neighbor in self.get_neighbors(state):
                val = self.minimax(neighbor, depth - 1, False)
                best_val = max(best_val, val)
            return best_val
        else:  # MIN player (System Glitch)
            best_val = float('inf')
            for neighbor in self.get_neighbors(state):
                val = self.minimax(neighbor, depth - 1, True)
                best_val = min(best_val, val)
            return best_val

    def alphabeta(self, state, depth, alpha, beta, is_max_player):
        """Minimax algorithm optimized with Alpha-Beta Pruning."""
        self.alphabeta_nodes += 1

        utility = self.get_manhattan_utility(state)
        if depth == 0 or utility == 0:
            return utility

        if is_max_player:
            best_val = float('-inf')
            for neighbor in self.get_neighbors(state):
                val = self.alphabeta(neighbor, depth - 1, alpha, beta, False)
                best_val = max(best_val, val)
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break  # Beta cut-off
            return best_val
        else:
            best_val = float('inf')
            for neighbor in self.get_neighbors(state):
                val = self.alphabeta(neighbor, depth - 1, alpha, beta, True)
                best_val = min(best_val, val)
                beta = min(beta, best_val)
                if beta <= alpha:
                    break  # Alpha cut-off
            return best_val


# --- Execution ---
if __name__ == "__main__":
    # A slightly scrambled state to evaluate
    initial_state = [
        [1, 2, 3],
        [4, 'B', 6],
        [7, 5, 8]
    ]

    SEARCH_DEPTH = 6
    game = AdversarialPuzzle(initial_state)

    print("--- Running Plain Minimax ---")
    mm_utility = game.minimax(initial_state, SEARCH_DEPTH, True)
    print(f"Utility Score: {mm_utility}")
    print(f"States Evaluated: {game.minimax_nodes}")

    print("\n--- Running Alpha-Beta Pruning ---")
    ab_utility = game.alphabeta(initial_state, SEARCH_DEPTH, float('-inf'), float('inf'), True)
    print(f"Utility Score: {ab_utility}")
    print(f"States Evaluated: {game.alphabeta_nodes}")

    print("\n--- Efficiency Analysis ---")
    savings = 100 - (game.alphabeta_nodes / game.minimax_nodes * 100)
    print(f"Alpha-Beta evaluated {savings:.2f}% fewer states while returning the exact same utility.")
