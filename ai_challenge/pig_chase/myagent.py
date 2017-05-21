from collections import namedtuple
from time import sleep
import numpy as np
from common import ENV_ACTIONS

from malmopy.agent import AStarAgent


class MyAgent(AStarAgent):
    ACTIONS = ENV_ACTIONS
    Neighbour = namedtuple('Neighbour', ['cost', 'x', 'z', 'direction', 'action'])

    def __init__(self, name, pig, collaborator, visualizer=None):
        super(MyAgent, self).__init__(name, len(MyAgent.ACTIONS),
                                      visualizer=visualizer)
        self._pig = str(pig)
        self._previous_target_pos = None
        self._collaborator = str(collaborator)
        self._action_list = []
        self._retries = 5
        self._actions_left = 25

    def act(self, state, reward, done, is_training=False):
        self._actions_left = self._actions_left - 1
        if done:
            self._action_list = []
            self._previous_target_pos = None
            self._retries = 5
            self._actions_left = 25

        if state is None:
            return np.random.randint(0, self.nb_actions)

        entities = state[1]
        state = state[0]

        me = [(j, i) for i, v in enumerate(state) for j, k in enumerate(v) if self.name in k]
        me_details = [e for e in entities if e['name'] == self.name][0]
        yaw = int(me_details['yaw'])
        direction = ((((yaw - 45) % 360) // 90) - 1) % 4  # convert Minecraft yaw to 0=north, 1=east etc.
        pig = [(j, i) for i, v in enumerate(state) for j, k in enumerate(v) if self._pig in k]
        collaborator = [(j, i) for i, v in enumerate(state) for j, k in enumerate(v) if self._collaborator in k]

        if len(collaborator) == 0:
            return np.random.randint(0, self.nb_actions)

        target = pig

        if pig == [(2, 2)]:
            if collaborator == [(3, 2)]:
                target = [(2, 3)]
            elif collaborator == [(2, 3)]:
                target = [(3, 2)]
        elif pig == [(6, 2)]:
            if collaborator == [(5, 2)]:
                target = [(6, 3)]
            elif collaborator == [(6, 3)]:
                target = [(5, 2)]
        elif pig == [(2, 6)]:
            if collaborator == [(2, 5)]:
                target = [(3, 6)]
            elif collaborator == [(3, 6)]:
                target = [(2, 5)]
        elif pig == [(6, 6)]:
            if collaborator == [(5, 6)]:
                target = [(6, 5)]
            elif collaborator == [(6, 5)]:
                target = [(5, 6)]
        elif pig == [(2, 3)]:
            if collaborator == [(2, 2)]:
                target = [(2, 4)]
            elif collaborator == [(2, 4)]:
                target = [(2, 2)]
        elif pig == [(3, 2)]:
            if collaborator == [(2, 2)]:
                target = [(4, 2)]
            elif collaborator == [(4, 2)]:
                target = [(2, 2)]
        elif pig == [(5, 2)]:
            if collaborator == [(6, 2)]:
                target = [(4, 2)]
            elif collaborator == [(4, 2)]:
                target = [(6, 2)]
        elif pig == [(6, 3)]:
            if collaborator == [(6, 2)]:
                target = [(6, 4)]
            elif collaborator == [(6, 4)]:
                target = [(6, 2)]
        elif pig == [(6, 5)]:
            if collaborator == [(6, 6)]:
                target = [(6, 4)]
            elif collaborator == [(6, 4)]:
                target = [(6, 6)]
        elif pig == [(5, 6)]:
            if collaborator == [(6, 6)]:
                target = [(4, 6)]
            elif collaborator == [(4, 6)]:
                target = [(6, 6)]
        elif pig == [(3, 6)]:
            if collaborator == [(2, 6)]:
                target = [(4, 6)]
            elif collaborator == [(4, 6)]:
                target = [(2, 6)]
        elif pig == [(2, 5)]:
            if collaborator == [(2, 4)]:
                target = [(2, 6)]
            elif collaborator == [(2, 6)]:
                target = [(2, 4)]
        elif pig == [(4, 3)]:
            if collaborator == [(4, 2)]:
                target = [(4, 4)]
            elif collaborator == [(4, 4)]:
                target = [(4, 2)]
        elif pig == [(5, 4)]:
            if collaborator == [(4, 4)]:
                target = [(6, 4)]
            elif collaborator == [(6, 4)]:
                target = [(4, 4)]
        elif pig == [(4, 5)]:
            if collaborator == [(4, 4)]:
                target = [(4, 6)]
            elif collaborator == [(4, 6)]:
                target = [(4, 4)]
        elif pig == [(3, 4)]:
            if collaborator == [(4, 4)]:
                target = [(2, 4)]
            elif collaborator == [(2, 4)]:
                target = [(4, 4)]
        # Bail mission conditions
        elif pig == [(4, 6)] or pig == [(4, 2)] or pig == [(2, 4)] or pig == [(6, 4)] or pig == [(4, 4)]:
            if self._retries > 0:
                sleep(5)
                self._retries = self._retries - 1
                return MyAgent.ACTIONS.index("turn 1")  # substitutes for a no-op command
            else:
                # Find closest lapis_block and set it as the target
                target_lapis_block_1 = [(1, 4)]
                target_lapis_block_2 = [(7, 4)]
                if (abs(me[0][0] - 1) + abs(me[0][1] - 4)) < (abs(me[0][0] - 7) + abs(me[0][1] - 4)):
                    target = target_lapis_block_1
                else:
                    target = target_lapis_block_2

        # Get agent and target nodes
        me = MyAgent.Neighbour(1, me[0][0], me[0][1], direction, "")
        target = MyAgent.Neighbour(1, target[0][0], target[0][1], 0, "")

        # If distance to the target is zero, just turn and wait
        if self.heuristic(me, target) == 0:
            return MyAgent.ACTIONS.index("turn 1")  # substitutes for a no-op command

        if not self._previous_target_pos == target:
            # Target has moved, or this is the first action of a new mission - calculate a new action list
            self._previous_target_pos = target

            path, costs = self._find_shortest_path(me, target, state=state)
            self._action_list = []
            for point in path:
                self._action_list.append(point.action)

        if self._action_list is not None and len(self._action_list) > 0:
            action = self._action_list.pop(0)
            return MyAgent.ACTIONS.index(action)

        # reached end of action list - turn on the spot
        return MyAgent.ACTIONS.index("turn 1")  # substitutes for a no-op command

    def neighbors(self, pos, state=None):
        state_width = state.shape[1]
        state_height = state.shape[0]
        dir_north, dir_east, dir_south, dir_west = range(4)
        neighbors = []
        inc_x = lambda x, dir, delta: x + delta if dir == dir_east else x - delta if dir == dir_west else x
        inc_z = lambda z, dir, delta: z + delta if dir == dir_south else z - delta if dir == dir_north else z
        # add a neighbour for each potential action; prune out the disallowed states afterwards
        for action in MyAgent.ACTIONS:
            if action.startswith("turn"):
                neighbors.append(
                    MyAgent.Neighbour(1, pos.x, pos.z, (pos.direction + int(action.split(' ')[1])) % 4, action))
            if action.startswith("move "):
                sign = int(action.split(' ')[1])
                weight = 1 if sign == 1 else 1.5
                neighbors.append(
                    MyAgent.Neighbour(weight, inc_x(pos.x, pos.direction, sign), inc_z(pos.z, pos.direction, sign),
                                      pos.direction, action))

        # now prune:
        valid_neighbours = [n for n in neighbors if
                            n.x >= 0 and n.x < state_width and n.z >= 0 and n.z < state_height and state[
                                n.z, n.x] != 'sand']
        return valid_neighbours

    def heuristic(self, a, b, state=None):
        (x1, y1) = (a.x, a.z)
        (x2, y2) = (b.x, b.z)
        return abs(x1 - x2) + abs(y1 - y2)

    def matches(self, a, b):
        return a.x == b.x and a.z == b.z  # don't worry about dir and action
