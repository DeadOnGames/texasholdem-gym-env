import gym_examples
import gym
import pandas as pd
import numpy as np

class UI_sandbox():

    #Simulate the dealing of a hand with rendering 

    #Create an instance of the HUNLTH environment
    env = gym.make('gym_examples/HUNLTH-v0')
    env.reset()

    #-----------Prepreflop-------
    env.render()
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(7) #Player1 makes a SB to start 

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(8) #Player2 makes a BB 
    env.render()

    #-----------Flop-------------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
    env.render()

    #-----------Turn-------------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
    env.render()

    #-----------River-------------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
    env.render()

    #-----------Showdown-------------
    env.set_dealer(True)
    env.set_player_num(1)
    env.step(4) #Player1 raises by pot

    env.set_dealer(False)
    env.set_player_num(2)
    env.step(2) #Player2 calls
    env.render()
