#!/usr/bin/env python
# coding: utf-8

# # 2次元ヒストグラム

# ## 概要
# 
# **2次元ヒストグラム**とは，2種類の量的変数の分布を見るために用いられる手法です．
# 集計したい変数の階級を横軸・縦軸にとり，その階級に含まれるデータの数を色で示します．

# ![2d](../figs/charts/2d.png)

# 例えば上図は，雑誌別に掲載位置（X軸）と掲載週数（Y軸）の作品数を表した2次元ヒストグラムです．色が明るいほど，該当する作品が多いことを表します．

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.density_heatmap()`を用いて作図できます．

# ```python
# import plotly.express as px
# fig = px.density_heatmap(
#     df, x='col_x', y='col_y')
# ```

# 上記の例では，`df`の`col_x`および`col_y`について，階級ごとにデータの下図を集計した二次元ヒストグラムのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と連載週数

# In[6]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[7]:


fig = px.density_heatmap(
    df_plot, x='position', y='weeks',
    title='作品別の平均掲載位置と掲載週数')
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='掲載週数')
show_fig(fig)


# In[8]:


fig.update_yaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と掲載週数

# In[9]:


df_plot =     df.groupby(['mcname', 'cname'])['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns =     ['mcname', 'cname', 'weeks', 'position']
df_plot = df_plot.sort_values(
    'mcname', ignore_index=True)
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[10]:


fig = px.density_heatmap(
    df_plot, x='position', y='weeks',
    facet_col='mcname', facet_col_wrap=2,
    title='雑誌別・作品別の平均掲載位置と掲載週数')
fig.for_each_annotation(
    lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(range=[0, 200])
show_fig(fig)


# ## 練習問題

# In[ ]:




