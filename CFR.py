import gym_examples
import gym
import pandas as pd
import numpy as np
from numpy.random import choice
from datetime import datetime

class CFR:  
    def __init__(self, env, num_iterations):
        self.NUM_ACTIONS = self.get_num_actions() #9
        self.possible_actions = np.arange(self.NUM_ACTIONS)
        self.env = env

        #Initialise all values to zero
        self.regret_sum = np.zeros(self.NUM_ACTIONS)
        self.strategy = np.zeros(self.NUM_ACTIONS)
        self.strategy_sum = np.zeros(self.NUM_ACTIONS)

        #Opponent's regret sum and strategy sum arrays
        self.p2_regret_sum = np.zeros(self.NUM_ACTIONS)
        self.p2_strategy_sum = np.zeros(self.NUM_ACTIONS)

        self.num_iterations = num_iterations
        self.util = {}

    def get_strategy(self, regret_sum):
        regret_sum[regret_sum < 0] = 0
        normalising_sum = sum(regret_sum)
        strategy = regret_sum
        for a in range(self.NUM_ACTIONS):
            if normalising_sum > 0:
                strategy[a] /= normalising_sum  #Will return a %
            else:
                strategy[a] = 1.0 / self.NUM_ACTIONS
        return strategy
    
    def get_average_strategy(self, strategy_sum):
        average_strategy = np.zeros(self.NUM_ACTIONS)
        normalising_sum = sum(strategy_sum)
        for a in range(self.NUM_ACTIONS):
            if normalising_sum > 0:
                average_strategy[a] = strategy_sum[a] / normalising_sum
            else:
                average_strategy[a] = 1.0 / self.NUM_ACTIONS
        return average_strategy


    def get_action(self, strategy):
        #Give the index of the action we want to take
        #p=strategy is the probability of strategy we want to use
        return choice(self.possible_actions, p=strategy) 

    def get_reward(self, p1_action, p2_action):
        #Return the action from the env
        #May need to chance whi mehtod bc p2_reward is also used
        return self.env.reward

    def __str__(self):
        return self.infoSet + ": " + str(self.get_average_strategy())  # + "; regret = " + str(self.regret_sum)
    
    def train(self, iterations):
    #Training is just iterating the CFR algorithm
        startTime = datetime.now()
        
        for i in range(iterations):
            strategy = self.get_strategy(self.regret_sum)
            p2_strategy = self.get_strategy(self.p2_regret_sum)
            self.strategy_sum += strategy
            self.p2_strategy_sum += p2_strategy
            #self.cfr(self.env.initial_state(), 1, 1)

            #Get an action we want to take
            p2_action = self.get_action(p2_strategy)
            p1_action = self.get_action(strategy)

            p1_reward = self.get_reward(p1_action, p2_action)
            p2_reward = self.get_reward(p2_action, p1_action)

            for a in range(self.NUM_ACTIONS):   #Loop through all actions
                #Calculate counterfactual reward
                p1_regret = self.get_reward(a, p2_action) - p1_reward
                p2_regret = self.get_reward(a, p1_action) -p2_reward
                self.regret_sum[a] += p1_regret
                self.p2_regret_sum[a] += p2_regret

        endTime = datetime.now()

    def get_available_actions(self, env):
        actions = []
        for e in env.action_space:
            actions.append(e.value)
        return actions
    
    def get_num_actions(self):
        #Hardcoded for time
        return 9

'''
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

'''
def main():
    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    #print("Start Time =", current_time)
    
    #Create an instance of the HUNLTH environment
    env = gym.make('gym_examples/HUNLTH-v0')
    env.reset()

    
    iterations = 5
    print("iterations =", iterations)
    cfr1 = CFR(env, iterations)    #Create an insatnce of CFR - player 1

    cfr1.train(iterations)

    target_policy = cfr1.get_average_strategy(cfr1.strategy_sum)
    p2_target_poliy = cfr1.get_average_strategy(cfr1.p2_strategy_sum)
    print('Target policy: %s' % (target_policy))

    #env.set_dealer(True)
    #env.step(7) #Make SB in prepreflop
    #env.render()

    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
    #print("End Time =", current_time)

    
if __name__ == "__main__":
    main()
