#!/usr/bin/env python
# coding: utf-8

# # 折れ線グラフ

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# In[85]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings('ignore')


# In[3]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[54]:


# 連載週数の最小値
MIN_WEEKS = 5
# 抽出するマンガ作品数
N_CNAMES = 4


# In[55]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    # 凡例でグラフが潰れないよう調整
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[56]:


df = pd.read_csv(PATH_DATA)


# ## エピソードの掲載日と掲載位置

# In[98]:


mcnames = sorted(df['mcname'].unique())
for mcname in mcnames:
    df_tmp = df[df['mcname']==mcname].reset_index(drop=True)
    df_cname =         df_tmp.value_counts('cname').reset_index(name='weeks')
    df_cname =         df_cname.sort_values(
            'weeks', ascending=False, ignore_index=True)
    cnames = df_cname['cname'][:N_CNAMES].values
    df_plot = df_tmp[df_tmp['cname'].isin(cnames)].        reset_index(drop=True)
    df_plot = df_plot.rename(columns={
        'cname': '作品名',
        'datePublished': '掲載日',
        'pageStartPosition': '掲載位置',
        'epname': '話名'})
    fig = px.line(
        df_plot, x='掲載日', y='掲載位置',
        color='作品名', title=f'{mcname}の長期連載作品',
        hover_data=['話名'], height=500)
    fig.update_layout(hovermode='x unified')
    show_fig(fig)


# ### エピソードの話数と掲載位置

# In[75]:


def add_epid_to_df(df):
    """dfのcnameごとに1から順番に話数を追加"""
    cnames = df['cname'].unique()
    df_out = pd.DataFrame()
    
    for cname in cnames:
        df_tmp = df[df['cname']==cname].reset_index(drop=True)
        df_tmp['epid'] = df_tmp.index + 1
        df_out = pd.concat([df_out, df_tmp], ignore_index=True)
        
    return df_out


# In[99]:


mcnames = sorted(df['mcname'].unique())
for mcname in mcnames:
    df_tmp = df[df['mcname']==mcname].reset_index(drop=True)
    df_cname =         df_tmp.value_counts('cname').reset_index(name='weeks')
    df_cname =         df_cname.sort_values(
            'weeks', ascending=False, ignore_index=True)
    cnames = df_cname['cname'][:N_CNAMES].values
    df_plot = df_tmp[df_tmp['cname'].isin(cnames)].        reset_index(drop=True)
    df_plot = add_epid_to_df(df_plot)
    df_plot = df_plot.rename(columns={
        'cname': '作品名',
        'epname': '話名',
        'epid': '話数',
        'pageStartPosition': '掲載位置',})
    fig = px.line(
        df_plot, x='話数', y='掲載位置',
        facet_col='作品名', facet_col_wrap=2,
        title=f'{mcname}の長期連載作品',
        hover_data=['話名'], height=500)
    fig.update_layout(
        hovermode='x unified')
    show_fig(fig)


# In[ ]:




