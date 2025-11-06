# --- Load GPyOpt
import numpy as np
from GPyOpt.methods import BayesianOptimization
from numpy.random import seed


def suggest_parameter(domain, data, normalize_Y, batch_size, acquisition_type, seed_num):
    data = data.to_numpy()
    # 末列以外の部分で実験条件の設定を行なっている。
    conditions = data[:, 0:(len(data[0])-1)]
    results = data[:, (len(data[0])-1)].reshape(len(data),1)

    # 最小化問題にするため
    results = -1 * results

    # クラスのインスタンス化と次の実験条件の提案
    seed(seed_num)
    myBopt = BayesianOptimization(f=None,
                                    domain=domain,
                                    X=conditions,
                                    Y=results,
                                    batch_size=batch_size,
                                    normalize_Y=normalize_Y,
                                    acquisition_type=acquisition_type,
                                    evaluator_type = 'local_penalization'
                                    )
    next_conditions = myBopt.suggest_next_locations()

    return next_conditions