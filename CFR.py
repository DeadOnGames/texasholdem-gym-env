import gym_examples
import gym
import pandas as pd
import numpy as np
from datetime import datetime

class CFR:  
    def __init__(self, env, num_iterations):
        self.NUM_ACTIONS = self.get_num_actions()
        self.env = env

        #Initialise all values to zero
        self.regret_sum = np.zeros(self.NUM_ACTIONS)
        self.strategy = np.zeros(self.NUM_ACTIONS)
        self.strategy_sum = np.zeros(self.NUM_ACTIONS)
        self.num_iterations = num_iterations
        self.util = {}

    def get_strategy(self, state, p0, num_actions):
        if state in self.strategy:
            strategy = self.strategy[state]
            return strategy
        elif state in self.regrets:
            regrets = self.regrets[state]
            normalizing_sum = sum([r if r > 0 else 0 for r in regrets])
            if normalizing_sum > 0:
                strategy = np.array([r/normalizing_sum for r in regrets])
                self.strategy[state] = strategy
                return strategy
            else:
                strategy = np.ones(num_actions) / num_actions
                self.strategy[state] = strategy
                return strategy
        else:
            strategy = np.ones(num_actions) / num_actions
            self.strategy[state] = strategy
            return strategy

    def __str__(self):
        return self.infoSet + ": " + str(self.get_average_strategy())  # + "; regret = " + str(self.regret_sum)
    
    #Train texasholdem - repreat for a large number of iterations until the startegy converges to an equilibrium
    def train(self, iterations):
        startTime = datetime.now()
        #Call CFR method for each iteration
        for i in range(self.num_iterations):
                self.cfr(self.env.initial_state(), 1, 1)
        endTime = datetime.now()

    def get_available_actions(self, env):
        actions = []
        for e in env.action_space:
            actions.append(e.value)
        return actions
    
    def get_num_actions(self):
        #Hardcoded for time
        return 9


    # Counterfactual regret minimization iteration
    def cfr(self, state, p0, p1):
        # Return payoff for terminal states
        if self.is_terminal(state):
                return self.get_utility(state, 0) #Player 0
        
        #For each action, recursively call CFR with probabilities

        if env.player_num == 1:
            return self.cfr_chance(state, p0, p1)
        elif player == 2:
            return self.cfr_player(state, p0, p1)

    def cfr_chance(self, state, p0, p1):
        actions = self.get_actions(state)
        num_actions = self.get_num_actions()
        strategy = self.get_strategy(state, p0, num_actions)
        util = np.zeros(num_actions)
        node_util = 0

        for i in range(num_actions):
            next_state = self.get_next_state(state, actions[i])
            util[i] = self.cfr(next_state, p0 * strategy[i], p1)
            node_util += strategy[i] * util[i]
            
        for i in range(num_actions):
            regret = util[i] - node_util
            if state in self.regrets:
                self.regrets[state][i] += p1 * regret
            else:
                self.regrets[state] = np.zeros(num_actions)
                self.regrets[state][i] += p1 * regret
                
        return node_util

    def cfr_player(self, state, p0, p1):
        actions = self.get_actions(state)
        num_actions = len(actions)
        strategy = self.get_strategy(state, p0, num_actions)
        util = np.zeros(num_actions)
        
        for i in range(num_actions):
            next_state = self.get_next_state(state, actions[i])
            util[i] = self.cfr(next_state, p0, p1 * strategy[i])
            
        node_util = np.dot(strategy, util)
        for i in range(num_actions):
            regret = util[i] - node_util
            if state in self.regrets:
                self.regrets[state][i] += p1 * regret
            else:
                self.regrets[state] = np.zeros(num_actions)
                self.regrets[state][i] += p1 * regret
                
        return node_util

    def get_utility(self, state, player):
        if state in self.util:  
            return self.util[state][player]
        elif self.is_terminal(state):
            if self.get_winner(state) == player:
                return self


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

        cfr1.train(iterations)

        env.set_dealer(True)
        env.step(7) #Make SB in prepreflop
        env.render()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("End Time =", current_time)

    
texasholdem_1 = texas_holdem()
