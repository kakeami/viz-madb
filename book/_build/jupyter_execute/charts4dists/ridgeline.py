#!/usr/bin/env python
# coding: utf-8

# # Ridgeline plot

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
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[7]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[26]:


df = pd.read_csv(PATH_DATA)


# ### 年代別・作品別の合計連載週数

# In[27]:


df = add_years_to_df(df, unit_years=10)
df_plot =     df.value_counts(['years', 'cname']).reset_index(name='weeks')
# 年代順にソート
df_plot = df_plot.sort_values(
    'years', ascending=False, ignore_index=True)
fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h')
fig.update_traces(
    side='positive', scalemode='count', width=4)
show_fig(fig)


# In[29]:


fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h')
fig.update_traces(
    side='positive', scalemode='count', width=4)
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 年代別・作者別の合計連載週数

# In[30]:


df = add_years_to_df(df, unit_years=10)
df_plot =     df.value_counts(['years', 'creator']).reset_index(name='weeks')
# 年代順にソート
df_plot = df_plot.sort_values(
    'years', ascending=False, ignore_index=True)
fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h')
fig.update_traces(
    side='positive', scalemode='count', width=4)
show_fig(fig)


# In[31]:


fig = px.violin(
    df_plot, x='weeks', y='years', orientation='h')
fig.update_traces(
    side='positive', scalemode='count', width=4)
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# In[ ]:




