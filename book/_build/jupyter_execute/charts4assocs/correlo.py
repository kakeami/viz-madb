#!/usr/bin/env python
# coding: utf-8

# # コレログラム

# ## 概要
# 

# **コレログラム（Correlogram）** とは，複数の量的変数を対象として，その **相関係数** を **色** で表すグラフです．
# [ヒートマップ](https://kakeami.github.io/viz-madb/charts4amounts/heatmap.html)の一種と捉えることができます．

# ::: {note}
# 時系列解析において，自己相関を見るために時点をずらした系列との相関係数を示したものもコレログラムと呼びますが，ここで紹介するのは変数同士の相関係数を示したものです．
# :::

# ![](../figs/charts/correlo.png)

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[10]:


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

import warnings
warnings.filterwarnings('ignore')


# In[11]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[12]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[13]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[14]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と掲載週数

# In[15]:


df_plot =     df.groupby(['cname'])    [['pages', 'pageStartPosition']].    agg(['count', 'mean']).reset_index()
df_plot.columns = [
    '作品名', '掲載週数', '平均ページ数',
    '_weeks', '平均掲載位置']
df_plot =     df_plot[df_plot['掲載週数'] >= MIN_WEEKS].    reset_index(drop=True)
df_plot = df_plot.drop(columns=['_weeks'])
df_corr = df_plot.corr()
df_corr = df_corr.iloc[::-1]


# In[16]:


df_corr


# In[26]:


fig = ff.create_annotated_heatmap(
    df_corr.values,
    x=list(df_corr.index.values),
    y=list(df_corr.columns.values),
    annotation_text=df_corr.values,
    #colorscale='BlueRed_r'
)
show_fig(fig)

