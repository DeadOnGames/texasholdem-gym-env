import gym_examples
import gym
import pandas as pd
import numpy as np
from datetime import datetime

class CFR:  
    def __init__(self, game, num_iterations):
        NUM_ACTIONS = self.get_num_actions(game)
        self.game = game
        #Initialise all regret values to zero
        self.regret_sum = np.zeros(NUM_ACTIONS)
        self.strategy = np.zeros(NUM_ACTIONS)
        self.strategy_sum = np.zeros(NUM_ACTIONS)
        self.num_iterations = num_iterations

    def get_strategy(self, realisation_weight):
        actions = self.get_available_actions()
        normalizingSum = 0
        for a in actions:
            self.strategy[a] = self.regret_sum[a] if self.regret_sum[a] > 0 else 0
            normalizingSum += self.strategy[a]

        for a in actions:
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS
            self.strategy_sum[a] += realisation_weight * self.strategy[a]
        return self.strategy
    
    def get_average_strategy(self, state, regrets):
        if regrets is None:
            return np.ones(len(self.game.actions(state))) / len(self.game.actions(state))
        else:
            avgStrategy = np.zeros(NUM_ACTIONS)
            normalizingSum = 0
            for a in range(NUM_ACTIONS):
                normalizingSum += self.strategy_sum[a]
            for a in range(NUM_ACTIONS):
                if (normalizingSum > 0):
                    avgStrategy[a] = round(self.strategy_sum[a] / normalizingSum, 2)
                else:
                    avgStrategy[a] = round(1.0 / NUM_ACTIONS)
            return avgStrategy

    def __str__(self):
        return self.infoSet + ": " + str(self.get_average_strategy())  # + "; regret = " + str(self.regret_sum)
    
    #Train texasholdem - repreat for a large number of iterations until the startegy converges to an equilibrium
    def train(self, iterations):
        startTime = datetime.now()
        #Call CFR method for each iteration
        for i in range(self.num_iterations):
                self.CFR(self.game.initial_state(), 1, 1)
        endTime = datetime.now()

    def get_available_actions(self, env):
        actions = []
        for e in env.action_space:
            actions.append(e.value)
        return actions
    
    def get_num_actions(self, env):
        #count = 0
        #for e in env.action_space:
        #    count += 1
        #return count

        #Hardcoded for time
        return 9


    # Counterfactual regret minimization iteration
    def CFR(self, state, p0, p1):
        # Return payoff for terminal states
        if self.game.terminated(state):
                return self.game.utility(state)
        player = self.game.player(state)

        player = self.game.player(state)
        if player == 1:
            #Update the player's strategy for each information set based on the regret values.
            strategy = self.get_strategy(state, self.regrets.get(state))
            action = np.random.choice(self.game.actions(state), p=strategy)
            next_state, reward = self.game.step(state, action)
            v = self.cfr(next_state, p0 * strategy[action], p1)
            
            for a in self.game.actions(state):
                if a == action:
                    self.regrets[state][a] += p1 * (v - reward) * strategy[a]
                else:
                    self.regrets[state][a] += p1 * v * strategy[a]
                    
            return v
        
        if player == 2:
            #Update the player's strategy for each information set based on the regret values.
            strategy = self.get_strategy(state, self.regrets.get(state))
            action = np.random.choice(self.game.actions(state), p=strategy)
            next_state, reward = self.game.step(state, action)
            v = self.cfr(next_state, p0, p1 * strategy[action])
            
            for a in self.game.actions(state):
                if a == action:
                    self.regrets[state][a] += p0 * (v - reward) * strategy[a]
                else:
                    self.regrets[state][a] += p0 * v * strategy[a]
                    
            return v

class texas_holdem:
    def __init__(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Start Time =", current_time)
        
        #Create an instance of the HUNLTH environment
        env = gym.make('gym_examples/HUNLTH-v0')
        env.reset()

        iterations = 5
        print("iterations =", iterations)
        cfr1 = CFR(env, iterations)    #Create an insatnce of CFR - player 1
        cfr2 = CFR(env, iterations)    #Create an insatnce of CFR - player 2

        relisation_weight = 0
        cfr1.get_strategy(realisation_weight)
        #train(iterations)

        env.set_dealer(True)
        env.step(7) #Make SB in prepreflop
        env.render()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("End Time =", current_time)

    
texasholdem_1 = texas_holdem()
