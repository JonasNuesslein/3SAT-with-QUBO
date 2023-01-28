import utils



class nuesslein1:

    def __init__(self, formula, V):
        # sort the formula (i.e. all negative literals are at the back of the clause)
        self.formula = [sorted(c, reverse=True) for c in formula]
        self.L = []
        for i in range(V):
            self.L.append(i+1)
            self.L.append(-(i+1))
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

    def R1(self, x):
        n = 0
        for c in self.formula:
            if x in c:
                n += 1
        return n

    def R2(self, x, y):
        n = 0
        for c in self.formula:
            if x in c and y in c:
                n += 1
        return n

    # this function creates the QUBO-Matrix Q
    def fillQ(self):
        for i in range(2*self.V + len(self.formula)):
            for j in range(2*self.V + len(self.formula)):
                if i > j:
                    continue
                if i == j and j < 2*self.V:
                    self.add(i, j, -self.R1(self.L[i]))
                elif i == j and j >= 2*self.V:
                    self.add(i, j, 2)
                elif j < 2*self.V and j-i == 1 and i%2 == 0:
                    self.add(i, j, len(self.formula)+1)
                elif i < 2*self.V and j < 2*self.V:
                    self.add(i, j, self.R2(self.L[i], self.L[j]))
                elif j >= 2*self.V and i < 2*self.V and self.L[i] in self.formula[j-2*self.V]:
                    self.add(i, j, -1)

    # this function starts creating Q, solving it and interpreting the solution
    # (e.g. deciding whether the formula is satisfiable or not)
    def solve(self):
        self.fillQ()
        answer = utils.solve_with_qbsolv(self.Q)
        assignment = [answer[2*i] for i in range(self.V)]
        return utils.check_solution(self.formula, assignment)


