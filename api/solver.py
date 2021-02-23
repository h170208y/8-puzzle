from sys import maxsize

# from copy import deepcopy

_dispatcher = {}


def _copy_list(l, dispatch):
    ret = l.copy()
    for idx, item in enumerate(ret):
        cp = dispatch.get(type(item))
        if cp is not None:
            ret[idx] = cp(item, dispatch)
    return ret


def _copy_dict(d, dispatch):
    ret = d.copy()
    for key, value in ret.items():
        cp = dispatch.get(type(value))
        if cp is not None:
            ret[key] = cp(value, dispatch)

    return ret


_dispatcher[list] = _copy_list
_dispatcher[dict] = _copy_dict


def deepcopy(sth):
    cp = _dispatcher.get(type(sth))
    if cp is None:
        return sth
    else:
        return cp(sth, _dispatcher)


def reverse(s):
    if len(s) == 0:
        return s
    else:
        return reverse(s[1:]) + s[0]


def get_neighbor_of_state(state_to_check_config, state_space_configs_dictionary):
    neighbors_list = []

    idx_of_0 = state_to_check_config.index(0)

    if idx_of_0 != 0 and idx_of_0 != 3 and idx_of_0 != 6:
        new_state_var_config = deepcopy(state_to_check_config)
        new_state_var_config[idx_of_0], new_state_var_config[idx_of_0 - 1] = new_state_var_config[idx_of_0 - 1], \
                                                                             new_state_var_config[idx_of_0]

        if str(new_state_var_config) not in state_space_configs_dictionary:
            state_space_configs_dictionary[str(new_state_var_config)] = ("L", maxsize)
            neighbors_list.append(new_state_var_config)

    if idx_of_0 != 2 and idx_of_0 != 5 and idx_of_0 != 8:

        new_state_var_config = deepcopy(state_to_check_config)
        new_state_var_config[idx_of_0], new_state_var_config[idx_of_0 + 1] = new_state_var_config[idx_of_0 + 1], \
                                                                             new_state_var_config[idx_of_0]

        if str(new_state_var_config) not in state_space_configs_dictionary:
            state_space_configs_dictionary[str(new_state_var_config)] = ("R", maxsize)
            neighbors_list.append(new_state_var_config)

    if idx_of_0 != 0 and idx_of_0 != 1 and idx_of_0 != 2:
        new_state_var_config = deepcopy(state_to_check_config)
        new_state_var_config[idx_of_0], new_state_var_config[idx_of_0 - 3] = new_state_var_config[idx_of_0 - 3], \
                                                                             new_state_var_config[idx_of_0]
        if str(new_state_var_config) not in state_space_configs_dictionary:
            state_space_configs_dictionary[str(new_state_var_config)] = ("U", maxsize)
            neighbors_list.append(new_state_var_config)

    if idx_of_0 != 6 and idx_of_0 != 7 and idx_of_0 != 8:
        new_state_var_config = deepcopy(state_to_check_config)
        new_state_var_config[idx_of_0], new_state_var_config[idx_of_0 + 3] = new_state_var_config[idx_of_0 + 3], \
                                                                             new_state_var_config[idx_of_0]
        if str(new_state_var_config) not in state_space_configs_dictionary:
            state_space_configs_dictionary[str(new_state_var_config)] = ("D", maxsize)
            neighbors_list.append(new_state_var_config)

    return neighbors_list


def get_shortest_path_for_this_state(goal_state_config, initial_state_config, state_space_dict):
    state_space_dict[str(goal_state_config)] = ("", 0)

    FIFS_queue_to_traverse_in_BFS = []

    FIFS_queue_to_traverse_in_BFS.append(goal_state_config)

    while len(FIFS_queue_to_traverse_in_BFS) != 0:
        state_to_check_config = FIFS_queue_to_traverse_in_BFS[0]

        FIFS_queue_to_traverse_in_BFS.pop(0)

        neighbors = get_neighbor_of_state(state_to_check_config, state_space_dict)

        for neighbor_config in (neighbors):

            state_space_dict[str(neighbor_config)] = (
                state_space_dict[str(state_to_check_config)][0] + state_space_dict[str(neighbor_config)][0],
                state_space_dict[str(neighbor_config)][1])

            if state_space_dict[str(neighbor_config)][1] == maxsize:
                FIFS_queue_to_traverse_in_BFS.append(neighbor_config)
                state_space_dict[str(neighbor_config)] = state_space_dict[str(neighbor_config)][0], \
                                                         state_space_dict[str(neighbor_config)][1] + 1

                if neighbor_config == initial_state_config:
                    return state_space_dict[str(neighbor_config)][0]
                else:
                    return ''


def ShortestPath(goal_state_config, list_of_initial_states_config):
    list_of_solutions_for_all_initial_states = []
    state_space = {}

    for initial_state_config in list_of_initial_states_config:
        deepcopy_of_state_space = deepcopy(state_space)
        shortest_path_for_this_state = get_shortest_path_for_this_state(goal_state_config, initial_state_config,
                                                                        deepcopy_of_state_space)
        list_of_solutions_for_all_initial_states.append(str(reverse(shortest_path_for_this_state)))
    return list_of_solutions_for_all_initial_states


def get_solution(board):
    current_goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    initial_states = [board, board]
    initial_state = [[1, 2, 3, 4, 5, 6, 8, 7, 0], [8, 3, 4, 0, 7, 1, 6, 2, 5]]

    paths = ShortestPath(current_goal_state, initial_states)  # [1, 2, 3, 4, 8, 5, 6, 7, 0]]) DRRULLDR
    if len(paths[0]) == 0:
        solution = 'No Solution'
    else:
        solution = paths[0]
    print("moves:", solution)
