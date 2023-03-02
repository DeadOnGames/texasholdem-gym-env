#pip install -e gym-examples

import gym_examples
import gym
import pandas as pd
import unittest
from hamcrest import assert_that, equal_to

#Create an instance of the HUNLTH environment
env = gym.make('gym_examples/HUNLTH-v0')

class TestHUNLenv(unittest.TestCase):

    def test_deal_hand(self):
        env.create_deck()
        hand = env.deal_hand()
        assert_that(len(hand), equal_to(2))

#    def test_hand_ranking_random(self):    #Simulates a showdown 
#        deck = env.create_deck()

#        test_hand = env.deal_hand()
#        pip, suit = test_hand[0]
#        pip, suit = test_hand[1]
        
#        test_cc = env.dealCards(3)
#        sc = env.hand_ranking_score(test_hand, test_cc)
#        assert_that(sc != None, equal_to(True))

    def test_check_same_suit(self):
        suits = ['♦','♦','♦','♦','♦']
        assert_that(env.check_same_suit(suits), equal_to(True))

    def test_check_Royal_Flush_success(self):
        #Assume all cards are the same suit
        pips = ['10','11','12','13','14']
        assert_that(env.check_royal_flush(pips), equal_to(True))

    def test_hand_ranking_full_house(self):
        test_hand = [('♦', '10'),('♦', 'J')]    #10♦, J♦
        test_cc = [('♦', 'Q'),('♦', 'K'),('♦', 'A')]        #Q♦, K♦, A♦
        sc = env.hand_ranking_score(test_hand, test_cc)
        assert_that(sc, equal_to('Royal Flush'))

    def test_convert_pips(self):
        pips = ['Q', '10', 'J', 'Q', 'K']
        #print(env.convert_pips(pips))
        assert_that(env.convert_pips(pips), equal_to(['12', '10', '11', '12', '13']))

    def test_check_consecutive_numerical_success(self):
        pips = ['2', '3', '4', '5', '6']
        assert_that(env.check_consecutive(pips), equal_to(True))

    def test_check_consective_non_numerical(self):
        pips = ['9', '10', 'J', 'Q', 'K']
        num_pips = env.convert_pips(pips)

        assert_that(env.check_consecutive(num_pips), equal_to(True))

if __name__ == '__main__':
    unittest.main()


    