# W11

## prep

```
uv add seaborn japanize-matplotlib setuptools
```

## ファイルパス

ファイルパスの指定方法を思い出す。

### プログラムのファイルを起点とする相対パス

```python
from pathlib import Path

Path(__file__).parent / "penguins.csv"
```

### ユーザーの作業ディレクトリを起点とする相対パス

```python
from pathlib import Path

Path.cwd() / "11" / "penguins.csv"
```


## Seaborn 

統計的なデータの可視化ライブラリ

- 11c.py
- 11d.py

Gallery https://seaborn.pydata.org/examples/index.html を参照して試してみよう。

サンプルデータは palmer penguins
https://allisonhorst.github.io/palmerpenguins/articles/art.html


## e-stat

e-stat で都道府県別のデータをダウンロードして自由に可視化してみよう。
