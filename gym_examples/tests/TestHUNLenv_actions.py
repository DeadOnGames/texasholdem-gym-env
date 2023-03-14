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
        env.reset()
        action = 0  #FOLD 
        env.step(action)
        env.step(action)
        env.step(action)
        assert_that(env.terminated, equal_to(True))

    def test_small_blind_success(self):
        env.set_dealer(True)
        action = 7  #SB
        env.reset()
        env.step(action)
        assert_that(env.pot, equal_to(5))

    def test_small_blind_failure(self):
        env.reset()
        env.set_dealer(False)
        action = 7  #SB
        env.step(action)
        assert_that(env.pot, equal_to(0))

if __name__ == '__main__':
    unittest.main()


    