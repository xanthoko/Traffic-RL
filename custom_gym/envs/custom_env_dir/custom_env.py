import gym
import numpy as np
from gym import spaces

STARTING_DISTANCE = 3

STARTING_POSITION = (0, 0)
GOAL_POSITION = (3, 0)
PATH_ARRAY = np.array([[1, 0], [1, 1], [1, 1], [1, 0]])


class TrafficEnv(gym.Env):
    def __init__(self):
        self.time_passed = 0
        self.distance_to_goal = STARTING_DISTANCE

        self.current_position = STARTING_POSITION

        # path followed
        self.path = [STARTING_POSITION]

        # possible actions: stay, left, forward, right
        self.action_space = spaces.Discrete(4)

        # distance to goal, time passed
        self.observation_space = spaces.Discrete(2)

    def step(self, action):
        if action == 1:
            # left
            target_position = (self.current_position[0],
                               self.current_position[1] - 1)
            if target_position[1] >= 0 and PATH_ARRAY[target_position]:
                # chaged index is non-negative and path element is not 0
                self.current_position = target_position
        elif action == 2:
            # forward
            target_position = (self.current_position[0] + 1,
                               self.current_position[1])
            if target_position[0] < PATH_ARRAY.shape[0] and PATH_ARRAY[
                    target_position]:
                # chaged index is inside PATH_ARRAY and path element is not 0
                self.current_position = target_position
        elif action == 3:
            # right
            target_position = (self.current_position[0],
                               self.current_position[1] + 1)
            if target_position[1] < PATH_ARRAY.shape[1] and PATH_ARRAY[
                    target_position]:
                # chaged index is inside PATH_ARRAY and path element is not 0
                self.current_position = target_position

        self.path.append(self.current_position)

        self.time_passed += 1

        done = self.current_position == GOAL_POSITION
        reward = 100 - self.time_passed

        return {}, reward, done, {}

    def reset(self):
        self.distance_to_goal = STARTING_DISTANCE
        self.time_passed = 0

    def render(self):
        copy_path_array = PATH_ARRAY.copy()
        for traveled_point in self.path:
            # asign the value 2 to every traveled point in the starting path
            copy_path_array[traveled_point] = 2

        replace_map = {0: '', 1: 'o', 2: '*'}
        # replace the values of the traveled path according to the replace map
        paths = [[replace_map[x[0]], replace_map[x[1]]] for x in copy_path_array]

        # convert the path to a printable format
        printable_path = '\n'.join([' '.join(x) for x in paths])
        # add a seperation line
        printable_path += '\n-------------------'
        print(printable_path)
