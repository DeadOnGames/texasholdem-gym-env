import gym_examples
import gym
import pandas as pd
import numpy as np
from datetime import datetime

NUM_ACTIONS = 9

class CFR(self, game, num_iterations):  
    def __init__(self):
        self.game = game
        #Initialise all regret values to zero
        self.regretSum = np.zeros(NUM_ACTIONS)
        self.strategy = np.zeros(NUM_ACTIONS)
        self.strategySum = np.zeros(NUM_ACTIONS)
        self.num_iterations = num_iterations

    def get_strategy(self, realisationWeight):
        actions = get_available_actions()
        normalizingSum = 0
        for a in actions:
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizingSum += self.strategy[a]

        for a in actions:
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS
            self.strategySum[a] += realisationWeight * self.strategy[a]
        return self.strategy
    
    def get_average_strategy(self, state, regrets):
        if regrets is None:
            return np.ones(len(self.game.actions(state))) / len(self.game.actions(state))
        else:
            avgStrategy = np.zeros(NUM_ACTIONS)
            normalizingSum = 0
            for a in range(NUM_ACTIONS):
                normalizingSum += self.strategySum[a]
            for a in range(NUM_ACTIONS):
                if (normalizingSum > 0):
                    avgStrategy[a] = round(self.strategySum[a] / normalizingSum, 2)
                else:
                    avgStrategy[a] = round(1.0 / NUM_ACTIONS)
            return avgStrategy

    def __str__(self):
        return self.infoSet + ": " + str(self.get_average_strategy())  # + "; regret = " + str(self.regretSum)
    
    #Train texasholdem - repreat for a large number of iterations until the startegy converges to an equilibrium
    def train(self, iterations):
        startTime = datetime.now()
        #Call CFR method for each iteration
        for i in range(self.num_iterations):
                self.CFR(self.game.initial_state(), 1, 1)
        endTime = datetime.now()

    def get_avaiable_actions(self):
        #Get available actions 
        for e in env.actions:
            return e.value 


    # Counterfactual regret minimization iteration
    def CFR(self, state, player_1, player_2):

        if self.game.is_terminal(state):
                return self.game.utility(state)
        player = self.game.player(state)

        player = self.game.player(state)
        if player == 1:
            #Update the player's strategy for each information set based on the regret values.
            strategy = self.get_strategy(state, self.regrets.get(state))
            action = np.random.choice(self.game.actions(state), p=strategy)
            next_state, reward = self.game.step(state, action)
            v = self.cfr(next_state, player_1 * strategy[action], player_2)
            
            for a in self.game.actions(state):
                if a == action:
                    self.regrets[state][a] += player_2 * (v - reward) * strategy[a]
                else:
                    self.regrets[state][a] += player_2 * v * strategy[a]
                    
            return v
        
        if player == 2:
            #Update the player's strategy for each information set based on the regret values.
            strategy = self.get_strategy(state, self.regrets.get(state))
            action = np.random.choice(self.game.actions(state), p=strategy)
            next_state, reward = self.game.step(state, action)
            v = self.cfr(next_state, player_1, player_2 * strategy[action])
            
            for a in self.game.actions(state):
                if a == action:
                    self.regrets[state][a] += player_1 * (v - reward) * strategy[a]
                else:
                    self.regrets[state][a] += player_1 * v * strategy[a]
                    
            return v

class texas_holdem(self):
    def __init__(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Start Time =", current_time)

        iterations = 5

        print("iterations =", iterations)

        train(iterations)

        #Create an instance of the HUNLTH environment
        env = gym.make('gym_examples/HUNLTH-v0')
        env.reset()
        env.set_dealer(True)
        env.step(7) #Make SB in prepreflop
        env.render()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("End Time =", current_time)

    
