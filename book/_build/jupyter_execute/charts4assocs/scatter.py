#!/usr/bin/env python
# coding: utf-8

# # 散布図・バブルチャート

# ## 概要

# **散布図（Scatter）** とは，主に二つの量的変数に対して，一つ一つのデータを **ドット** で表すグラフです．

# ![](../figs/charts/scatter.png)

# **バブルチャート（Bubble Chart)** とは

# ![](../figs/charts/bubble.png)

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
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と連載週数

# In[21]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[22]:


fig = px.scatter(
    df_plot, x='position', y='weeks', opacity=0.7, 
    hover_data=['cname'], title='作品別の平均掲載位置と連載週数')
fig.update_traces(
    marker={'size': 10, 'line_width':1,})
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='連載週数')
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数

# In[23]:


df_plot =     df.groupby(['mcname', 'cname'])['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['mcname', 'cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[24]:


fig = px.scatter(
    df_plot, x='position', y='weeks', color='mcname', 
    opacity=0.7,
    hover_data=['cname'], 
    color_discrete_sequence= px.colors.diverging.Portland,
    title='雑誌別・作品別の平均掲載位置と連載週数')
fig.update_traces(
    marker={'size': 10, 'line_width':1})
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='連載週数')
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数と平均ページ数

# In[25]:


df_plot =     df.groupby(['mcname', 'cname'])    [['pages', 'pageStartPosition']].    agg(['count', 'mean']).reset_index()
df_plot.columns = [
    'mcname', 'cname', 'weeks', 'pages',
    '_weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[26]:


fig = px.scatter(
    df_plot, x='position', y='weeks', color='mcname',
    size='pages', opacity=0.7,
    color_discrete_sequence= px.colors.diverging.Portland,
    hover_data=['cname'], title='雑誌別・作品別の平均掲載位置と連載週数')
fig.update_traces(
    marker={'line_width':1})
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='連載週数')

show_fig(fig)

