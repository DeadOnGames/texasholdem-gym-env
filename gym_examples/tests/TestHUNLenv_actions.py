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
        #-----------Prepreflop-------
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        #-----------Preflop---------
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot (+£7.5)

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(0) #Player2 folds

        assert_that(env.terminated, equal_to(True))

    def test_small_blind_success(self):

        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #SB

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #BB

        assert_that(env.pot, equal_to(15))

    def test_small_blind_failure(self):
        env.reset()
        env.set_dealer(False)
        action = 7  #SB
        env.step(action)
        assert_that(env.pot, equal_to(0))

    def test_preflop_check(self):
        #-----------Prepreflop-------
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        env.set_dealer(True)
        env.set_player_num(1)
        for i in range(5):
            env.step(1) #CHECK action
        
        assert_that(env.stage, equal_to(1)) #Test that a check will remain in the preflop stage 
    
    def test_preflop_bet_ALL_IN(self):
        env.reset()
        #-----------Prepreflop-------
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        #-----------Preflop---------
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(6) #Player1 raises by half pot (+£7.5)

        assert_that(env.money_player_1, equal_to(0))

    def test_preflop_bet_RAISE_2POT(self):

        #-----------Prepreflop-------
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 
        pot_before = env.pot    #£15
        assert_that(pot_before, equal_to(15))

        #-----------Preflop---------
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot (+£7.5)
        assert_that(env.bet_amount, equal_to(7.5)) #Amount of money player 1 has bet £7.5
        assert_that(env.stage_complete, equal_to(True))

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(3) #Player2 raises by half pot (+£7.5)
        #assert_that(env.p2_stage_complete, equal_to(True))
        #assert_that(env.p2_bet_amount, equal_to(7.5))   #Amount of money player 2 has bet

        pot_after = env.pot
        predicted_pot = pot_before * 2
        #assert_that(pot_after, equal_to(predicted_pot))
        assert_that(env.stage, equal_to(2))



if __name__ == '__main__':
    unittest.main()


    