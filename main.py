import utils
import nuesslein1
import nuesslein2
import chancellor
import choi



V = 10
C = 40
formula = utils.create_formula(V, num_clauses=C, k=3)

print("The formula has ", V, " variables and ", C, " clauses.")

print("nuesslein_{n+m}: ", nuesslein2.nuesslein2(formula, V).solve())
print("nuesslein_{2n+m}: ", nuesslein1.nuesslein1(formula, V).solve())
print("chancellor_{n+m}: ", chancellor.chancellor(formula, V).solve())
print("choi_{3m}: ", choi.choi(formula, V).solve())
