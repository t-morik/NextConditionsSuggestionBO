# GPyOptのバッチベイズ的最適化による実験条件の提案
## 環境構築方法(python=3.9.15で確認)
```
git clone git@gitlab.com:funalab/next_conditions_suggestion_bo.git
cd next_conditions_suggestion_bo
git submodule update --init --recursive
python -m venv venv
source venv/bin/activate
pip install --upgrade pip 
cd GPy
pip -v install -e .
cd ../gpyopt
python setup.py develop
pip install -r ../requirements.txt
```
## 実行方法
`conditions.csv`にこれまでの実験条件と結果を加える。  

現在のプログラム上では、刺激印加のタイミング(離散値)、周期(連続値)、電圧(連続値)について最適化を行うようになっている。  

なお`conditions.txt`は以下のような形式となっている。

| time of stimulation | frequency |  voltage |  result | 
| ------------------- | --------- | -------- | ------- | 
| 1                   | 3.4       | 4.5      | 5       | 
| 3                   | 6.7       | 1.2      | 10      | 
| 4                   | 9.2       | 9.9      | 15      | 
| 6                   | 1.5       | 15.4     | 10      | 
| ~                   | ~         | ~        | ~       | 

以上のような`condtions.txt`を作成したら  

```
python main.py
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

Previous experimental condition
[[6.  1.  2. ]
 [6.  1.3 3.9]
 [4.  8.3 2.4]]
Previous experimental result (multiplied -1)
[[-0.118]
 [-0.204]
 [-0.   ]]
```


## Reference
- GPyOptのライブラリ  
    https://github.com/SheffieldML/GPyOpt  
- GPyOptにおけるバッチベイズ的最適化の理論  
    https://proceedings.mlr.press/v51/gonzalez16a.html  