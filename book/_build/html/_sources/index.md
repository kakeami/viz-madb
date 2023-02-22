# はじめに

```{only} html
[![Jupyter Book Badge](https://jupyterbook.org/_images/badge.svg)](https://jupyterbook.org)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-pandas](https://img.shields.io/badge/Made%20with-Pandas-1f425f.svg)](https://pandas.pydata.org/)
[![made-with-plotly](https://img.shields.io/badge/Made%20with-Plotly-1f425f.svg)](https://plotly.com/python/)
```

**データビジュアライゼーション**とは，数値や文章などのデータに基づいた情報を，人間が理解しやすい形に視覚化する技術を指します．

このサイトは，[文化庁の**メディア芸術データベース・ラボ（MADB Lab）**](https://mediag.bunka.go.jp/madb_lab/)で公開されている四大少年誌（
[週刊少年サンデー](https://websunday.net/)，
[週刊少年ジャンプ](https://www.shonenjump.com/j/)，
[週刊少年チャンピオン](https://www.akitashoten.co.jp/w-champion)，
[週刊少年マガジン](https://shonenmagazine.com/)
）のデータを用いて，データビジュアライゼーションの学習を手助けすることを目指しています．

::::{grid} 1 1 2 2
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:class-header: bg-light

📚**約47年分の四大少年誌データを採用**📚
^^^
データビジュアライゼーション（に限らずデータ分析全般）の学習において重要なのは，**分析対象のデータに興味を持てるかどうか**です．
本書では約47年の四大少年誌のマンガ作品データを採用しているため，モチベーションを保ちつつ学習を進めることが可能です．

<div style="text-align: center;">
<video autoplay loop muted playsinline width="100%" src="demo.mp4"></video>
</div>
:::


:::{grid-item-card}
:class-header: bg-light

👁️**インタラクティブな可視化**👁️
^^^
Plotlyで自由にズームイン・ズームアウトが可能なグラフを出力しています．
興味の赴くまま，グリグリグラフを動かしてみましょう．
新たな分析のヒントが得られるかもしれません．

<div style="text-align: center;">
<video autoplay loop muted playsinline width="100%" src="plotly.mp4"></video>
</div>

:::


:::{grid-item-card}
:class-header: bg-light

👩‍🎓**Docker + Jupyter Labで環境構築**🧑‍🎓
^^^

本書はJupyter Labで作成したソースコードをJupyter Bookで変換して構築しています．
[GitHub](https://github.com/kakeami/viz-madb)からソースコードをダウンロードすることで，手元で環境を再現可能ですので，どんどん新しい切り口でビジュアライゼーションしましょう．
詳細は[Appendix - 環境構築](https://kakeami.github.io/viz-madb/appendix/setup.html)をご参照ください．

![jupyter](figs/jupyter.png)

:::


:::{grid-item-card}
:class-header: bg-light

🇯🇵**MADB Labを利用**🇯🇵
^^^

MADB Labは，文化庁が提供する，メディア芸術作品に関するデータをより広く活用するためのウェブサイトです．
本書では，[v1.0として公開されているデータ](https://github.com/mediaarts-db/dataset/tree/1.0)を[前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html)して利用しています．
データセットの詳細は[公式リポジトリ](https://github.com/mediaarts-db/dataset)をご参照ください．

![madb](figs/madb.png)

:::
::::

## 本書で用いる用語

```{glossary}
量的変数
 数値で測ることができる変数です．例えば，ページ数，掲載位置，連載作品数，掲載週数，など．

質的変数
 数値で測ることができず，分類や種類を区別するために用いられる変数です．例えば，雑誌名，作品名，作家名，曜日，など.

雑誌
 `週刊少年ジャンプ`のように，マンガ雑誌を指します．
 データ中では`mcname`という変数名で管理されています．

雑誌巻号
 `週刊少年ジャンプ 1970年 表示号数31`のように，マンガ雑誌の号数を表します．
 データ中では`miname`という変数名で管理されています．

作品
 `男一匹ガキ大将`のように，マンガ雑誌に掲載されているマンガ作品を表します．
 データ中では`cname`という変数名で管理されています．

各話
 `土佐の源蔵の巻`のように，マンガ作品を構成するエピソードを指します．通常，雑誌巻号に一話ずつ掲載されます．
 データ中では`epname`という変数名で管理されています．
```

## こんなとき何を描く？

[Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)を参考にビジュアライゼーション手法を分類[^drop]しました．

[^drop]: [5 Directory of visualizations](https://clauswilke.com/dataviz/directory-of-visualizations.html)の
[5.1 Amounts](https://clauswilke.com/dataviz/directory-of-visualizations.html#amounts)
が「量を見たい」に，
[5.2 Distributions](https://clauswilke.com/dataviz/directory-of-visualizations.html#distributions)
が「分布を見たい」に，
[5.3 Proportions](https://clauswilke.com/dataviz/directory-of-visualizations.html#proportions)
が「比率を見たい」に，そして
[5.4 x–y relationships](https://clauswilke.com/dataviz/directory-of-visualizations.html#xy-relationships)
が「変数間の関係を見たい」に対応しています．
[5.5 Geospatial data](https://clauswilke.com/dataviz/directory-of-visualizations.html#directory-geospatial-data)
に関してはMADB Labの漫画雑誌データ上に十分な量の地理データが存在しなかったため，
[5.6 Uncertainty](https://clauswilke.com/dataviz/directory-of-visualizations.html#directory-uncertainty)
に関しては高度な数理統計の知識が必要になるためスコープ外としました．


::::{grid} 1 1 2 2
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:class-header: bg-light

**量を見たい**
^^^

{term}`質的変数`の量を見る最も一般的な方法は
[棒グラフ](https://kakeami.github.io/viz-madb/charts4amounts/bars.html)
を作図することです．
複数の{term}`質的変数`を扱う場合は，集合棒グラフや積上げ棒グラフも効果的です．
前者は特に絶対値を比較したい場合，後者は特に割合を比較したい場合に便利です．
全体像を俯瞰したい場合は，
[ヒートマップ](https://kakeami.github.io/viz-madb/charts4amounts/heatmap.html)
を選択肢に入れましょう．
ただし，ヒートマップは{term}`質的変数`の組合せの量を**色**で表現するため，数値を付記しなければ絶対値の比較が難しいことにご注意ください．

:::

:::{grid-item-card}
:class-header: bg-light
**分布を見たい**[^dist]
^^^

{term}`量的変数`の分布を見る際に直感的にわかりやすいのは，
[ヒストグラム](https://kakeami.github.io/viz-madb/charts4dists/hist.html)
や
[密度プロット](https://kakeami.github.io/viz-madb/charts4dists/density.html)
ですが，パラメータ設定に注意が必要です．
複数の{term}`量的変数`の分布を比較する際は，
[箱ひげ図](https://kakeami.github.io/viz-madb/charts4dists/box.html)，
[バイオリンプロット](https://kakeami.github.io/viz-madb/charts4dists/violin.html)，
そして
[ストリッププロット](https://kakeami.github.io/viz-madb/charts4dists/strip.html)
がおすすめです．
[リッジラインプロット](https://kakeami.github.io/viz-madb/charts4dists/ridgeline.html)
はバイオリンプロットと似ていますが，主に分布の時間的な変遷[^tb]を見る際に適しています．

[^tb]: [TensorBoard](https://www.tensorflow.org/tensorboard)でパラメータの学習過程を表現する際に使われていたり

:::

:::{grid-item-card}
:class-header: bg-light
**比率を見たい**
^^^

{term}`質的変数`の比率を可視化する際は，
[円グラフ](https://kakeami.github.io/viz-madb/charts4props/pie.html)
や
[棒グラフ](https://kakeami.github.io/viz-madb/charts4props/bars.html)
が用いられます．
前者は割合を直感的に表現する際に適しており，後者は絶対値を比較する際に適しています．
連続的に変化する比率を表現する際は
[積上げ密度プロット](https://kakeami.github.io/viz-madb/charts4props/stacked_den.html)
が効果的です．
複数の{term}`質的変数`の比率を表現する際は
[モザイクプロット](https://kakeami.github.io/viz-madb/charts4props/mosaic.html)，
[ツリーマップ](https://kakeami.github.io/viz-madb/charts4props/tree.html)，
そして
[パラレルセットグラフ](https://kakeami.github.io/viz-madb/charts4props/parallel.html)
を検討しましょう．
特に，モザイクプロットは二つの{term}`質的変数`の組合せの比率を表現したいときに，
ツリーマップは階層構造を持つ{term}`質的変数`の比率を表現したいときに，
そしてパラレルセットグラフは三つ以上の{term}`質的変数`の比率を表現したいときに力を発揮します．

:::

:::{grid-item-card}
:class-header: bg-light
**変数間の関係を見たい**[^assoc]
^^^

二つの{term}`量的変数`の関係を表現する典型的な方法は
[散布図](https://kakeami.github.io/viz-madb/charts4assocs/scatter.html)
を描くことです．
ただし，データ量が多すぎる場合は凡例が重複してわかりづらいので，
[二次元ヒストグラム](https://kakeami.github.io/viz-madb/charts4assocs/2d.html)
や
[等高線プロット](https://kakeami.github.io/viz-madb/charts4assocs/contours.html)
を検討しましょう．
{term}`量的変数`が三つ以上ある場合は，
[バブルチャート](https://kakeami.github.io/viz-madb/charts4assocs/scatter.html)
や
[並行座標プロット](https://kakeami.github.io/viz-madb/charts4assocs/slope.html)
[^slope]でその関係性を表現できます．
変数同士の相関係数を表現したい場合は
[コレログラム](https://kakeami.github.io/viz-madb/charts4assocs/correlo.html)
を使いましょう．
ある変数の時系列的な変化を表現する際は
[折れ線グラフ](https://kakeami.github.io/viz-madb/charts4assocs/line.html)
を用いることが多いです．
なお一般的な折れ線グラフは一変数の推移しか表現できませんが，
[工夫](https://kakeami.github.io/viz-madb/charts4assocs/connected.html)
すれば二変数の推移を表現することも可能です．

:::
::::


[^dist]: [Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)で分布を見る手法として紹介されているもののうち，次のものは割愛しました．**[Sina plot](https://www.tandfonline.com/doi/abs/10.1080/10618600.2017.1366914?journalCode=ucgs20)**：Plotlyで簡易に作図する方法が見当たらず，かつバイオリンプロットとストリッププロットで雰囲気をつかめると判断したため．**[Quantile-quantile plot](https://clauswilke.com/dataviz/ecdf-qq.html#qq-plots)**：理論的な確率密度分布と標本分布の一致性を見る目的で用いられることが多く，解釈に高度な数理統計学の知識が必要であり，本書のスコープを超えるため

[^assoc]: [Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)で分布を見る手法として紹介されているもののうち，次のものは割愛しました．**[Hexagonal binning](https://clauswilke.com/dataviz/overlapping-points.html#d-histograms)**：Plotlyで簡易に作図する方法が見当たらず，かつ二次元ヒストグラムで雰囲気をつかめると判断したため．

[^slope]: [Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)ではペアとなる二変数の関係性を示す手法として[Slopegraph](https://clauswilke.com/dataviz/visualizing-associations.html#associations-paired-data)が紹介されていますが，適切な例を見つけられなかったため割愛しました．代わりに（目的は全く異なりますが）似たような手段でデータを描画する並行座標プロットを追加しました．

## 謝辞

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [Jupyter](https://jupyter.org/)
- [Jupyter Book](https://jupyterbook.org/)
- [文部科学省文化庁，メディア芸術データベース・ラボ](https://mediag.bunka.go.jp/madb_lab/)
- [週刊少年サンデー](https://websunday.net/)
- [週刊少年ジャンプ](https://www.shonenjump.com/j/)
- [週刊少年チャンピオン](https://www.akitashoten.co.jp/w-champion)
- [週刊少年マガジン](https://shonenmagazine.com/)

## 参考文献

- [Claus O. Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/index.html)
- [Kiri Kuroda, いつか役に立つかもしれない資料](https://datareporting.kirikuroda.com/)
- [宋財泫 (Jaehyun Song)・矢内勇生 (Yuki Yanai), 私たちのR: ベストプラクティスの探究](https://www.jaysong.net/RBook/)
- [visualizing.jp](https://visualizing.jp/)
- [小久保 奈都弥，データ分析者のためのPythonデータビジュアライゼーション入門 コードと連動してわかる可視化手法](https://www.shoeisha.co.jp/book/detail/9784798163970)
- [岡崎 直観，機械学習帳](https://chokkan.github.io/mlnote/index.html)

## 作者

::::{grid} 2 2 2 2

:::{grid-item}
:columns: 4
```{image} figs/kakeami.jpg
:class: m-auto
:width: 200px
```
:::

:::{grid-item}
:columns: 7
二児の父．
都内マーケティング会社にて，機械学習・数理統計・数理最適化を用いたマーケティング技術の研究・開発に従事．
2022年より[ジョージア工科大学大学院にてComputer Scienceを学ぶ](https://omscs.gatech.edu/)．
マンガ好きが高じ，
Web教材「[マンガと学ぶデータビジュアライゼーション](https://kakeami.github.io/viz-madb/index.html)」
を作成．

- GitHub: [`@kakeami`](https://github.com/kakeami)
- Zenn: [`@kakeami`](https://zenn.dev/kakeami)
- Twitter: [`@_kakeami`](https://twitter.com/_kakeami)
:::
::::
