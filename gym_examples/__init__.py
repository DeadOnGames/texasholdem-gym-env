from gym.envs.registration import register

register(
    id="gym_examples/HUNLTH-v0",
    entry_point="gym_examples.envs:HUNLTH_env",
    #max_episode_steps=300,
    #autoreset=True
)
