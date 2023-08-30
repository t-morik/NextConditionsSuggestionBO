import suggest
import numpy as np
import csv

# 結果のファイル名
data_file = 'conditions_k.csv'

# 条件を探索する領域
domain = [{'name': '刺激時間', 'type': 'discrete', 'domain': (5,10,15,20,15,30,35,40,45,50,55,60)},
            {'name': '刺激日', 'type': 'discrete', 'domain': (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)},
            {'name': '電圧', 'type': 'continuous', 'domain': (0, 10)}]

# データの読み取りおよび刺激日データ(2進数)を10進数に変換
data = []
with open(data_file, 'r') as f:
    header = next(csv.reader(f))
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        add_data = [float(line[0]),int(line[1], 2),float(line[2]),float(line[3])]
        data.append(add_data)
data = np.array(data)

# 次の実験条件の提案
next_conditions = suggest.suggest_parameter(domain=domain, data=data)

# 10進数 -> 2進数
l_next_conditions = next_conditions.tolist()
for x in l_next_conditions:
    x[1] = format(int(x[1]), '04b')

# 結果
print('\n次の条件 = [刺激時間, 刺激日, 電圧]')
for x in l_next_conditions:
    print(x)