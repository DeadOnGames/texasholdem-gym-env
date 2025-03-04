#pip install -e gym-examples

import gym_examples
import gym
import pandas as pd
import unittest
from hamcrest import assert_that, equal_to

#Create an instance of the HUNLTH environment
env = gym.make('gym_examples/HUNLTH-v0')

class TestHUNLenv_two_players(unittest.TestCase):
    
    def test_both_players_play_before_stage_end(self):
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 
        assert_that(env.stage, equal_to(1))

    def test_players_hands(self):
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 
        assert_that(env.hand_state, not(equal_to([None] * 2)))
        assert_that(env.p2_hand_state, not(equal_to([None] * 2)))

    def test_check_two_players(self):
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        env.set_dealer(True)
        env.set_player_num(1)
        env.step(1) #Player1 checks

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(3) #Player2 raises by half pot

        assert_that(env.stage, equal_to(1))     #A check shouldn't progress stage

    def test_call_two_players(self):
        env.reset()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        assert_that(env.pot, equal_to(15)) 
        pot_before = env.pot    #£15

        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot (+£7.5)
        assert_that(env.bet_amount, equal_to(7.5)) 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(2) #Player2 calls
        #assert_that(env.p2_bet_amount, equal_to(7.5)) 

        pot_after = env.pot
        assert_that(pot_after, equal_to(pot_before * 2))     #Pot should have been raised by 100%

    def test_two_player_win_by_fold(self):

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
        env.step(2) #Player2 calls
    
        #-----------Flop-------------
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(0) #Player2 folds

        assert_that(env.terminated, True)
        assert_that(env.won, equal_to(True))
        #env.render()    #Player 1 wins!
    
    def test_two_player_win_by_showdown(self):

        #-----------Prepreflop-------0
        
        env.reset()
        #env.render()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(7) #Player1 makes a SB to start 

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(8) #Player2 makes a BB 

        #-----------Preflop---------1
        #env.render()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot (+£7.5)

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(2) #Player2 calls
    
        #-----------Flop-------------2
        #env.render()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(3) #Player2 raises by half pot

        #-----------Turn-------------3
        #env.render()
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(3) #Player2 raises by half pot 
        #assert_that(env.bet_amount, equal_to(5))
        #-----------River-------------
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(3) #Player1 raises by half pot

        env.set_dealer(False)
        env.set_player_num(2)
        env.step(3) #Player2 raises by half pot 

        #-----------Showdown-------------
        env.render()
        assert_that(env.stage, equal_to(5))   #Showdown stage
        assert_that(env.reward, not(equal_to(0)))
        #print("Terminated = " + str(env.terminated) + " Reward = " + str(env.reward))
        assert_that(env.terminated, equal_to(True))

if __name__ == '__main__':
    unittest.main()


    