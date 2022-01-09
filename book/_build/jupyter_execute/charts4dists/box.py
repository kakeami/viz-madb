#!/usr/bin/env python
# coding: utf-8

# # Box plot

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[13]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[14]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[15]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[16]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・作品別の合計連載週数 

# In[18]:


df_plot =     df.value_counts(['mcname', 'cname']).reset_index(name='weeks')
fig = px.box(df_plot, x='mcname', y='weeks', title='雑誌別・作品別の合計連載週数')
show_fig(fig)


# [Histogram](https://kakeami.github.io/viz-madb/charts4dists/hist.html#id3)と同様に，2週以上掲載された**連載**作品に絞って作図してみます．

# In[19]:


df_plot = df_plot[df_plot['weeks']>=2].reset_index(drop=True)
fig = px.box(df_plot, x='mcname', y='weeks', title='雑誌別・連載作品別の合計連載週数')
show_fig(fig)


# ### 作者別の合計連載週数

# In[20]:


df_plot =     df.value_counts(['mcname', 'creator']).reset_index(name='weeks')
fig = px.box(df_plot, x='mcname', y='weeks', title='雑誌別・作者別の合計連載週数')
show_fig(fig)

