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
        #print(hand)
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
        test_hand = [('♦', '10'),('♦', 'J')]    #10♦, J♦
        test_cc = [('♦', 'Q'),('♦', 'K'),('♦', 'A')]        #Q♦, K♦, A♦
        sc = env.hand_ranking_score(test_hand, test_cc)
        assert_that(sc, equal_to('Royal Flush'))

    def test_hand_ranking_straight_flush_success(self):
        test_hand = [('♦', '2'),('♦', '3')]    
        test_cc = [('♦', '5'),('♦', '4'),('♦', '6')]        
        sc = env.hand_ranking_score(test_hand, test_cc)
        assert_that(sc, equal_to('Straight Flush'))

    def test_hand_ranking_straight_success(self):
        test_hand = [('♦', '2'),('♠', '3')]    
        test_cc = [('♥', '5'),('♦', '4'),('♣', '6')]        
        sc = env.hand_ranking_score(test_hand, test_cc)
        assert_that(sc, equal_to('Straight'))

    def test_hand_ranking_flush_success(self):
        test_hand = [('♦', '4'),('♦', 'Q')]    
        test_cc = [('♦', '5'),('♦', 'K'),('♦', '6')]        
        sc = env.hand_ranking_score(test_hand, test_cc)
        assert_that(sc, equal_to('Flush'))

    def test_hand_ranking_four_kind_success(self):
        hand = [('♥', '5'),('♥', '5')]
        cc = [('♦', '5'),('♠', '5'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('Four of a kind'))

    def test_hand_ranking_full_house_success(self):
        hand = [('♥', '5'),('♥', '5')]
        cc = [('♦', '7'),('♠', '7'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('Full House'))

    def test_hand_ranking_three_kind_success(self):
        hand = [('♥', '4'),('♥', '5')]
        cc = [('♦', '7'),('♠', '7'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('Three of a kind'))

    def test_hand_ranking_two_pair_success(self):
        hand = [('♥', '4'),('♥', '5')]
        cc = [('♦', '5'),('♠', '7'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('Two pair'))

    def test_hand_ranking_pair_success(self):
        hand = [('♥', '4'),('♥', '5')]
        cc = [('♦', 'Q'),('♠', 'Q'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('Pair'))
    
    def test_hand_ranking_pair_success(self):
        hand = [('♥', '2'),('♥', '5')]
        cc = [('♦', '4'),('♠', 'Q'),('♥', '7')]  
        assert_that(env.hand_ranking_score(hand, cc), equal_to('High Card'))

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
    
    def test_check_duplicates_success(self):
        pips = ['2', '2', 'Q', 'Q', 'K']
        num_pips = env.convert_pips(pips)
        assert_that(env.check_duplicates(num_pips), equal_to(True))
    
    def test_get_duplicates(self):
        pips = ['2', '2', '3', '3', '4']
        assert_that(env.get_duplicates(pips), equal_to([2,2]))

    def test_check_duplicates_fail(self):
        pips = ['3', '2', 'J', 'Q', 'K']
        num_pips = env.convert_pips(pips)
        assert_that(env.check_duplicates(num_pips), equal_to(False))

if __name__ == '__main__':
    unittest.main()


    