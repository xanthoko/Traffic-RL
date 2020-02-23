import numpy as np
from routes import RoutePlan


class QAgent():
    def __init__(self, alpha, gamma, actions, rp):

        self.gamma = gamma
        self.alpha = alpha

        self.location_to_state = rp.location_to_state
        self.actions = actions
        self.rewards = rp.rewards
        self.state_to_location = rp.state_to_location
        self.max_state = rp.max_state
        self.max_time_passed = rp.max_time

        self.Q = np.array(np.zeros([rp.max_state + 1, rp.max_state + 1]))

    # Training the robot in the environment
    def training(self, start_location, end_location, iterations):

        rewards_new = np.copy(self.rewards)

        # get the state at the end location for every time
        end_location_states = [
            self.location_to_state(end_location, x)
            for x in range(self.max_time_passed)
        ]
        # set the ending state reward
        for end_state in end_location_states:
            rewards_new[end_state] = [999, 0, 0, 0, 0]  # stay at end location

        for i in range(iterations):
            current_state = np.random.randint(0, self.max_state)

            playable_actions = [
                x for x in range(len(self.actions)) if rewards_new[current_state, x]
            ]

            if not playable_actions:
                continue

            direction = np.random.choice(playable_actions)

            if direction == 1:
                current_location, current_time = self.state_to_location(
                    current_state)
                next_location = (current_location[0], current_location[1] - 1)
                next_state = self.location_to_state(next_location, current_time + 1)
            elif direction == 2:
                current_location, current_time = self.state_to_location(
                    current_state)
                next_location = (current_location[0] + 1, current_location[1])
                next_state = self.location_to_state(next_location, current_time + 1)
            elif direction == 3:
                current_location, current_time = self.state_to_location(
                    current_state)
                next_location = (current_location[0], current_location[1] + 1)
                next_state = self.location_to_state(next_location, current_time + 1)
            elif direction == 4:
                current_location, current_time = self.state_to_location(
                    current_state)
                next_location = (current_location[0] - 1, current_location[1])
                next_state = self.location_to_state(next_location, current_time + 1)
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


def main():
    gamma = 0.75  # Discount factor
    alpha = 0.9  # Learning rate
    actions = [0, 1, 2, 3, 4]  # stay, left, down, right, up

    shape = (2, 2)
    connections = [[(0, 0), (0, 1)], [(0, 0), (1, 0)], [(0, 1), (1, 1)],
                   [(1, 0), (1, 1)]]
    max_time_passed = 4

    rp = RoutePlan(shape, connections, max_time_passed)
    rp.form_rewards()
    rp.add_light((1, 0), 1, 1)

    qagent = QAgent(alpha, gamma, actions, rp)
    qagent.training((0, 0), (1, 1), 1000)

    return


if __name__ == '__main__':
    main()
