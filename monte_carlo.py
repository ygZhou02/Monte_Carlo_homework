# -*- coding: utf-8 -*-
"""
Editor: zhou yuguang
Email Address: bjygzhou@126.com

This is an implementation of monte carlo tree search on TicTacToe game.
"""

import numpy as np


class TicTacToe:
    """
    class TicTacToe, initialize a grid and a round counter.
    """
    def __init__(self, round_num):
        super().__init__()
        self.grid = np.zeros((3, 3), dtype=int)
        self.round_num = round_num

    def judge(self):
        """
        judge whether the game ends and which player wins the game.

        :return: ending information: [0]-not end, [1]-player 1 wins, [-1]-player -1 wins, [2]-draw.
        """
        for i in range(3):
            Player = self.grid[i][0]
            if Player != 0 and self.grid[i][1] == Player and self.grid[i][2] == Player:
                return Player

        for i in range(3):
            Player = self.grid[0][i]
            if Player != 0 and self.grid[1][i] == Player and self.grid[2][i] == Player:
                return Player

        Player = self.grid[0][0]
        if Player != 0 and self.grid[1][1] == Player and self.grid[2][2] == Player:
            return Player

        Player = self.grid[2][0]
        if Player != 0 and self.grid[1][1] == Player and self.grid[0][2] == Player:
            return Player

        if (self.grid != 0).all():
            return 2

        return 0

    def take_turn(self, p, x_axis, y_axis):
        self.grid[x_axis][y_axis] = p
        self.round_num += 1
        return

    def possible_state(self):
        possible_list = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    possible_list.append((i, j))

        return possible_list

    def epsilon_greedy(self, tree, player_, epsilon=0.3):
        """
        choose an action by epsilon greedy policy.

        :param tree: monte carlo tree node, which contains winning rate information
        :param player_: which player takes turn
        :param epsilon: epsilon-greedy policy parameter
        :return: the chosen action
        """
        possibility = np.random.uniform(0, 1)
        state_list = self.possible_state()
        if possibility > epsilon:               # choose acition according to greedy winning rate
            pred_state = np.copy(tree.state)
            vic = np.zeros(len(state_list))
            index = 0
            for action_ in state_list:          # count winning rate of each action
                pred_state[action_[0]][action_[1]] = player_
                for item in tree.Child:
                    if (pred_state == item.state).all() and item.victoryRate[1] != 0:
                        vic[index] = float(item.victoryRate[0]) / float(item.victoryRate[1])
                pred_state[action_[0]][action_[1]] = 0
                index += 1
            if player_ == 1:
                index = np.argmax(vic)
            else:
                index = np.argmin(vic)          # player -1 should minimize player 1's winning rate
            Action = state_list[index]
        else:                                   # a random action
            index = np.random.randint(0, len(state_list))
            Action = state_list[index]
        return Action


class MonteCarloTree:
    """
    Monte carlo tree class. each node has a list of child,
    a father, a state representing, and a winning rate.
    """
    def __init__(self, father=None, child=[], state=np.zeros((3, 3), dtype=int)):
        super().__init__()
        self.Child = child
        self.father = father
        self.state = state
        self.victoryRate = np.zeros(2, dtype=int)

    def insert(self, state):
        """
        judge whether the state has appeared, and insert a new state to the monte carlo tree.

        :param state: the state to be judged and inserted
        :return: a monte carlo tree node representing input state.
        """
        for i in self.Child:
            if (state == i.state).all():
                return i
        t = MonteCarloTree(state=state, child=[])
        t.father = self
        self.Child.append(t)
        return t


def MonteCarlo(input_state, player, depth=1000, round_num=0, e=0.3):
    """
    implement monte carlo tree search, in order to find the best choice for a given game.

    :param input_state: the origin of tree search.
    :param player: the game is at which player's turn.
    :param depth: how many episodes the monte carlo search take.
    :param round_num: which round the game is at.
    :param e: epsilon-greedy policy parameter.
    :return: best choice to drop a piece.
    """

    episode_num = depth                         # total episode
    game = TicTacToe(round_num=round_num)       # initialize a game
    if player == -1:
        input_state = - input_state             # convert the chess board
    root = MonteCarloTree()                     # initialize a monte carlo tree
    root.Child = []                             # clear root.Child
    root.state = np.copy(input_state)           # initialize origin state
    game.grid = np.copy(input_state)            # initialize origin state
    for episode in range(episode_num):
        player = 1
        game.grid = np.copy(input_state)        # initialize origin state
        game.round_num = round_num
        now_node = root
        while game.judge() == 0:
            # choose an action according to epsilon-greedy policy
            action = game.epsilon_greedy(tree=now_node, player_=player, epsilon=e)
            # game forward
            game.take_turn(player, action[0], action[1])
            # get the new game state
            new_state = np.copy(game.grid)
            # if a brand new state appears, add it to monte carlo tree
            new_node = now_node.insert(new_state)
            # player interchange
            player = player * (-1)
            now_node = new_node
        ret = game.judge()                      # get the game result
        element = now_node
        while element:                          # monte carlo tree retrieval
            if ret == 1:                        # player wins the game
                element.victoryRate[0] += 2     # get a 2/2 increase
            elif ret == 2:                      # game draw
                element.victoryRate[0] += + 1   # get a 1/2 reward
            element.victoryRate[1] += 2         # if player loses the game, get a 0/2 decrease
            element = element.father            # retrieve

    vic_list = np.zeros(len(root.Child))
    for i in range(len(root.Child)):            # count winning percentage
        if root.Child[i].victoryRate[1] != 0:   # avoid dividing zero
            print("son", i, root.Child[i].state)
            vicRate = float(root.Child[i].victoryRate[0]) / float(root.Child[i].victoryRate[1])
            print("confidence:\n", vicRate)
            vic_list[i] = vicRate
    index = np.argmax(vic_list)                 # choose the action with highest winning percentage
    print("vic list", vic_list)
    pred_state = root.Child[index].state
    print("chosen state:", pred_state)
    print("origin state:", input_state)
    ans = np.where(pred_state != input_state)   # extract action information
    return ans


def main():
    monte_carlo_depth = 3000        # monte carlo search total episode
    epsilon = 0.7                   # epsilon-greedy policy

    print("game start")
    game = TicTacToe(round_num=0)   # start a TicTacToe game
    playerid = 1                    # two player, 1 and -1
    while game.judge() == 0:        # game is not over
        print("round", game.round_num, "start!")
        game_state = np.copy(game.grid)
        # player chooses action according to monte carlo search
        player_action = MonteCarlo(input_state=game_state, player=playerid,
                                   depth=monte_carlo_depth, round_num=game.round_num, e=epsilon)
        print("player", playerid, "'s action:", player_action)
        # place a piece
        game.take_turn(playerid, player_action[0][0], player_action[1][0])
        # show how game goes
        print(game.grid)
        # chance exchange
        playerid *= (-1)
    print(game.judge(), "WINS!")    # if nobody wins, game.judge() will return 0. otherwise 1 or -1 wins the game.


if __name__ == "__main__":
    main()
