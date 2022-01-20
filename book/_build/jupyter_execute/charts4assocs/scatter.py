#!/usr/bin/env python
# coding: utf-8

# # 散布図・バブルチャート

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[5]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[36]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[63]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[7]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と連載週数

# In[64]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[65]:


fig = px.scatter(
    df_plot, x='position', y='weeks', opacity=0.7, 
    hover_data=['cname'], title='作品別の平均掲載位置と連載週数')
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数

# In[66]:


df_plot =     df.groupby(['mcname', 'cname'])['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['mcname', 'cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[67]:


fig = px.scatter(
    df_plot, x='position', y='weeks', color='mcname', 
    opacity=0.7,
    hover_data=['cname'], 
    title='雑誌別・作品別の平均掲載位置と連載週数')
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数と平均ページ数

# In[68]:


df_plot =     df.groupby(['mcname', 'cname'])    [['pages', 'pageStartPosition']].    agg(['count', 'mean']).reset_index()
df_plot.columns = [
    'mcname', 'cname', 'weeks', 'pages',
    '_weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[69]:


fig = px.scatter(
    df_plot, x='position', y='weeks', color='mcname',
    size='pages', opacity=0.7,
    hover_data=['cname'], title='雑誌別・作品別の平均掲載位置と連載週数')
show_fig(fig)


# In[ ]:




