import suggest
import numpy as np

# 結果のファイル名
data_file = 'conditions_m.csv'

# 条件を探索する領域
domain = [{'name': 'time of stimulation', 'type': 'discrete', 'domain': (0,1,2,3,4,5,6)},
            {'name': 'frequency', 'type': 'continuous', 'domain': (0.5, 10)},
            {'name': 'voltage', 'type': 'continuous', 'domain': (0, 18)}]

# データの読み取り
data = np.loadtxt(data_file, delimiter= ",", skiprows=1)

# 次の実験条件の提案
next_conditions = suggest.suggest_parameter(domain=domain, data=data)

# 結果
print('\n次の条件 = [time of stimulation, frequency, voltage]')
print(next_conditions)