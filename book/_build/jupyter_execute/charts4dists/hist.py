#!/usr/bin/env python
# coding: utf-8

# # Histogram

# ## 概要

# **Histogram**（ヒストグラム）とは，例えば下図のように，

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[4]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の合計連載週数

# In[5]:


df_plot = df.value_counts('cname').reset_index(name='weeks')


# In[12]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100)
show_fig(fig)


# ### 作者別の合計連載週数

# In[14]:


df_plot = df.value_counts('creator').reset_index(name='weeks')


# In[15]:


fig = px.histogram(df_plot, x='weeks', nbins=100)
show_fig(fig)

