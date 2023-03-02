#!/usr/bin/env python
# coding: utf-8

from enum import Enum
import random
import gym
from gym import spaces
from gym.spaces import Box, Discrete
from gym import Env
import numpy as np
from collections import Counter

class actions(Enum):
    FOLD = 0
    CHECK = 1
    CALL = 2
    RAISE_3BB = 3
    RAISE_HALF_POT = 3
    RAISE_POT = 4
    RAISE_2POT = 5
    ALL_IN = 6
    SMALL_BLIND = 7
    BIG_BLIND = 8

class stage_enum(Enum):
  PREPREFLOP = 0 
  PREFLOP = 1
  FLOP = 2
  TURN = 3
  RIVER = 4
  SHOWDOWN = 5

#1D array - less computationally demanding to iterate
deck = []

#Symbols for cards
clubs = "\u2663"
hearts = "\u2665"
diamonds = "\u2666"
spades = "\u2660"

PIPS = ("A","2","3","4","5","6","7","8","9","10","J","Q","K")
SUITS = (clubs, spades, diamonds, hearts)

class HUNLTH_env(gym.Env):
  metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
  """A Heads-Up No Limit Texas Hold'em environment for OpenAI gym"""

  def __init__(self,  render_mode=None):
    #define environment

    #self.deck = create_deck()  #Create a new deck of cards at the start of the episode
    #self.stage = ...
    self.hand_state = [None] * 2 #Slots for cards in hand
    self.community_cardsState = [None] * 5  #Slots for cards in community pile

    self.money_player_1 = 10000
    self.money_player_2 = 10000
    self.pot = 0 
    self.rounds = 20
    self.collected_reward_player_1 = 0
    self.dealer = True

    # Define action space
    self.action_space = spaces.Discrete(len(actions))

    #Define observation space as a tuple - states are 'slots' not cards
    self.observation_space = spaces.Discrete(10)
    #self.observation_space = spaces.Tuple(spaces.Discrete(7),                 # hand & community cards 
     #                                     spaces.Box(0,20000,shape=(1,)),     # money of player 1
      #                                    spaces.Box(0,20000,shape=(1,)),     # money of player 2
       #                                   spaces.Box(0,40000,shape=(1,)))     # money in the pot

    #Current state
    #At the beginning all card slots will be null and so will the pot

    assert render_mode is None or render_mode in self.metadata["render_modes"]
    self.render_mode = render_mode

    self.window = None
    self.clock = None

  def _get_obs(self):
    #Translates the environment's state into an observation

    #Return tuple
    return spaces.Tuple(self.hand_state, self.community_cards, self.money_player_1, self.money_player_2, self.pot)

  def reset(self):
    #Assume that reset() is called before step()

    #Alternate the dealer
    if self.dealer == True:
      self.dealer = False
    else :
      self.dealer = True

    # Reset the state of the environment to an initial state
    self.hand_state = [None] * 2 #Slots for cards in hand
    self.community_cardsState = [None] * 5  #Slots for cards in community pile
    self.pot = 0 
    self.deck = create_deck()
    self.stage = stage_enum.PREFLOP.value  # 0
    observation = self._get_obs()

    return observation

  def step(self, action):
    # Execute one time step within the environment
    self._take_action(action)
    self.stage += 1

    #terminated = 
    # Terminated signal to signify the end of the game
    # Games ends if either player fold, or after showdown

    reward = ...
    # 0 if game still going
    # pot if game won
    # - money_player_1 if game lost
    

    observation = self._get_obs
    return observation, reward, terminated, False, info

  def _take_action(self, action):

    if self.stage == 0: #----------------PREPREFLOP----------------------------------------------------------------
      #Check dealer status
      if self.dealer:
        if(action == 7):  #SB
          self.money_player_1 -= 5
          pot += 5
        else:
          illegal_move()
      else: # Non-dealer posts BB
        if(action == 8):  #BB
          self.money_player_1 -= 10
          pot += 10
        else:
          illegal_move()

    elif self.stage == 1: #----------------PREFLOP----------------------------------------------------------------
      #Deal hand to each player
      self.hand_state = deal_hand()
      #First round of betting (dealer goes first)
      #if(self.dealer == true):
        #if(action == 0):  #FOLD
          #gameOver()
        #if(action == 1):  #CHECK
          #Wait for opponent
        #if(action == 2):  #CALL
          #
      #else:

    elif self.stage == 3: #----------------FLOP----------------------------------------------------------------
      deal_cards(3)  #Deal 3 community cards
      #Second round of betting (bb goes first)

    elif self.stage == 4: #----------------TURN----------------------------------------------------------------
        #Deal 1 more community card
      deal_cards(1)
      #Third round of betting (bb goes first)

    elif self.stage == 5: #----------------RIVER----------------------------------------------------------------
        #Deal 1 more community card
      deal_cards(1)
      #Forth round of betting (bb goes first)

    elif self.stage == 6: #----------------SHOWDOWN----------------------------------------------------------------
      # Check cards 
      hand_ranking_score(self.hand_state, self.community_cardsState)
      #Compare hand ranking score 
      # Assign reward

    if self.action == 0: #FOLD
      print("Fold")
      #End the game
      #Pot goes to other player
    
    elif self.action == 1: #CALL
      print("Call")
        #Match the money put into the pot by other player

        
    elif self.action == 2: #RAISE
      print("Raise")
        #Add an amount more than the other player's amount into pot
        
    elif self.action == 3: #CHECK
      print("Check")
        #Give away turn to other player to bet first 
        # - can only be performed if player is going first in a round of betting

  def bet(amount):
    
    if(self.dealer == True  and self.stage == 2):    #If player is dealer during pre-flop
        #PlayerOne goes first
        print("Player one goes first") 
    elif(self.dealer == False and self.stage >= 3):   #If player is bb during flop, turn or river
        #Player 1 goes first 
        print("Player one goes first") 
    else:
        #Player 2 goes first 
        print("Player two goes first") 
        
    #Remove money from player currently betting
    self.money_player_1 -= amount
    #Add money to pot
    self.pot += amount

  def illegal_move():
    print("Illegal move")

  def hand_ranking_score(self, hand, cc):
    #Put all cards into an array and prepare for sorting
    ranking_cards = []
    for i in hand:
      ranking_cards.append(i)
    for c in cc:
      ranking_cards.append(c)
    #print(ranking_cards)

    #Separate pips into separate array
    pips = []
    pips = [x[1] for x in ranking_cards]
    #print(pips)
    pips = self.convert_pips(pips)
    #print(pips)

    #Separate suits into separate array
    suits = []
    suits = [x[0] for x in ranking_cards]
    #print(suits)
    
    if(self.check_same_suit(suits)):
      if(self.check_consecutive(pips)):
        if(self.check_royal_flush(pips)):
          return 'Royal Flush'
        else: 
          return 'Straight Flush'
      else:
        return 'Flush'
    else:
      if(self.check_consecutive(pips)):
        return 'Straight'
      else:
        if(self.get_duplicates(pips) == [4]):
          return "Four of a kind"
        elif(self.get_duplicates(pips) == [3,2] or self.get_duplicates(pips) == [2,3]):
          return "Full House"
        elif(self.get_duplicates(pips) == [3]):
          return "Three of a kind"
        elif(self.get_duplicates(pips) == [2,2]):
          return "Two pair"
        elif(self.get_duplicates(pips) == [2]):
          return "Pair"
        else:
          return 'High Card'

  def check_duplicates(self, pips_array):
    a = dict(Counter(pips_array)) #E.g. {'2': 2, '12': 2, '13': 1}
    b = dict()
    for x, y in a.items():
      if(int(y) >= 2):
        b[x] = y
    if(len(b) == 0):
      return False
    else:
      return True
    
  def get_duplicates(self, pips_array):
    a = dict(Counter(pips_array))
    count = []
    for x, y in a.items():
      if(int(y) >= 2):
        count.append(y)
    return count 

  def check_same_suit(self, suits_array):
    if(all(x == suits_array[0] for x in suits_array)):   #Check if all cards are same suit
      return True
    else:
      return False

  def check_consecutive(self, pips_array):
    #Check if cards are sorted numerically
    intpips_array = [eval(i) for i in pips_array]
    if(sorted(intpips_array) == list(range(min(intpips_array), max(intpips_array)+1))):
      return True
    else:
      return False

  def check_royal_flush(self, pips_array):
    count = 10
    trueCount = 0
    for i in range(len(pips_array)):
      if (eval(pips_array[i]) == count):
        trueCount = trueCount + 1
        count = count + 1
    
    if(trueCount == 5):
      return True
    else:
      return False

  def convert_pips(self, pips_array):
    #Check for non-numerical pips
    if(any(not x.isalpha() for x in pips_array)):

      #Change non-numerical elements into numbers 
      for i in range(len(pips_array)):
        if (pips_array[i].isalpha()):
          pips_array[i] = self.assign_numerical_value(pips_array[i])
      return pips_array
    else:
      return pips_array
  
  def assign_numerical_value(self, symbol):
    if(symbol == 'J'):
      return '11'
    elif(symbol == 'Q'):
      return '12'
    elif(symbol == 'K'):
      return '13'
    elif(symbol == 'A'):
      return '14'

  def create_deck(self):
    for suit in SUITS:
        for pip in PIPS:
            card = (suit,pip)
            deck.append(card)
  
  def deal_hand(self):
    hand = []
    for i in range(2):
      card = random.choice(deck)
      deck.remove(card)
      hand.append(card)
    return hand

  def deal_cards(self, numCards):
    community_cards = []
    for i in range(numCards):
      #pip, suit = takeCardFromDeck()
      card = random.choice(deck)
      deck.remove(card)
      community_cards.append(card)
    return community_cards
      

  def deal_entire_deck(self):
    for i in range(13):
        for j in range(4):
            #pip,suit = takeCardFromDeck()
            card = random.choice(deck)
            deck.remove(card)
            pip, suit = card
            print(suit + pip, end = " ")
        print()

#create_deck()
#deal_entire_deck()

