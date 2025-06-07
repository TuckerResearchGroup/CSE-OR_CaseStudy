"""
Model Version 3: Target Coverage

Code associated with paper:
    "Developing Optimization Models with Cognitive Systems Engineering"
    By Tyler C. O'Brien, Emily L. Tucker, Steven Foster, and Sudeep Hegde
    Journal of the Operational Research Society


"""
from pyomo.environ import *
import pandas as pd
import numpy as np
import sys

# Model 
model = ConcreteModel(name = "V3_TargetCoverage")

# Set
model.B = Set(initialize=[0, 1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35]) 
    # Indices are associated with the following bulidings: ["Academic Success Center", "Administrative Services Building", "Barre Hall",	"Biosystems Research Complex",	"Brackett Hall",	"Brooks Center for Performing Arts",	"Campbell Museum of Natural History",	"College of Business",	"Cook Engineering Laboratory" ,	"Dillard Building" ,	"Earle Hall",	"Edwards Hall",	"Fluor Daniel Engineering Innovation Building",	"Freeman Hall",	"Godfrey Hall",	"Hardin Hall",	"Harris A. Smith Building",	"Holtzendorff Hall",	"Hunter Chemistry Laboratory",	"Jordan Hall",	"Kinard Laboratory of Physics",	"Lee Hall (Includes all 3 Buildings - 1, 2 ,3)",	"Long Hall",	"Lowry Hall",	"Martin Hall (Includes 3 sections - E, M, O)",	"McAdams Hall",	"Old Main", "Olin Hall", Poole Agricultural Center",	"Rhodes Engineering Center",	"Robert Muldrow Cooper Library",	"Sikes Hall",	"Sirrine Hall",	"Strode Tower",	"Vickery Hall",	"Watt Family Innovation Center"])

# Parameters

# Demand (February 2021)
d = [1047,	726,	1833,	4272,	3913,	3794,	49,	14335,	402,	781,	1538,	3608,	1946,	3194,	1926,	1332,	450,	2174,	2065,	1823,	1676,	3632,	1678,	1943,	2729,	2034,      4035,	436,	3357,	2709,	8428,	2436,	4177,	1317,	1682,	7444]


N = 102 # available dispensers
u = 500 # available uses

# Decision Variables
model.x = Var(model.B, within=NonNegativeIntegers)

# Constraints
def Allocate_At_Least_One_Cons(model, b):
    return model.x[b] >= 1 
model.con_Allocate_At_Least_One_Cons = Constraint(model.B, rule=Allocate_At_Least_One_Cons)


def Total_Disp_Supply_Cons(model):
    return sum(model.x[b] for b in model.B) <= N
model.Total_Disp_Supply_Cons = Constraint(rule=Total_Disp_Supply_Cons)

# Objective Function
def obj_rule(model):
    return sum((d[b]-u*model.x[b])**2 for b in model.B)
model.obj = Objective(rule=obj_rule, sense = minimize)


# Solve
solver = SolverFactory('gurobi')
solver.solve(model)
model.pprint()
print("Obj value: " + str(value(model.obj)))
