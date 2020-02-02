import gym
import envs
import numpy as np

env = gym.make("traffic-v0")
env.reset()

done = False
while not done:
    # action = 2
    action = np.random.randint(1, env.action_space.n)

    new_state, reward, done, _ = env.step(action)
else:
    env.render()
    print('Done')
