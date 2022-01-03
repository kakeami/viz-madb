#!/usr/bin/env python
# coding: utf-8

# # Bars

# ## 概要

# **Bars**（棒グラフ）とは，
# 
# > 縦軸にデータ量をとり、棒の高さでデータの大小を表したグラフです。（縦横が逆の場合もあります。）
# > 　値の高い項目や低い項目を判別するのに有効なグラフで、データの大小が、棒の高低で表されるので、データの大小を比較するのに適しています。
# 
# （「[総務省統計局，なるほど統計学園，棒グラフ](http://www.stat.go.jp/naruhodo/4_graph/shokyu/bou-graph.html)」より抜粋）
# 
# です．

# ## Plotlyによる作図方法

# Plotlyでは`plotly.express.bar()`で棒グラフを作成可能です．

# ```python
# import plotly.express as px
# fig = px.bar(df, x='col_x', y='col_y')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とした棒グラフのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[5]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[8]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[9]:


df = pd.read_csv(PATH_DATA)


# In[10]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# ### 作品別の合計連載週数（上位20作品）

# In[26]:


df_plot = df.value_counts('cname').reset_index(name='weeks').head(20)
fig = px.bar(df_plot, x='cname', y='weeks', title='作品別の合計連載週数')
show_fig(fig)


# ### 作者別の合計連載週数（上位20名）

# In[27]:


df_plot = df.value_counts('creator').reset_index(name='weeks').head(20)
fig = px.bar(df_plot, x='creator', y='weeks', title='作者別の合計連載週数')
show_fig(fig)

