#pip install -e gym-examples

import gym_examples
import gym
import pandas as pd
import unittest
from hamcrest import assert_that, equal_to

#Create an instance of the HUNLTH environment
env = gym.make('gym_examples/HUNLTH-v0')

class TestHUNLenv_actions(unittest.TestCase):
    
    def test_fold_game_over_preflop(self):
        #env.stage = 1
        #env.dealer = True
        action = 7  #FOLD 
        env.reset()
        env.step(action)
        action = 0  #FOLD 
        env.step(action)
        #env.step(action)
        assert_that(env.terminated, equal_to(True))

if __name__ == '__main__':
    unittest.main()


    