import os
import sys
import json
import copy
import argparse
import pprint
import pandas as pd
import suggest


def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def min_max_encode(x, source_min, source_max):
    return (x - source_min) / (source_max - source_min)


def min_max_decode(x_norm, source_min, source_max):
    return x_norm * (source_max - source_min) + source_min


def main(args):
    data_path = args.dataset
    domain_path = args.domain
    y_label = args.y_label
    normalize_Y = args.normalize_Y
    save_dir = check_dir(args.save_dir)
    batch_size = int(args.batch_size)
    normalize_X = args.normalize_X
    acquisition_type =args.acquisition_type

    # コマンドを command.txt に書き出す
    command = f"{sys.executable} " + " ".join(sys.argv)
    with open(f"{save_dir}/command.txt", "w") as f:
        f.write(command)

    # 条件を探索する領域
    with open(domain_path, 'r') as json_open:
        domain_origin = json.load(json_open)
    params = [k['name'] for k in domain_origin]

    # データの読み取り
    data = pd.read_csv(data_path, usecols=params + [y_label])
    print('=' * 100)
    print(f'dataset path: {data_path}')
    print(f'domain path: {domain_path}')
    print('-' * 100)
    print('実験データ')
    print(data)
    print('-'*100)
    print('探索範囲')
    pprint.pprint(domain_origin)


    # 次の実験条件の提案
    print('=' * 100)
    print('Bayesian Optimization start')
    print('-' * 100)
    print(f'Optimization: Max')
    print(f'acquisition_type: {acquisition_type}')
    print(f'normalize_Y: {normalize_Y}')
    print(f'normalize_X: {normalize_X}')
    print(f'batch_size: {batch_size}')
    domain = copy.deepcopy(domain_origin)
    if normalize_X:
        # 入力データのmin-max正規化
        for i, domain_each in enumerate(domain_origin):
            name = domain_each['name']
            min_val = min(domain_each['domain'])
            max_val = max(domain_each['domain'])
            assert min_val < max_val, 'domain invalid'
            data[name] = min_max_encode(x=data[name],
                                        source_min=min_val,
                                        source_max=max_val)
            domain[i]['domain'] = [0, 1]

        print('-' * 100)
        print('min-max正規化後の実験データ')
        print(data)
        print('-'*100)
        print('min-max正規化後の探索範囲')
        pprint.pprint(domain)

    next_conditions = suggest.suggest_parameter(domain=domain,
                                                data=data,
                                                normalize_Y=normalize_Y,
                                                batch_size=batch_size,
                                                acquisition_type=acquisition_type)
    if normalize_X:
        # スケーリングを実軸に戻してプリント
        for i, domain_each in enumerate(domain_origin):
            if domain_each['type'] != 'discrete':
                min_val = min(domain_each['domain'])
                max_val = max(domain_each['domain'])
                next_conditions[:, i] = min_max_decode(x_norm=next_conditions[:, i],
                                                       source_min=min_val,
                                                       source_max=max_val)

    next_conditions = pd.DataFrame(data=next_conditions, columns=params, dtype=float)
    save_path = f'{save_dir}/suggest_data.csv'
    next_conditions.to_csv(save_path)
    next_conditions.to_excel(save_path.replace('.csv', '.xlsx'))

    # 結果
    print('=' * 100)
    print(f'save path: {save_path}')
    print('-' * 100)
    print('次の実験条件')
    print(next_conditions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type=str,
                        default='./datasets/20250708/conditions.csv',
                        help='dataset path')
    parser.add_argument('--domain', type=str,
                        default='./datasets/20250708/domain.json',
                        help='domain path')
    parser.add_argument('--save_dir', type=str, required=True,
                        help='save path')
    parser.add_argument('--y_label', type=str, default='Score',
                        help='output label')
    parser.add_argument('--normalize_Y', action='store_true',
                        help='normalization of Y')
    parser.add_argument('--normalize_X', action='store_true',
                        help='minmax normalization of X')
    parser.add_argument('--batch_size', type=int, default=4,
                        help='suggest batch size')
    parser.add_argument('--acquisition_type', type=str, default='LCB',
                        help='acquisition_type: EI, LCB')

    args = parser.parse_args()

    main(args)