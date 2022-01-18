#!/usr/bin/env python
# coding: utf-8

# # リッジラインプロット
# 
# **リッジラインプロット**とは

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[6]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[7]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[8]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[9]:


df = pd.read_csv(PATH_DATA)


# ### 年代別・作品別の合計連載週数

# In[10]:


df = add_years_to_df(df, unit_years=10)
df_plot =     df.value_counts(['years', 'cname']).reset_index(name='weeks')
# 年代順にソート
df_plot = df_plot.sort_values(
    'years', ascending=False, ignore_index=True)
fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h', 
    points=False)
fig.update_traces(
    side='positive', scalemode='count', width=4)
show_fig(fig)


# In[11]:


fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 年代別・作者別の合計連載週数

# In[14]:


df = add_years_to_df(df, unit_years=10)
df_plot =     df.value_counts(['years', 'creator']).reset_index(name='weeks')
# 年代順にソート
df_plot = df_plot.sort_values(
    'years', ascending=False, ignore_index=True)
fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h',
    points=False)
fig.update_traces(
    side='positive', scalemode='count', width=4)
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 年代別の各話ページ数

# In[18]:


# 年代順にソート
df = df.sort_values(
    'years', ascending=False, ignore_index=True)
fig = px.violin(
    df, x='pages', y='years', orientation='h',
    points=False)
fig.update_traces(
    side='positive', scalemode='count', width=4)
fig.update_xaxes(range=[0, 50])
show_fig(fig)

