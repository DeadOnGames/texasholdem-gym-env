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
        env.set_dealer(True)
        action = 7  #SB 
        env.step(action)
        action = 0  #FOLD 
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

    def test_preflop_check(self):
        env.reset()
        env.set_dealer(True) #Dealer goes first
        env.step(7) #Make a SB to start 
        for i in range(5):
            env.step(1) #CHECK action
        assert_that(env.stage, equal_to(1)) #Test that a check will remain in the preflop stage 
    
    def test_preflop_bet_ALL_IN(self):
        env.reset()
        env.set_dealer(True) #Dealer goes first
        env.step(7) #Make a SB to start 
        env.step(6) #All in bet
        assert_that(env.money_player_1, equal_to(0))

    def test_preflop_bet_RAISE_2POT(self):
        env.reset()
        env.set_dealer(True) #Dealer goes first
        env.step(7) #Make a SB to start 
        pot_before = env.pot
        env.step(3) #Raise half pot
        pot_after = env.pot
        predicted_pot = pot_before * 1.5
        assert_that(pot_after, equal_to(predicted_pot))



if __name__ == '__main__':
    unittest.main()


    