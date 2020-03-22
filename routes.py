class RoutePlan:
    def __init__(self, shape, connections, max_time):
        self.connections = connections
        self.height = shape[0]
        self.width = shape[1]
        self.max_time = max_time

        self.rewards = []
        # The rewards array has a length of all the points of the route
        for _ in range(self.width * self.height * max_time):
            self.rewards.append([0, 0, 0, 0, 0])

        self.max_state = self.location_to_state((self.width - 1, self.height - 1),
                                                max_time - 1)

    def location_to_state(self, location, time):
        """Converts given 3d location (x, y, time) to state.

        State increases horizontally.

        Args:
            location (tuple): location coordinates
            time (integer): Time passed
        Returns:
            integer: The state
        """
        return int((location[0] * self.width + location[1]) * self.max_time + time)

    def location_to_simple_state(self, location):
        """Converts given location (x, y) to simple state (no time involved).

        State increases horizontally.

        Args:
            location (tuple): location coordinates
        Returns:
            integer: The state
        """
        return int((location[0] * self.width + location[1]))

    def state_to_location(self, state):
        """Converts given state to 3d location (x, y, time).

        Args:
            state (integer): The state
        Returns:
            tuple: (x,y) location and time passed
        """
        location, time = divmod(state, self.max_time)
        x, y = divmod(location, self.width)
        return (int(x), int(y)), time

    def form_rewards(self):
        """Forms the rewards array base on the given connections."""

        for connection in self.connections:
            # get the index of the starting and end points of the connection
            start_index = self.location_to_state(connection[0], 0)
            end_index = self.location_to_state(connection[1], 0)

            start, end = connection
            diffy = end[0] - start[0]
            diffx = end[1] - start[1]

            if not (diffx + diffy):
                # same connection edges (no move)
                continue

            direction = 0
            if diffy:
                if diffy > 0:
                    direction = 2
                else:
                    direction = 4
            if diffx:
                if diffx > 0:
                    direction = 3
                else:
                    direction = 1

            self._set_reward_value(start_index, end_index, direction)
            # max state for connection edges
            max_state_start = self.location_to_state(connection[0],
                                                     self.max_time - 1)
            max_state_end = self.location_to_state(connection[1], self.max_time - 1)
            # set "stay" as the only possible action when time = max_time
            self.rewards[max_state_start] = [1, 0, 0, 0, 0]
            self.rewards[max_state_end] = [1, 0, 0, 0, 0]

    def add_light(self, location, time_start, duration):
        """Adds the light logic by setting 'stay' as the only possible action in
        the state described by the location and time.

        Args:
            location (tuple): X and Y
            time_start (integer): The time the light is turning red for the first
                time
            duration (integer): The duration of the light (same for green and red)
        """
        min_state = self.location_to_state(location, 0)
        max_state = self.location_to_state(location, self.max_time - 1)

        # times the red light is on
        # if time_start = 2, duration = 3, max_time = 10
        # _ _ - - - _ _ _ - -, where '_' is green and '-' red
        for i in range(time_start, self.max_time, duration * 2):
            for redd in range(i, i + duration):
                if min_state + redd <= max_state:
                    self.rewards[min_state + redd] = [1, 0, 0, 0, 0]

    def _set_reward_value(self, start, end, direction):
        """Sets the reward value of the given indexes and direction.

        Args:
            start (integer): The index of the starting connection
            end (integer): The index of the ending connection
            direction (integer): The index of the direction
        """
        for i in range(self.max_time - 1):
            dir_relation_map = {1: 3, 3: 1, 4: 2, 2: 4}
            self.rewards[start + i][direction] = 1
            self.rewards[end + i][dir_relation_map[direction]] = 1


if __name__ == '__main__':
    connections = [[(0, 0), (0, 1)], [(0, 0), (1, 0)], [(0, 1), (1, 1)],
                   [(1, 0), (1, 1)]]
    rp = RoutePlan((2, 2), connections, 4)
    rp.form_rewards()
    rp.add_light((0, 1), 1, 2)
