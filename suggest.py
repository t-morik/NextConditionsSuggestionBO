# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np
from numpy.random import seed

def suggest_parameter(domain, data):
    # condtions.txtのファイルから実験条件と結果の組み合わせを取ってくる。
    conditions = data[:, 0:(len(data[0])-1)] # 末列以外の部分で実験条件の設定を行なっている。
    results = -1 * data[:, (len(data[0])-1)].reshape(len(data),1)

    # クラスのインスタンス化と次の実験条件の提案
    seed(123)
    myBopt = BayesianOptimization(f=None,
                                    domain=domain,
                                    X=conditions,
                                    Y=results,
                                    batch_size=4,
                                    evaluator_type = 'local_penalization'
                                    )
    next_conditions = myBopt.suggest_next_locations()

    return next_conditions