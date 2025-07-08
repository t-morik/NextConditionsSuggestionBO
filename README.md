# GPyOptのバッチベイズ的最適化による実験条件の提案
## 環境構築方法(python=3.9.10で確認)
```
git clone git@github.com:t-morik/NextConditionsSuggestionBO.git
cd NextConditionsSuggestionBO
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
git submodule add https://github.com/SheffieldML/GPyOpt.git ./GPyOpt
cd ./GPyOpt
git submodule update --init --recursive
python setup.py develop
cd ../
```

(*) ```git submodule add```で何らかのエラーが発生し，再度やり直す場合は，下記の手順でGPyOptのリンクを消しておく．

```
1. GPyOptのdirectoryを削除する
2. .gitmodulesから対象のモジュール情報を削除する
3. .git/configのモジュール情報を削除する
4. .git/modules/以下にあるsubmoduleでとってきたリポジトリを削除する
5. git rm --cached GPyOpt
```

## 実行方法(main.pyについて)
`<PATH>/conditions.csv`にこれまでの実験条件と結果を加える。

現在のプログラム上では、電圧(連続値)、刺激時間(連続値)刺激タイミング(連続値)について最適化を行うようになっている。

なお`<PATH>/conditions.csv`は以下のような形式となっている。

| 電圧 | 刺激時間 | 刺激タイミング | Score |
|----|------|---------|-------|
| 1  | 3.4  | 4.5     | 5     |
| 3  | 6.7  | 1.2     | 10    |
| 4  | 9.2  | 9.9     | 15    |
| 6  | 1.5  | 15.4    | 10    |
| ~  | ~    | ~       | ~     |

以上のような`<PATH>/conditions.csv`を作成したら，
パラメタ探索する条件を設定する`<PATH>/domain.json`を作成する．
```
[
  {"name": "電圧", "type": "continuous", "domain": [0.1,20]},
  {"name": "刺激時間", "type": "continuous", "domain": [1,240]},
  {"name": "刺激タイミング", "type": "continuous", "domain": [1, 96]}
]
```

上記2つのファイルを作成したら，下記のコマンドを実行する．

```
python main.py --dataset ./datasets/20250708/conditions.csv --domain ./datasets/20250708/domain.json --save_dir ./results/20250708/normalize_Y --normalize_Y
```

と実行することで以下のように結果を得ることができる。
`Error in parallel computation. Fall back to single process!`は評価を取る際に並列化できなかったというだけなので問題ないと思われる。
Next conditionsとして次行うべき実験条件が表示される。
また、Previous experimental conditionとPrevious experimental result (multiplied -1)にこれまで行なった実験条件とその結果が表示されるので誤っていないか確認する。

```
Error in parallel computation. Fall back to single process!

Next conditions = [time of stimulation, frequency, voltage]
[[6.         1.3835053  4.87180085]
 [5.         1.87077515 3.96820215]
 [6.         3.33889503 3.70235029]
 [6.         0.85271185 8.59540011]]

```


## Reference
- GPyOptのライブラリ (https://github.com/SheffieldML/GPyOpt)
- GPyOptにおけるバッチベイズ的最適化の理論 (https://proceedings.mlr.press/v51/gonzalez16a.html)