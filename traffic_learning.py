import numpy as np
"""State depends on 2 variables. Location and Time passed"""

PATH_ARRAY = np.array([[1, 1, 1], [1, 1, 1], [0, 1, 0]])
height, width = PATH_ARRAY.shape
max_time_passed = 6

gamma = 0.75  # Discount factor
alpha = 0.9  # Learning rate

# (2d indexes converted to 1d) * width + the time passed
location_to_state = lambda x, y: (x[0] * width + x[1]) * max_time_passed + y


def state_to_location(state):
    location, time = divmod(state, max_time_passed)
    x, y = divmod(location, width)
    return (x, y), time


max_state = location_to_state((height - 1, width - 1), max_time_passed - 1)

actions = [0, 1, 2, 3, 4]  # stay, left, down, right, up

pos1_rews = [[0, 0, 1, 0, 0]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos2_rews = [[0, 0, 1, 1, 0]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos3_rews = [[0, 1, 1, 0, 0]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos4_rews = [[0, 0, 0, 1, 1]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos5_rews = [[0, 1, 1, 1, 1]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos6_rews = [[0, 1, 0, 0, 1]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos7_rews = [[0, 0, 0, 0, 0]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos8_rews = [[0, 0, 0, 0, 1]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]
pos9_rews = [[0, 0, 0, 0, 0]
             for x in range(max_time_passed - 1)] + [[1, 0, 0, 0, 0]]

# pos2_rews[3] = [1, 0, 0, 0, 0]  # light logic
pos6_rews[3] = [1, 0, 0, 0, 0]  # light logic

all_pos = (pos1_rews + pos2_rews + pos3_rews + pos4_rews + pos5_rews + pos6_rews +
           pos7_rews + pos8_rews + pos9_rews)
rewards = np.array(all_pos)

Q = np.array(np.zeros([max_state + 1, max_state + 1]))


class QAgent():

    # Initialize alpha, gamma, states, actions, rewards, and Q-values
    def __init__(self, alpha, gamma, location_to_state, actions, rewards,
                 state_to_location, Q):

        self.gamma = gamma
        self.alpha = alpha

        self.location_to_state = location_to_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location

        self.Q = Q

    # Training the robot in the environment
    def training(self, start_location, end_location, iterations):

        rewards_new = np.copy(self.rewards)

        # get the state at the end location for every time
        end_location_states = [
            location_to_state(end_location, x) for x in range(max_time_passed)
        ]
        # set the ending state reward
        for end_state in end_location_states:
            rewards_new[end_state] = [999, 0, 0, 0, 0]  # stay at end location

        for i in range(iterations):
            current_state = np.random.randint(0, max_state)

            playable_actions = [
                x for x in range(len(actions)) if rewards_new[current_state, x]
            ]

            if not playable_actions:
                continue

            direction = np.random.choice(playable_actions)

            if direction == 1:
                current_location, current_time = state_to_location(current_state)
                next_location = (current_location[0], current_location[1] - 1)
                next_state = location_to_state(next_location, current_time + 1)
            elif direction == 2:
                current_location, current_time = state_to_location(current_state)
                next_location = (current_location[0] + 1, current_location[1])
                next_state = location_to_state(next_location, current_time + 1)
            elif direction == 3:
                current_location, current_time = state_to_location(current_state)
                next_location = (current_location[0], current_location[1] + 1)
                next_state = location_to_state(next_location, current_time + 1)
            elif direction == 4:
                current_location, current_time = state_to_location(current_state)
                next_location = (current_location[0] - 1, current_location[1])
                next_state = location_to_state(next_location, current_time + 1)
            else:
                next_state = current_state

            TD = rewards_new[current_state, direction] + self.gamma * self.Q[
                next_state, np.argmax(self.Q[next_state, ]
                                      )] - self.Q[current_state, next_state]

            self.Q[current_state, next_state] += self.alpha * TD

        route = [start_location]
        next_location = start_location

        # Get the route
        self.get_optimal_route(start_location, end_location, next_location, route,
                               self.Q)

        self.rewards_new = rewards_new

    # Get the optimal route
    def get_optimal_route(self, start_location, end_location, next_location, route,
                          Q):

        counter = 0
        while (next_location != end_location):
            starting_state = self.location_to_state(start_location, counter)

            next_state = np.argmax(Q[starting_state, ])
            next_location, counter = self.state_to_location(next_state)
            route.append(next_location)

            start_location = next_location

        print(route)


qagent = QAgent(alpha, gamma, location_to_state, actions, rewards,
                state_to_location, Q)

qagent.training((0, 0), (0, 2), 1000)
