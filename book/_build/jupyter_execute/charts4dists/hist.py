#!/usr/bin/env python
# coding: utf-8

# # Histogram

# ## 概要

# **Histogram**（ヒストグラム）とは，例えば下図のように，

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.histogram()`でヒストグラムを作成可能です．

# ```python
# import plotly.express as px
# fig = px.histogram(df, x='col_x')
# ```

# 上記の例では，`df`の`col_x`列をX軸，その度数をY軸に取ったヒストグラムのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[2]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[3]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の合計連載週数

# In[46]:


df_plot = df.value_counts('cname').reset_index(name='weeks')


# In[47]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作品別の合計連載週数')
show_fig(fig)


# :::{admonition} `nbins`オプション
# `plotly.express.histogram()`では`nbins`オプジョンでbin数を指定可能です．上記の例では，自動設定で作図するとbinが非常に細かくなってしまうため，便宜的に`nbins=100`を設定しています．
# :::

# [事前分析](https://kakeami.github.io/viz-madb/eda/eda.html#cname)の結果，`df`は1週限りの読み切り作品や企画作品を含むことがわかっています．
# 2週以上のマンガ作品（**連載**作品）に限定して，もう一度分布を見てみましょう．

# In[53]:


df_plot = df_plot[df_plot['weeks']>=2].reset_index(drop=True)
fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='連載作品別の合計連載週数')
show_fig(fig)


# 少し緩やかな分布になりました．

# ### 作者別の合計連載週数

# In[54]:


df_plot = df.value_counts('creator').reset_index(name='weeks')


# In[58]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作者別の合計連載週数')
show_fig(fig)


# In[ ]:




