# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np

# 条件を探索する領域
domain = [{'name': 'time of stimulation', 'type': 'discrete', 'domain': (2,3,4,5,6,7,8)},
            {'name': 'frequency', 'type': 'continuous', 'domain': (0.5, 10)},
            {'name': 'voltage', 'type': 'continuous', 'domain': (0, 18)}]

data = np.loadtxt('./conditions.txt', delimiter= ",", skiprows=1)
conditions = data[:, 0:3]

# --- Define your problem
def f(x, data = data):
    for i in range(0,3):
        if np.array_equal(x, data[i][0:3]):
            return data[i][3]

# --- Solve your problem
myBopt = BayesianOptimization(f=f, domain=domain, X=conditions, batch_size=4, evaluator_type = 'local_penalization')
result = myBopt.suggest_next_locations()

print(f'{ result = }')