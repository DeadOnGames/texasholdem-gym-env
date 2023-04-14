from random import shuffle
import numpy as np
from datetime import datetime

class Kuhn_cfr:

    def __init__(self):
        self.node_map = {}
        self.expected_game_value = 0
        self.num_cards = 3
        self.nash_equilibrium = dict()
        self.current_player = 0
        self.deck = np.array([0,1,2])
        self.num_actions = 2

    def train(self, num_iterations):
        expected_game_value = 0
        for _ in range(num_iterations):
            shuffle(self.deck)
            expected_game_value += self.cfr('', 1, 1)
            for _, v in self.node_map.items():
                v.update_strategy()

        expected_game_value /= num_iterations
        display_results(expected_game_value, self.node_map)

    def cfr(self, history, pr_1, pr_2): #Recursive function
        n = len(history)
        is_player_1 = n % 2 == 0
        player_card = self.deck[0] if is_player_1 else self.deck[1]

        if self.is_terminal(history):
            card_player = self.deck[0] if is_player_1 else self.deck[1]
            card_opponent = self.deck[1] if is_player_1 else self.deck[0]
            reward = self.get_reward(history, card_player, card_opponent)
            return reward

        node = self.get_node(player_card, history)
        strategy = node.strategy

        # Counterfactual utility per action.
        action_utils = np.zeros(self.num_actions)

        for act in range(self.num_actions):
            next_history = history + node.action_dict[act]
            if is_player_1:
                #Multiplied by -1 bc if Player 1 gets a reward of 1, Player 2 will get -1
                action_utils[act] = -1 * self.cfr(next_history, pr_1 * strategy[act], pr_2)
            else:
                action_utils[act] = -1 * self.cfr(next_history, pr_1, pr_2 * strategy[act])

        # Utility of information set.
        util = sum(action_utils * strategy)
        regrets = action_utils - util
        #Update reach prob and regrrt sum
        if is_player_1:
            node.reach_pr += pr_1
            node.regret_sum += pr_2 * regrets
        else:
            node.reach_pr += pr_2
            node.regret_sum += pr_1 * regrets

        return util

    @staticmethod
    def is_terminal(history):   #For calculating rewards for terminal nodes
        if history[-2:] == 'pp' or history[-2:] == "bb" or history[-2:] == 'bp':
            return True

    @staticmethod
    def get_reward(history, player_card, opponent_card):    #Determine reward from showdown
        terminal_pass = history[-1] == 'p'
        double_bet = history[-2:] == "bb"
        if terminal_pass:
            if history[-2:] == 'pp':
                return 1 if player_card > opponent_card else -1
            else:
                return 1
        elif double_bet:
            return 2 if player_card > opponent_card else -2

    def get_node(self, card, history):
        key = str(card) + " " + history
        if key not in self.node_map:
            action_dict = {0: 'p', 1: 'b'}
            info_set = Node(key, action_dict)
            self.node_map[key] = info_set
            return info_set
        return self.node_map[key]  
    #def play(self):
    #    print('You are player x')
    #   print()

class Node:
    def __init__(self, key, action_dict, num_actions=2):
        self.key = key
        self.num_actions = num_actions
        self.regret_sum = np.zeros(self.num_actions)
        self.strategy_sum = np.zeros(self.num_actions)
        self.action_dict = action_dict
        self.strategy = np.repeat(1/self.num_actions, self.num_actions)
        self.reach_pr = 0   #Probability of reaching this node in the game tree
        self.reach_pr_sum = 0

    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.reach_pr_sum += self.reach_pr
        self.strategy = self.get_strategy()
        self.reach_pr = 0   

    def get_strategy(self):
        regrets = self.regret_sum
        regrets[regrets < 0] = 0
        normalizing_sum = sum(regrets)
        if normalizing_sum > 0:
            return regrets / normalizing_sum
        else:
            return np.repeat(1/self.num_actions, self.num_actions)

    def get_average_strategy(self):
        strategy = self.strategy_sum / self.reach_pr_sum
        # Re-normalize
        total = sum(strategy)
        strategy /= total
        return strategy

    def __str__(self):
        strategies = ['{:03.2f}'.format(x)
                      for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies)


def display_results(expected_value, i_map):
    print('player 1 expected value (Nash Equilibrium): {}'.format(expected_value))
    print('player 2 expected value (Nash Equilibrium): {}'.format(-1 * expected_value))

    print()
    print('Player 1 strategies:')
    sorted_items = sorted(i_map.items(), key=lambda x: x[0])
    for _, v in filter(lambda x: len(x[0]) % 2 == 0, sorted_items):
        print(v)
    print()
    print('Player 2 strategies:')
    for _, v in filter(lambda x: len(x[0]) % 2 == 1, sorted_items):
        print(v)



if __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")[:-3]
    print("Start Time =", current_time)

    num_iterations=50000
    kuhn1 = Kuhn_cfr()
    kuhn1.train(num_iterations)
    print("Number of iterations:" + str(num_iterations))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")[:-3]
    print("End Time =", current_time)
