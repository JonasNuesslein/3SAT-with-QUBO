import utils
import numpy as np



class nuesslein2:

    def __init__(self, formula, V):
        # sort the formula (i.e. all negative literals are at the back of the clause)
        self.formula = [sorted(c, reverse=True) for c in formula]
        self.V = V
        self.Q = {}

    # new values are added to the QUBO-Matrix Q via this monitor
    def add(self, x, y, value):
        x = np.abs(x) - 1
        y = np.abs(y) - 1
        if x > y:
            x,y = y,x
        if (x,y) in self.Q.keys():
            self.Q[(x,y)] += value
        else:
            self.Q[(x,y)] = value

    # this function creates the QUBO-Matrix Q
    def fillQ(self):
        for i, c in enumerate(self.formula):
            if list(np.sign(c)) == [1, 1, 1]:
                self.add(c[0], c[1], 2)
                self.add(c[0], self.V + i + 1, -2)
                self.add(c[1], self.V + i + 1, -2)
                self.add(c[2], c[2], -1)
                self.add(c[2], self.V + i + 1, 1)
                self.add(self.V + i + 1, self.V + i + 1, 1)
            elif list(np.sign(c)) == [1, 1, -1]:
                self.add(c[0], c[1], 2)
                self.add(c[0], self.V + i + 1, -2)
                self.add(c[1], self.V + i + 1, -2)
                self.add(c[2], c[2], 1)
                self.add(c[2], self.V + i + 1, -1)
                self.add(self.V + i + 1, self.V + i + 1, 2)
            elif list(np.sign(c)) == [1, -1, -1]:
                self.add(c[0], c[0], 2)
                self.add(c[0], c[1], -2)
                self.add(c[0], self.V + i + 1, -2)
                self.add(c[1], self.V + i + 1, 2)
                self.add(c[2], c[2], 1)
                self.add(c[2], self.V + i + 1, -1)
            else:
                self.add(c[0], c[0], -1)
                self.add(c[0], c[1], 1)
                self.add(c[0], c[2], 1)
                self.add(c[0], self.V + i + 1, 1)
                self.add(c[1], c[1], -1)
                self.add(c[1], c[2], 1)
                self.add(c[1], self.V + i + 1, 1)
                self.add(c[2], c[2], -1)
                self.add(c[2], self.V + i + 1, 1)
                self.add(self.V + i + 1, self.V + i + 1, -1)

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether the formula is satisfiable or not)
    def solve(self):
        self.fillQ()
        answer = utils.solve_with_qbsolv(self.Q)
        assignment = [answer[i] for i in range(self.V)]
        return utils.check_solution(self.formula, assignment)



