#!/usr/bin/env python
# coding: utf-8

# # モザイクプロット

# ## 概要

# **モザイクプロット**とは，

# ## Plotlyによる作図方法

# https://plotly.com/python/bar-charts/

# 上記を参考に作図可能

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別の合計作品数

# In[6]:


col_count = 'cname'


# In[7]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
# mcname, yearsで集計
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
# years単位で集計してdf_plotにカラムを追加
df_tmp = df_plot.groupby('years')[col_count].sum().reset_index(
    name='years_total')
df_plot = pd.merge(df_plot, df_tmp, how='left', on='years')
# years合計あたりの比率を計算
df_plot['ratio'] = df_plot[col_count] / df_plot['years_total']


# In[13]:


fig = go.Figure()
for mcname in df_plot['mcname'].unique():
    df_tmp =         df_plot[df_plot['mcname']==mcname].reset_index(drop=True)
    widths = df_tmp['years_total']
    fig.add_trace(go.Bar(
        name=mcname,
        x=df_tmp['years_total'].cumsum() - widths,
        y=df_tmp['ratio'],
        width=widths,
        offset=0,))
fig.update_xaxes(
    tickvals=widths.cumsum() - widths/2,
    ticktext=df_plot['years'].unique(),)
fig.update_layout(barmode='stack')
show_fig(fig)    


# ### 雑誌別・年代別の合計作者数

# In[14]:


col_count = 'creator'


# In[15]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
# mcname, yearsで集計
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
# years単位で集計してdf_plotにカラムを追加
df_tmp = df_plot.groupby('years')[col_count].sum().reset_index(
    name='years_total')
df_plot = pd.merge(df_plot, df_tmp, how='left', on='years')
# years合計あたりの比率を計算
df_plot['ratio'] = df_plot[col_count] / df_plot['years_total']


# In[16]:


fig = go.Figure()
for mcname in df_plot['mcname'].unique():
    df_tmp =         df_plot[df_plot['mcname']==mcname].reset_index(drop=True)
    widths = df_tmp['years_total']
    fig.add_trace(go.Bar(
        name=mcname,
        x=df_tmp['years_total'].cumsum() - widths,
        y=df_tmp['ratio'],
        width=widths,
        offset=0,))
fig.update_xaxes(
    tickvals=widths.cumsum() - widths/2,
    ticktext=df_plot['years'].unique(),)
fig.update_layout(barmode='stack')
show_fig(fig)    

