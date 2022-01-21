#!/usr/bin/env python
# coding: utf-8

# # 並行座標プロット

# ## 概要

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
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と連載週数

# In[6]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot = df_plot[['cname', 'position', 'weeks']]
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[8]:


fig = px.parallel_coordinates(
    df_plot, color='position',
    labels={'position': '掲載位置', 'weeks': '掲載週数'})
show_fig(fig)


# ### 作品別の平均掲載位置と連載週数と平均ページ数

# In[10]:


df_plot =     df.groupby(['mcname', 'cname'])    [['pages', 'pageStartPosition']].    agg(['count', 'mean']).reset_index()
df_plot.columns = [
    'mcname', 'cname', 'weeks', 'pages',
    '_weeks', 'position']
df_plot = df_plot[[
    'mcname', 'cname', 'position', 'pages', 'weeks']]
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[12]:


fig = px.parallel_coordinates(
    df_plot, color='position',
    labels={
        'position': '掲載位置', 'weeks': '掲載週数',
        'pages': 'ページ数'})
show_fig(fig)

