# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np
from numpy.random import seed

# 条件を探索する領域
domain = [{'name': 'time of stimulation', 'type': 'discrete', 'domain': (0,1,2,3,4,5,6)},
            {'name': 'frequency', 'type': 'continuous', 'domain': (0.5, 10)},
            {'name': 'voltage', 'type': 'continuous', 'domain': (0, 18)}]

# condtions.txtのファイルから実験条件と結果の組み合わせを取ってくる。
data = np.loadtxt('./conditions.csv', delimiter= ",", skiprows=1)
conditions = data[:, 0:3] # 末列以外の部分で実験条件の設定を行なっている。
results = -1 * data[:, 3].reshape(len(data),1)

# クラスのインスタンス化と次の実験条件の提案
seed(123)
myBopt = BayesianOptimization(f=None,
                                domain=domain, 
                                X=conditions, 
                                Y=results,
                                batch_size=4, 
                                evaluator_type = 'local_penalization',
                                maximize=True)
next_conditions = myBopt.suggest_next_locations()

print('\nNext conditions = [time of stimulation, frequency, voltage]')
print(f'{next_conditions}\n')
print(f'Previous experimental condition\n{myBopt.X}\n')
print(f'Previous experimental result (multiplied -1)\n{myBopt.Y}\n')