from dwave_qbsolv import QBSolv
import numpy as np



# this function downloads a random k-SAT formula
def create_formula(num_vars, num_clauses, k):

    formula = []
    while len(formula) < num_clauses:
        vars = np.random.choice(range(1,num_vars+1), size=k, replace=False)
        signs = np.random.choice([-1,+1], size=k, replace=True)
        formula.append(vars * signs)

    return formula


# this function solves a given QUBO-Matrix Q with Qbsolv
def solve_with_qbsolv(Q):
    response = QBSolv().sample_qubo(Q, num_repeats=1000)
    return response.samples()[0]


# this function calculates the value of a solution for a given QUBO-Matrix Q
def getValue(Q, solution):
    ones = [x for x in solution.keys() if solution[x] == 1]
    value = 0
    for x in ones:
        for y in ones:
            if (x,y) in Q.keys():
                value += Q[(x,y)]
    return value


# this function prints the first n row/columns of a QUBO-Matrix Q
def printQUBO(Q, n):
    for row in range(n):
        for column in range(n):
            if row > column:
                print("      ", end = '')
                continue
            printing = ""
            if (row,column) in Q.keys() and Q[(row,column)] != 0:
                printing = str(Q[(row,column)])
            printing += "_____"
            printing = printing[:5]
            printing += " "
            print(printing, end = '')
        print("")


# this function checks, whether a given assignment satisfies a given SAT-formula
def check_solution(formula, assignment):
    n = 0
    for c in formula:
        for l in c:
            if l < 0 and assignment[abs(l)-1] == 0:
                n += 1
                break
            elif l > 0 and assignment[abs(l)-1] == 1:
                n += 1
                break
    return n


def get_n_couplings(Q):
    n = 0
    for k in Q.keys():
        if Q[k] != 0:
            n += 1
    return n
