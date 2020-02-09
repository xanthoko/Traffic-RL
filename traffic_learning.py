import gym
import envs
import numpy as np

env = gym.make("traffic-v0")

PATH_ARRAY = np.array([[1, 0], [1, 1], [1, 1], [1, 0]])

EPISODES = 10
LEARNING_RATE = 0.1
DISCOUNT = 0.95
DISCRETE_OS_SIZE = [20, 20]
q_table = np.random.uniform(low=90,
                            high=100,
                            size=(DISCRETE_OS_SIZE + [env.action_space.n]))

for episode in range(EPISODES):
    state = env.reset()
    done = False

    while not done:
        # action = 2
        action = np.random.randint(1, env.action_space.n)

        new_state, reward, done, _ = env.step(action)
        # print(new_state)

        if not done:
            # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_state])

            # Current Q value (for current state and performed action)
            current_q = q_table[state + (action, )]

            # And here's our equation for a new Q value for current state and action
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (
                reward + DISCOUNT * max_future_q)

            # Update Q table with new Q value
            q_table[state + (action, )] = new_q

        # Simulation ended (for any reson) - if goal position is achived
        # update Q value with reward directly
        else:
            # print(f'We did it on episode 0')
            # q_table[discrete_state + (action,)] = reward
            q_table[state + (action, )] = 0

    else:
        env.render()
