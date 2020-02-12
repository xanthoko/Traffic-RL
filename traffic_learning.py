import numpy as np

PATH_ARRAY = np.array([[1, 1], [1, 1], [1, 1], [1, 0]])
height, width = PATH_ARRAY.shape

gamma = 0.75  # Discount factor
alpha = 0.9  # Learning rate

location_to_state = lambda x: x[0] * PATH_ARRAY.shape[1] + x[1]
state_to_location = lambda x: divmod(x, PATH_ARRAY.shape[1])

max_state = location_to_state((height - 1, width - 1))

actions = [0, 1, 2, 3, 4]  # stay, left, down, right, up

rewards = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 1, 1],
                    [0, 1, 1, 0, 1], [0, 0, 1, 1, 1], [0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])

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

        ending_state = location_to_state(end_location)
        rewards_new[ending_state] = [999, 0, 0, 0, 0]  # goal is to stay at state 6

        for i in range(iterations):
            current_state = np.random.randint(0, max_state)

            playable_actions = [
                x for x in range(len(actions)) if rewards_new[current_state, x]
            ]
            if not playable_actions:
                continue

            direction = np.random.choice(playable_actions)
            if direction == 1:
                next_state = current_state - 1
            elif direction == 2:
                next_state = current_state + 2
            elif direction == 3:
                next_state = current_state + 1
            elif direction == 4:
                next_state = current_state - 2
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

    # Get the optimal route
    def get_optimal_route(self, start_location, end_location, next_location, route,
                          Q):

        while (next_location != end_location):
            starting_state = self.location_to_state(start_location)
            next_state = np.argmax(Q[starting_state, ])
            next_location = self.state_to_location(next_state)
            route.append(next_location)
            start_location = next_location

        print(route)


qagent = QAgent(alpha, gamma, location_to_state, actions, rewards,
                state_to_location, Q)

qagent.training((0, 0), (0, 1), 100)
