#!/usr/bin/env python
# coding: utf-8

# # コレログラム

# ## 概要
# 

# ::: {note}
# 時系列解析において，自己相関を見るために時点をずらした系列との相関係数を示したものもコレログラムと呼びますが，ここで紹介するのは変数同士の相関係数を示したものです．
# :::

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.graph_objects as go
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


# In[11]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と掲載週数

# In[13]:


df_plot =     df.groupby(['cname'])    [['pages', 'pageStartPosition']].    agg(['count', 'mean']).reset_index()
df_plot.columns = [
    '作品名', '掲載週数', '平均ページ数',
    '_weeks', '平均掲載位置']
df_plot =     df_plot[df_plot['掲載週数'] >= MIN_WEEKS].    reset_index(drop=True)
df_plot = df_plot.drop(columns=['_weeks'])
df_corr = df_plot.corr()
df_corr = df_corr.iloc[::-1]


# In[14]:


df_corr


# In[21]:


fig = go.Figure(go.Heatmap(
    x=df_corr.index.values,
    y=df_corr.columns.values,
    z=df_corr.values,))
fig.update_layout(
    title='各変数の相関')
show_fig(fig)


# In[22]:


fig = px.scatter_matrix(
    df_plot[['平均掲載位置', '平均ページ数', '掲載週数']],
    opacity=0.7, height=500)
fig.update_traces(marker={'line_width':1})
fig.update_layout(title='各変数の散布図行列')
show_fig(fig)


# ## 練習問題

# In[ ]:




