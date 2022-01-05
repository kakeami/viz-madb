# はじめに

```{only} html
[![Jupyter Book Badge](https://jupyterbook.org/_images/badge.svg)](https://jupyterbook.org)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-pandas](https://img.shields.io/badge/Made%20with-Pandas-1f425f.svg)](https://pandas.pydata.org/)
[![made-with-plotly](https://img.shields.io/badge/Made%20with-Plotly-1f425f.svg)](https://plotly.com/python/)
```

**データ・ビジュアライゼーション**とは，数値や文章などのデータに基づいた情報を，人間が理解しやすい形に視覚化する技術を指します．

このサイトは，[文化庁の**メディア芸術データベース・ラボ**（**MADB Lab**）](https://mediag.bunka.go.jp/madb_lab/)で公開されている**四大少年誌**（
[週刊少年ジャンプ](https://www.shonenjump.com/j/)，
[週刊少年サンデー](https://websunday.net/)，
[週刊少年マガジン](https://shonenmagazine.com/)，
[週刊少年チャンピオン](https://www.akitashoten.co.jp/w-champion)
）のデータを用いて，データ・ビジュアライゼーションの学習を手助けすることを目指しています．

:::{panels}
:container: +full-width
:column: col-lg-6 px-2 py-2
:card:

---
📚**約47年分の四大少年誌の掲載作品データを採用**📚
^^^
データ分析の学習において重要なのは，**分析対象のデータに興味を持てるかどうか**だと思います．
本サイトでは約47年の四大少年誌のマンガ作品データを採用しているため，（少なくとも私は）飽きることなく学習を継続可能です！

（いい感じのgifを貼る）

---
👁️**Plotlyによるインタラクティブなビジュアライゼーション**👁️
^^^
Plotlyで自由にズームイン・ズームアウトが可能なグラフを出力しています．
興味の赴くまま，グリグリグラフを動かしてみましょう．
新たな分析のヒントが得られるかもしれません．

（いい感じのgifを貼る）

---
👩‍🎓**Jupyter形式でPythonのソースコードを公開**🧑‍🎓
^^^

本サイトはJupyter Labで作成したソースコードをJupyter Bookでビルドして構築しています．
[GitHub](https://github.com/kakeami/viz-madb)からソースコードをダウンロードすることで，手元で環境を再現可能ですので，どんどん新しい切り口でビジュアライゼーションしましょう．
環境構築に関する詳細は[README.md](https://github.com/kakeami/viz-madb)をご参照ください．

![jupyter](figs/jupyter.png)

---
🇯🇵**メディア芸術データベース・ラボ（MADB Lab）を利用**🇯🇵
^^^

MADB Labは，文化庁が提供する，メディア芸術作品に関するデータをより広く活用するためのウェブサイトです．
本サイトでは，[v1.0として公開されているデータ](https://github.com/mediaarts-db/dataset/tree/1.0)を[前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html)して利用しています．
データセットの詳細は[公式リポジトリ](https://github.com/mediaarts-db/dataset)をご参照ください．

![madb](figs/madb.png)

:::

## こんなとき何を描く？

本サイトで紹介するビジュアライゼーション手法を，Fundamentals of Data Visualizationを参考に分類しました．

:::{panels}
:container: +full-width
:column: col-lg-6 px-2 py-2

---
**推移を見たい**
^^^

---
**量を見たい**
^^^

---
**分布を見たい**
^^^

---
**比率を見たい**
^^^

---
**変数間の関係を見たい**
^^^

:::

## 謝辞

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Jupyter](https://jupyter.org/)
- [Jupyter Book](https://jupyterbook.org/)
- [文部科学省文化庁，メディア芸術データベース・ラボ](https://mediag.bunka.go.jp/madb_lab/)
- [週刊少年ジャンプ](https://www.shonenjump.com/j/)
- [週刊少年サンデー](https://websunday.net/)
- [週刊少年マガジン](https://shonenmagazine.com/)
- [週刊少年チャンピオン](https://www.akitashoten.co.jp/w-champion)

## 参考文献

- [Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)
- [小久保 奈都弥，データ分析者のためのPythonデータビジュアライゼーション入門 コードと連動してわかる可視化手法](https://www.shoeisha.co.jp/book/detail/9784798163970)
- [総務省統計局，なるほど統計学園](https://www.stat.go.jp/naruhodo/)
