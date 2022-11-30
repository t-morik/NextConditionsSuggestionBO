# GPyOptのバッチベイズ的最適化による実験条件の提案
## 環境構築方法
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
`conditions.txt`にこれまでの実験条件と結果を加える。  

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

```
Error in parallel computation. Fall back to single process!
next_conditions = array([[ 5.        ,  1.58741141, 14.72770675],
       [ 3.        ,  7.34914362,  5.14228276],
       [ 7.        ,  5.67603118,  0.58706094],
       [ 6.        ,  8.84558988,  9.27243744]])
```


## Reference
- GPyOptのライブラリ  
    https://github.com/SheffieldML/GPyOpt  
- GPyOptにおけるバッチベイズ的最適化の理論  
    https://proceedings.mlr.press/v51/gonzalez16a.html  