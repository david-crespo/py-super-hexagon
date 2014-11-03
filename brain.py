from a_star import find_path

def decide_left_or_right(parsed_frame):
    '''
    based on the position of the cursor and walls, decide whether to
        1) press left (return 'left')
        2) press right (return 'right')
        3) do nothing (return None)
    '''
    action = None


    return action


class GoalSet:
    def __init__(self, nodes, x_coord):
        self.nodes = nodes
        self.x_coord = x_coord