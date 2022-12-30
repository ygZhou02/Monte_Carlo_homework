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
        if possibility > epsilon:  # choose acition according to greedy winning rate
            pred_state = np.copy(tree.state)
            vic = np.zeros(len(state_list))
            exp = np.zeros(len(state_list))
            index = 0
            for action_ in state_list:  # count winning rate of each action
                pred_state[action_[0]][action_[1]] = player_
                for item in tree.Child:
                    if (pred_state == item.state).all() and item.victoryRate[1] != 0 and tree.total_trial != 0:
                        vic[index] = float(item.victoryRate[0]) / float(item.victoryRate[1])
                        exp[index] = np.sqrt(np.log(tree.total_trial) / item.appear_times)
                pred_state[action_[0]][action_[1]] = 0
                index += 1
            # implement confidence limit algorithm
            C = 1
            vic += C * exp
            if player_ == 1:
                index = np.argmax(vic)
            else:
                index = np.argmin(vic)  # player -1 should minimize player 1's winning rate
            Action = state_list[index]
        else:  # a random action
            index = np.random.randint(0, len(state_list))
            Action = state_list[index]
        return Action
