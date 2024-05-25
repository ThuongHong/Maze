from algorithm.data_structure import StackFroniterGreedySearch
from algorithm.data_structure import Node

from utility.draw_utility import draw_two_grids


def get_manhattan_distance(fisrt_position: tuple, second_position: tuple):
    return abs(fisrt_position[0] - second_position[0]) + abs(
        fisrt_position[1] - second_position[1]
    )


def GBFS(
    grids: dict,
    player_current_position: tuple[int],
    player_winning_position: tuple[int],
    is_process: bool = False,
):

    # Keep track which node is explored
    node_explored = []
    all_player_moves = []

    # Initialize a frontier to contain nodes that need to explored
    frontier = StackFroniterGreedySearch()
    start = Node(state=player_current_position, action=None, parent=None)
    frontier.add([start])

    # Loop til find the solution
    while True:
        if frontier.empty():
            if is_process:
                return all_player_moves
            else:
                return []

        node = frontier.remove()
        all_player_moves.append(node.state)

        if node.state == player_winning_position:  # Found the goal
            actions = []
            states = []
            # Backtrack to get the path
            while node.parent is not None:
                actions.append(node.action)
                states.append(node.state)
                node = node.parent

            all_player_moves.pop(0)

            actions.reverse()
            states.reverse()

            if is_process:
                return all_player_moves
            else:
                return list(zip(actions, states))

        # When haven't found the goal yet, add the current node to frontier
        node_explored.append(node.state)

        # This list contains the child nodes of current node
        moves = []
        for action, state in grids[node.state].get_neighbors(is_get_direction=True):
            if not frontier.contains_state(state) and state not in node_explored:

                child = Node(state=state, action=action, parent=node)
                moves.append(child)

                # if screen:
                #     draw_two_grids(grids= grids,
                #                 screen= screen,
                #                 current_grid= node.state,
                #                 next_grid= child.state)

                #     pygame.time.wait(10)

        # Add child nodes that are sorted decreasely by Manhattan distance
        frontier.add(
            sorted(
                moves,
                key=lambda x: get_manhattan_distance(x.state, player_winning_position),
                reverse=True,
            )
        )
