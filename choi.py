import utils



class choi:

    def __init__(self, formula, V):
        # sort the formula (i.e. all negative literals are at the back of the clause)
        self.L = []
        self.formula = formula
        for c in formula:
            self.L.extend(c)
        self.V = V
        self.Q = {}

    # new values are added to the QUBO-Matrix Q via this monitor
    def add(self, x, y, value):
        if x > y:
            x,y = y,x
        if (x,y) in self.Q.keys():
            self.Q[(x,y)] += value
        else:
            self.Q[(x,y)] = value

    # this function creates the QUBO-Matrix Q
    # Explanations can be found in the paper
    def fillQ(self):
        for i in range(len(self.L)):
            for j in range(len(self.L)):
                if i > j:
                    continue
                if i == j:
                    self.add(i, j, -1)
                elif j - i <= 2 and j//3 == i//3:
                    self.add(i, j, 3)
                elif abs(self.L[i]) == abs(self.L[j]) and self.L[i] != self.L[j]:
                    self.add(i, j, 3)

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether the formula is satisfiable or not)
    def solve(self):
        self.fillQ()
        answer = utils.solve_with_qbsolv(self.Q)
        assignment = [0 for _ in range(self.V)]
        for i in range(len(self.L)):
            if answer[i] == 1:
                if self.L[i] < 0:
                    assignment[abs(self.L[i])-1] = 0
                else:
                    assignment[abs(self.L[i])-1] = 1
        return utils.check_solution(self.formula, assignment)



