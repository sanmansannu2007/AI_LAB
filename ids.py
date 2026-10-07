from collections import deque

# Goal state
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


# Generate possible moves
def get_neighbors(state):
    neighbors = []

    blank = state.index(0)

    row = blank // 3
    col = blank % 3

    # Up
    if row > 0:
        new_state = list(state)
        new_state[blank], new_state[blank - 3] = \
            new_state[blank - 3], new_state[blank]
        neighbors.append(tuple(new_state))

    # Down
    if row < 2:
        new_state = list(state)
        new_state[blank], new_state[blank + 3] = \
            new_state[blank + 3], new_state[blank]
        neighbors.append(tuple(new_state))

    # Left
    if col > 0:
        new_state = list(state)
        new_state[blank], new_state[blank - 1] = \
            new_state[blank - 1], new_state[blank]
        neighbors.append(tuple(new_state))

    # Right
    if col < 2:
        new_state = list(state)
        new_state[blank], new_state[blank + 1] = \
            new_state[blank + 1], new_state[blank]
        neighbors.append(tuple(new_state))

    return neighbors


# Print puzzle
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()





# ---------------------------------------
# IDS
# ---------------------------------------

def depth_limited_search(state, depth, path):

    if state == GOAL:
        return path

    if depth == 0:
        return None

    for neighbor in get_neighbors(state):

        if neighbor not in path:

            result = depth_limited_search(
                neighbor,
                depth - 1,
                path + [neighbor]
            )

            if result is not None:
                return result

    return None


def ids(start):

    depth = 0

    while True:

        result = depth_limited_search(
            start,
            depth,
            [start]
        )

        if result is not None:
            return result

        depth += 1


# ---------------------------------------
# MAIN PROGRAM
# ---------------------------------------

start = (2, 1, 3,
         0, 4, 6,
         7, 5, 8)


print("INITIAL STATE")
print_puzzle(start)






# IDS
print("========== IDS ==========")

ids_solution = ids(start)

print("Number of moves:", len(ids_solution) - 1)

for i, state in enumerate(ids_solution):
    print("Step", i)
    print_puzzle(state)