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

# In[59]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[60]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[61]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[62]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の合計連載週数

# In[71]:


df_plot = df.value_counts('cname').reset_index(name='weeks')


# In[72]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作品別の合計連載週数')
show_fig(fig)


# :::{admonition} `nbins`オプション
# `plotly.express.histogram()`では`nbins`オプジョンでbin数を指定可能です．上記の例では，自動設定で作図するとbinが非常に細かくなってしまうため，便宜的に`nbins=100`を設定しています．
# :::

# これでは少し見づらいので，表示範囲を`fig.update_xaxis()`で変更します．

# In[73]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作品別の合計連載週数')
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 作者別の合計連載週数

# In[74]:


df_plot = df.value_counts('creator').reset_index(name='weeks')


# In[75]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作者別の合計連載週数')
show_fig(fig)


# In[76]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作者別の合計連載週数')
fig.update_xaxes(range=[0, 200])
show_fig(fig)

