import gym_examples
import gym
import pandas as pd
import numpy as np
import time
import random
import warnings
warnings.filterwarnings("ignore")

#Symbols for cards
clubs = "\u2663"
hearts = "\u2665"
diamonds = "\u2666"
spades = "\u2660"

class player_sandbox:

    def __init__(self, env):
        self.current_player = 0
        self.env = env

    def print_menu(self):
        lines = [[] for i in range(10)]
        
        lines[0].append("\n                       " + clubs +" "+ hearts +" "+ diamonds +" "+ spades +" POKERBOT "+ clubs +" "+ hearts +" "+ diamonds +" "+ spades)
        lines[1].append(" ")
        lines[2].append("Choose an action:")
        lines[3].append("FOLD = 0")
        lines[4].append("CHECK = 1")
        lines[5].append("CALL = 2")
        lines[6].append("RAISE_HALF_POT = 3")
        lines[7].append("RAISE_POT = 4")
        lines[8].append("RAISE_2POT = 5")
        lines[9].append("ALL_IN = 6")

        result = []

        for index, line in enumerate(lines):
            result.append(''.join(lines[index]))

        for i in result:
            print(i)

    def print_starting_message(self):
        lines = [[] for i in range(6)]
        lines[0].append(" ")
        lines[1].append(" ")
        lines[2].append(" ")
        lines[3].append( clubs +" "+ hearts +" "+ diamonds +" "+ spades +" POKERBOT "+ clubs +" "+ hearts +" "+ diamonds +" "+ spades)
        lines[4].append("You are player 1. You make a small blind bid of £5 automatically.")
        lines[5].append(" ")
        result = []

        for index, line in enumerate(lines):
            result.append(''.join(lines[index]))

        for i in result:
            print(i)

    def make_blind_bet(self, is_dealer, player_num):
        env.set_dealer(is_dealer)
        env.set_player_num(player_num)
        if(player_num == 1):
            env.step(7) #Player1 makes a SB to start 
        elif(player_num == 2):
            env.step(8) #Player2 makes a BB 

    def make_move(self, action):
        env.set_dealer(True)
        env.set_player_num(1)
        env.step(action)
        env.render()

        #Then set player 2 
        env.set_dealer(False)
        env.set_player_num(2)


    def make_random_move(self):
        min_bet = env.bet_amount
        env.set_dealer(False)
        env.set_player_num(2)
        action = random.randint(0,6)

        #A bit of validation to make player 2 more reasonable
        if(action == 1):    #Player 2 will always go 2nd so checking doesn't make sense
            action += 1
        if(action == 3 and min_bet > (env.pot * 0.5)):
            action += 1
        if(action == 4 and min_bet > env.pot):
            action += 1
        if(action == 5 and min_bet > (env.pot * 2)):
            action += 1

        env.step(action) #Player1 makes a SB to start 
        env.render()

if __name__ == "__main__":
    #Create an instance of the HUNLTH environment
    env = gym.make('gym_examples/HUNLTH-v0')
    env.reset()
    global_sleep_time = 2

    #Initial start UI and information
    game_1 = player_sandbox(env)
    game_1.print_starting_message()
    time.sleep(global_sleep_time)
    game_1.make_blind_bet(True, 1)
    game_1.make_blind_bet(False, 2)
    env.render()

    #Main game action choices
    while(not(env.terminated) and env.stage < 5):
        time.sleep(global_sleep_time)
        game_1.print_menu()
        chosen_action = int(input("Enter number of action:"))
        time.sleep(global_sleep_time)
        game_1.make_move(chosen_action)
        time.sleep(global_sleep_time)
        game_1.make_random_move()
        time.sleep(global_sleep_time)



    