import numpy as np


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
        self.appear_times = 0
        self.total_trial = 0
        self.victoryRate = np.zeros(2, dtype=int)

    def insert(self, state):
        """
        judge whether the state has appeared, and insert a new state to the monte carlo tree.

        :param state: the state to be judged and inserted
        :return: a monte carlo tree node representing input state.
        """
        for i in self.Child:
            if (state == i.state).all():
                self.total_trial += 1
                i.appear_times += 1
                return i
        t = MonteCarloTree(state=state, child=[])
        t.father = self
        t.appear_times += 1
        t.total_trial = 0
        self.Child.append(t)
        return t

    def clear_appears(self):
        for i in self.Child:
            i.total_trial = 0
            i.appear_times = 0
            i.clear_appears()
