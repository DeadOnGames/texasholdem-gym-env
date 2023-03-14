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
    self.terminated = False
    self.big_blind = 0

    # Define action space
    self.action_space = spaces.Discrete(len(actions))

    #Define observation space as a tuple - states are 'slots' not cards
    self.observation_space = spaces.Discrete(10)

    assert render_mode is None or render_mode in self.metadata["render_modes"]
    self.render_mode = render_mode

    self.window = None
    self.clock = None

  def _get_obs(self):
    #Translates the environment's state into an observation
    return self.hand_state, self.community_cardsState, self.money_player_1, self.money_player_2, self.pot
  
  def __get_info(self):
    #Return some aribrariy info for debugging
    return {"stage": self.stage, "hand": self.hand_state, "Player 1 money": self.money_player_1}

  def reset(self):
    #Assume that reset() is called before step()

    # Reset the state of the environment to an initial state
    self.hand_state = [None] * 2 #Slots for cards in hand
    self.community_cardsState = [None] * 5  #Slots for cards in community pile
    self.pot = 0 
    self.deck = self.create_deck()
    self.stage = stage_enum.PREPREFLOP.value  # 0
    observation = self._get_obs()

    return observation

  def step(self, action):
    # Execute one time step within the environment
    self._take_action(action)
    self.stage += 1

    #terminated = 
    # Terminated signal to signify the end of the game
    # Games ends if either player fold, or after showdown

    #if(self.terminated and self.won): # pot if game won
    #  reward = self.pot                 
    #elif(self.terminated and not won):  # - money_player_1 if game lost
    #  reward = 1 - self.money_player_1  
    #else:  # 0 if game still going
    reward = 0                       

    observation = self._get_obs
    info = self.__get_info()
    return observation, reward, self.terminated, False, info

  def _take_action(self, action):

    a = [2,3,4,5,6] #Array to handle betting action indexes

    if self.stage == 0: #----------------PREPREFLOP----------------------------------------------------------------
      #Check dealer status
      if self.dealer:
        if(action == 7):  #SB
          self.money_player_1 -= 5
          self.pot += 5
        else:
          self.illegal_move()
      else: # Non-dealer posts BB
        if(action == 8):  #BB
          self.money_player_1 -= 10
          self.pot += 10
        else:
          self.illegal_move()

    elif self.stage == 1: #----------------PREFLOP----------------------------------------------------------------
      #Deal hand to each player
      self.hand_state = self.deal_hand()

      #First round of betting (dealer goes first)
      if(self.dealer == True):
        if(action == 0):  #FOLD
          self.game_over()
        elif(action == 1):  #CHECK
          #Wait for opponent]
          print()
        elif(action in a):
          self.bet(action)
        else:
          self.illegal_move()

    elif self.stage == 3: #----------------FLOP----------------------------------------------------------------
      self.deal_cards(3)  #Deal 3 community cards
      #Second round of betting (bb goes first)
      if(self.dealer == False):
        if(action == 0):  #FOLD
          self.game_over()
        elif(action == 1):  #CHECK
          #Wait for opponent
          print()
        elif(action in a):
          self.bet(action)
        else:
          self.illegal_move()

    elif self.stage == 4 or 5: #----------------TURN / RIVER ---------------------------------------------------------
        #Deal 1 more community card
      self.deal_cards(1)
      #Third round of betting (bb goes first)
      if(self.dealer == False):
        if(action == 0):  #FOLD
          self.game_over()
        elif(action == 1):  #CHECK
          #Wait for opponent
          print()
        elif(action in a):
          self.bet(action)
        else:
          self.illegal_move()

    elif self.stage == 6: #----------------SHOWDOWN----------------------------------------------------------------
      # Check cards 
      hand_rank = self.hand_ranking_score(self.hand_state, self.community_cardsState)
      #if player1 hand_rank == player2 hand_rank:
        #Calculate inter-hand ranking

      #Compare hand ranking score 
      # Assign reward

  def bet_handler(self, action):  #Called if action 2,3,4,5 or 6 are used
    #if(self.dealer == True  and self.stage == 1):    #If player is dealer during pre-flop
        #PlayerOne goes first
    #    print("Player one goes first")
    #elif(self.dealer == False and self.stage >= 2):   #If player is bb during flop, turn or river
        #Player 1 goes first 
    #    print("Player one goes first") 
    #else:
        #Player 2 goes first 
    #    print("Player two goes first") 
        
    if(action == 2): #Call
      self.bet(-1)      #Need to hook up to player 2 
    elif(action == 3): #RASIE_3BB
      self.bet(self.big_blind * 3)
    elif(action == 4): #RAISE_HALF_POT
      self.bet(self.pot * 0.5)
    elif(action == 5):  #RAISE_POT
      self.bet(self.pot * 2)
    elif(action == 6):  #RASIE_2POT
      self.bet(self.pot * 2)
    elif(action == 7): #ALL_IN
      self.bet(self.money_player_1)

    
  def bet(self, amount):
    #Add money to pot
      self.pot += amount
      #Remove money from player currently betting
      self.money_player_1 -= amount

  def game_over(self):
    self.terminated = True

  def illegal_move(self):
    return "Illegal move"

  def hand_ranking_score(self, hand, cc):
    #Put all cards into an array and prepare for sorting
    ranking_cards = []
    for i in hand:
      ranking_cards.append(i)
    for c in cc:
      ranking_cards.append(c)

    #Separate pips into separate array
    pips = []
    pips = [x[1] for x in ranking_cards]
    pips = self.convert_pips(pips)

    #Separate suits into separate array
    suits = []
    suits = [x[0] for x in ranking_cards]
    
    if(self.check_same_suit(suits)):
      if(self.check_consecutive(pips)):
        if(self.check_royal_flush(pips)):
          return 'royal_flush', self.calc_inter_hand_ranking(5, pips)
        else: 
          return 'straight_flush',self.calc_inter_hand_ranking(5, pips)
      else:
        return 'flush', self.calc_inter_hand_ranking(5,pips)
    else:
      if(self.check_consecutive(pips)):
        return 'straight', self.calc_inter_hand_ranking(5,pips)
      else:
        if(self.get_duplicates(pips) == [4]):
          return "four_of_a_kind", self.calc_inter_hand_ranking(4,pips)
        elif(self.get_duplicates(pips) == [3,2] or self.get_duplicates(pips) == [2,3]):
          return "full_house", self.calc_inter_hand_ranking(5, pips)
        elif(self.get_duplicates(pips) == [3]):
          return "three_of_a_kind", self.calc_inter_hand_ranking(3, pips)
        elif(self.get_duplicates(pips) == [2,2]):
          return "two_pair", self.calc_inter_hand_ranking(4,pips)
        elif(self.get_duplicates(pips) == [2]):
          return "pair", self.calc_inter_hand_ranking(2, pips)
        else:
          return 'high_card', self.calc_inter_hand_ranking(1, pips)

  def check_duplicates_score(self, pips_array):
    a = dict(Counter(pips_array)) #E.g. {'2': 2, '12': 2, '13': 1}
    b = dict()
    for x, y in a.items():
      if(int(y) >= 2):
        b[x] = y
    if(len(b) > 0):
      sum = 0
      for x, y in b.items():
        sum += (int(x) * int(y))
      return sum
    else:
      return 0
    
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
  
  def calc_inter_hand_ranking(self, no_cards, pips_array):
    #Count up cards for inter-hand ranking
    sum = 0 
    if(no_cards == 5):  #Hands were all cards are counted
      for i in pips_array:
        sum += int(i)
      return sum
    elif(no_cards == 1):  #Highest card, return highest number card
      sum = int(pips_array[0])
      for i in pips_array:
        if(eval(i) > sum):
          sum = int(i)
      return sum
    else:
      return self.check_duplicates_score(pips_array) #Hands with duplicates

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
  
  def set_dealer(self, bool):
    self.dealer = bool

#create_deck()
#deal_entire_deck()

