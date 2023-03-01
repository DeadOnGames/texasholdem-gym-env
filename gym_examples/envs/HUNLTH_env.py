#!/usr/bin/env python
# coding: utf-8

from enum import Enum
import random
import gym
from gym import spaces
from gym.spaces import Box, Discrete
from gym import Env
import numpy as np

class Actions(Enum):
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

class StageEnum(Enum):
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

    #self.deck = createDeck()  #Create a new deck of cards at the start of the episode
    #self.stage = ...
    self.handState = [None] * 2 #Slots for cards in hand
    self.communityCardsState = [None] * 5  #Slots for cards in community pile

    self.moneyPlayer1 = 10000
    self.moneyPlayer2 = 10000
    self.pot = 0 
    self.rounds = 20
    self.collected_rewardPlayer1 = 0
    self.dealer = True

    # Define action space
    self.action_space = spaces.Discrete(len(Actions))

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
    return spaces.Tuple(self.handState, self.communityCards, self.moneyPlayer1, self.moneyPlayer2, self.pot)

  def reset(self):
    #Assume that reset() is called before step()

    #Alternate the dealer
    if self.dealer == True:
      self.dealer = False
    else :
      self.dealer = True

    # Reset the state of the environment to an initial state
    self.handState = [None] * 2 #Slots for cards in hand
    self.communityCardsState = [None] * 5  #Slots for cards in community pile
    self.pot = 0 
    self.deck = createDeck()
    self.stage = StageEnum.PREFLOP.value  # 0
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
    # - moneyPlayer1 if game lost
    

    observation = self._get_obs
    return observation, reward, terminated, False, info

  def _take_action(self, action):

    if self.stage == 0: #----------------PREPREFLOP----------------------------------------------------------------
      #Check dealer status
      if self.dealer:
        if(action == 7):  #SB
          self.moneyPlayer1 -= 5
          pot += 5
        else:
          illegalMove()
      else: # Non-dealer posts BB
        if(action == 8):  #BB
          self.moneyPlayer1 -= 10
          pot += 10
        else:
          illegalMove()

    elif self.stage == 1: #----------------PREFLOP----------------------------------------------------------------
      #Deal hand to each player
      self.handState = dealHand()
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
      dealCards(3)  #Deal 3 community cards
      #Second round of betting (bb goes first)

    elif self.stage == 4: #----------------TURN----------------------------------------------------------------
        #Deal 1 more community card
      dealCards(1)
      #Third round of betting (bb goes first)

    elif self.stage == 5: #----------------RIVER----------------------------------------------------------------
        #Deal 1 more community card
      dealCards(1)
      #Forth round of betting (bb goes first)

    elif self.stage == 6: #----------------SHOWDOWN----------------------------------------------------------------
      # Check cards 
      handRankingScore(self.handState, self.communityCardsState)
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
    self.moneyPlayer1 -= amount
    #Add money to pot
    self.pot += amount

  def illegalMove():
    print("Illegal move")

  def handRankingScore(self, hand, cc):
    #Put all cards into an array and prepare for sorting
    rankingCards = []
    for i in hand:
      rankingCards.append(i)
    for c in cc:
      rankingCards.append(c)
    #print(rankingCards)

    #Separate pips into separate array
    pips = []
    pips = [x[1] for x in rankingCards]
    #print(pips)
    pips = self.convertPips(pips)
    #print(pips)

    #Separate suits into separate array
    suits = []
    suits = [x[0] for x in rankingCards]
    #print(suits)
    
    if(self.checkSameSuit(suits)):
      if(self.checkConsective(pips)):
        if(self.checkRoyalFlush(pips)):
          return 'Royal Flush'

  def checkSameSuit(self, suitsArray):
    if(all(x == suitsArray[0] for x in suitsArray)):   #Check if all cards are same suit
      return True
    else:
      return False

  def checkConsective(self, pipsArray):
    #Check if cards are sorted numerically
    intPipsArray = [eval(i) for i in pipsArray]
    if(sorted(intPipsArray) == list(range(min(intPipsArray), max(intPipsArray)+1))):
      return True
    else:
      return False

  def checkRoyalFlush(self, pipsArray):
    count = 10
    trueCount = 0
    for i in range(len(pipsArray)):
      if (eval(pipsArray[i]) == count):
        trueCount = trueCount + 1
        count = count + 1
    
    if(trueCount == 5):
      return True
    else:
      return False

  def convertPips(self, pipsArray):
    #Check for non-numerical pips
    if(any(not x.isalpha() for x in pipsArray)):

      #Change non-numerical elements into numbers 
      for i in range(len(pipsArray)):
        if (pipsArray[i].isalpha()):
          pipsArray[i] = self.assignNumericalValue(pipsArray[i])
      return pipsArray
    else:
      return pipsArray
  
  def assignNumericalValue(self, symbol):
    if(symbol == 'J'):
      return '11'
    elif(symbol == 'Q'):
      return '12'
    elif(symbol == 'K'):
      return '13'
    elif(symbol == 'A'):
      return '14'

  def createDeck(self):
    for suit in SUITS:
        for pip in PIPS:
            card = (suit,pip)
            deck.append(card)
  
  def dealHand(self):
    hand = []
    for i in range(2):
      card = random.choice(deck)
      deck.remove(card)
      hand.append(card)
    return hand

  def dealCards(self, numCards):
    communityCards = []
    for i in range(numCards):
      #pip, suit = takeCardFromDeck()
      card = random.choice(deck)
      deck.remove(card)
      communityCards.append(card)
    return communityCards
      

  def dealEntireDeck(self):
    for i in range(13):
        for j in range(4):
            #pip,suit = takeCardFromDeck()
            card = random.choice(deck)
            deck.remove(card)
            pip, suit = card
            print(suit + pip, end = " ")
        print()

#createDeck()
#dealEntireDeck()

