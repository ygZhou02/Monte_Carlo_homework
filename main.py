# -*- coding: utf-8 -*-
"""
Editor: zhou yuguang
Email Address: bjygzhou@126.com

This is an implementation of monte carlo tree search on TicTacToe game.
"""

import numpy as np
import time
from monte_carlo_tree import MonteCarloTree
from TicTacToe import TicTacToe
from visualization import visualization


def MonteCarlo(input_state, player, depth=1000, round_num=0, e=0.0):
    """
    implement monte carlo tree search, in order to find the best choice for a given game.

    :param input_state: the origin of tree search.
    :param player: the game is at which player's turn.
    :param depth: how many episodes the monte carlo search take.
    :param round_num: which round the game is at.
    :param e: epsilon-greedy policy parameter.
    :return: best choice to drop a piece.
    """

    episode_num = depth  # total episode
    game = TicTacToe(round_num=round_num)  # initialize a game
    if player == -1:
        input_state = - input_state  # convert the chess board
    root = MonteCarloTree()  # initialize a monte carlo tree
    root.Child = []  # clear root.Child
    root.state = np.copy(input_state)  # initialize origin state
    game.grid = np.copy(input_state)  # initialize origin state
    root.clear_appears()
    for episode in range(episode_num):
        player = 1
        game.grid = np.copy(input_state)  # initialize origin state
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
        ret = game.judge()  # get the game result
        element = now_node
        while element:  # monte carlo tree retrieval
            if ret == 1:  # player wins the game
                element.victoryRate[0] += 2  # get a 2/2 increase
            elif ret == 2:  # game draw
                element.victoryRate[0] += + 1  # get a 1/2 reward
            element.victoryRate[1] += 2  # if player loses the game, get a 0/2 decrease
            element = element.father  # retrieve

    vic_list = np.zeros(len(root.Child))
    for i in range(len(root.Child)):  # count winning percentage
        if root.Child[i].victoryRate[1] != 0:  # avoid dividing zero
            print("son", i, root.Child[i].state)
            vicRate = float(root.Child[i].victoryRate[0]) / float(root.Child[i].victoryRate[1])
            print("confidence:\n", vicRate)
            vic_list[i] = vicRate
    index = np.argmax(vic_list)  # choose the action with highest winning percentage
    print("vic list", vic_list)
    pred_state = root.Child[index].state
    print("chosen state:", pred_state)
    print("origin state:", input_state)
    ans = np.where(pred_state != input_state)  # extract action information
    return ans


def main():
    monte_carlo_depth = 3000  # monte carlo search total episode
    epsilon = 0.6  # epsilon-greedy policy

    print("game start")
    game = TicTacToe(round_num=0)  # start a TicTacToe game
    playerid = 1  # two player, 1 and -1
    while game.judge() == 0:  # game is not over
        print("round", game.round_num, "start!")
        game_state = np.copy(game.grid)
        # initialize pygame
        play_board = visualization()
        # player chooses action according to monte carlo search
        player_action = MonteCarlo(input_state=game_state, player=playerid,
                                   depth=monte_carlo_depth, round_num=game.round_num, e=epsilon)
        print("player", playerid, "'s action:", player_action)
        # place a piece
        game.take_turn(playerid, player_action[0][0], player_action[1][0])
        # show how game goes
        print(game.grid)
        # visualize the game in pygame
        play_board.drawGame(game.grid)
        time.sleep(1)
        # chance exchange
        playerid *= (-1)
    print(game.judge(), "WINS!")  # if nobody wins, game.judge() will return 0. otherwise 1 or -1 wins the game.
    play_board.waitForClose()


if __name__ == "__main__":
    main()
