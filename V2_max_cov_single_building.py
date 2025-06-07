"""
Model Version 2: Single Building Max Coverage

Code associated with paper:
    "Developing Optimization Models with Cognitive Systems Engineering"
    By Tyler C. O'Brien, Emily L. Tucker, Steven Foster, and Sudeep Hegde
    Journal of the Operational Research Society


Notes on use:
    - Replace "filename" with the appropriate path to the file where the data is stored
    - The code uses zero-based indexing, and the paper reports results in one-based indexing.
        - E.g., x[0] in the code means candidate location 1 in the paper.

"""
import pandas as pd
import numpy as np
import sys
from pyomo.environ import *


filename = # INSERT PATH #####################################3
df = pd.read_excel (filename, sheet_name='Data')

# Sets
C = ["Freeman078", "Freeman128", "Freeman138"]
J = list(df.index)


# Parameters
T = 8 # coverage time
p = 4 # stations to locate

a = df <= T # coverage indicator
a.replace({False: 0, True: 1}, inplace=True)


# Model
model = ConcreteModel(name = "V2_MaxCover")

# Decision Variables
model.x = Var(J, within=Binary) # candidate location selection
model.z = Var(C, within=Binary) # classroom coverage

# Objective Function

def obj_rule(model):
    return sum(model.z[c] for c in C)
model.obj = Objective(rule=obj_rule, sense = maximize)

# Constraints

def node_coverage_cons(model, c):
    return sum(a[c][j]*model.x[j] for j in J) >= model.z[c]
model.node_cons_Coverage = Constraint(C, rule=node_coverage_cons)


def dispenser_per_building(model):
    return sum(model.x[j] for j in J) == p
model.dispenser_per_building = Constraint(rule=dispenser_per_building)

# Solve
solver = SolverFactory('gurobi')
solver.solve(model)
model.pprint()
print("Obj value: " + str(value(model.obj)))
