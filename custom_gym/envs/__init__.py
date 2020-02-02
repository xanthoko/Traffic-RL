from gym.envs.registration import register

register(id='traffic-v0', entry_point='envs.custom_env_dir:TrafficEnv')
