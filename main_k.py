import suggest
import numpy as np
import csv

# 結果のファイル名
data_file = 'conditions_k.csv'

# 条件を探索する領域
domain = [{'name': '電圧', 'type': 'continuous', 'domain': (0,20)},
            {'name': '刺激時間', 'type': 'continuous', 'domain': (0,240)},
            {'name': '刺激タイミング', 'type': 'continuous', 'domain': (0, 96)}]

# データの読み取り
data = np.loadtxt(data_file, delimiter= ",", skiprows=1)

# 次の実験条件の提案
next_conditions = suggest.suggest_parameter(domain=domain, data=data)

# 結果
print('\n次の条件 = [電圧, 刺激時間, 刺激タイミング]')
print(next_conditions)