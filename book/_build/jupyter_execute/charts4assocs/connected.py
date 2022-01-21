#!/usr/bin/env python
# coding: utf-8

# # 折れ線グラフ（2変数）

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


# In[4]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[5]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    # 凡例でグラフが潰れないよう調整
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[6]:


df = pd.read_csv(PATH_DATA)


# ### 作品数と作家数の推移

# In[77]:


YEARS_TO_DROP = ['1970', '2015']


# In[78]:


df = add_years_to_df(df, 5)
df_plot =     df.groupby('years')['cname', 'creator'].nunique().reset_index()
# 最初と最後の年度は不十分なデータなので除外
df_plot =     df_plot[~df_plot['years'].isin(YEARS_TO_DROP)]    .reset_index(drop=True)


# In[79]:


fig = px.line(
    df_plot, x='cname', y='creator', text='years')
fig.update_traces(textposition='bottom right')
show_fig(fig)


# ### 雑誌別の作品数と作家数の推移

# In[85]:


df = add_years_to_df(df, 5)
df_plot =     df.groupby(['mcname', 'years'])['cname', 'creator']    .nunique().reset_index()
# 最初と最後の年度は不十分なデータなので除外
df_plot =     df_plot[~df_plot['years'].isin(YEARS_TO_DROP)]    .reset_index(drop=True)


# In[87]:


fig = px.line(
    df_plot, x='cname', y='creator', text='years',
    facet_col='mcname', facet_col_wrap=2)
fig.update_traces(textposition='bottom right')
fig.update_xaxes(title='作品数')
fig.update_yaxes(title='作家数')
show_fig(fig)

