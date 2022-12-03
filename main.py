# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np
from numpy.random import seed

# 条件を探索する領域
domain = [{'name': 'time of stimulation', 'type': 'discrete', 'domain': (0,1,2,3,4,5,6)},
            {'name': 'frequency', 'type': 'continuous', 'domain': (0.5, 10)},
            {'name': 'voltage', 'type': 'continuous', 'domain': (0, 18)}]

# condtions.txtのファイルから実験条件と結果の組み合わせを取ってくる。
data = np.loadtxt('./conditions.txt', delimiter= ",", skiprows=1)
conditions = data[:, 0:3] # 末列以外の部分で実験条件の設定を行なっている。

# 実験条件の組み合わせを受け取ったら結果を返す関数(すでに実験済みの条件のみ)
def f(x, data = data):
    for i in range(0,3):
        if np.array_equal(x, data[i][0:3]):
            return data[i][3]

# クラスのインスタンス化と次の実験条件の提案
seed(123)
myBopt = BayesianOptimization(f=f, domain=domain, X=conditions, batch_size=4, evaluator_type = 'local_penalization')
next_conditions = myBopt.suggest_next_locations()

print(f'{next_conditions = }')