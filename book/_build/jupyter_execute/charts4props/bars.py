#!/usr/bin/env python
# coding: utf-8

# # Bars

# ## 概要

# ## Plotlyによる作図方法

# ### Bars

# ### Stacked bars

# ### Grouped bars

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


# In[14]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[15]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[16]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別の合計作品数

# In[46]:


col_count = 'cname'


# In[55]:


df_plot =     df.groupby('mcname')[col_count].nunique().reset_index()
df_plot['ratio'] = df_plot[col_count] / df_plot[col_count].sum()
df_plot['years'] = '全期間'
fig = px.bar(
    df_plot, x='years', y='ratio', barmode='stack', 
    color='mcname', title='雑誌別の合計作品数')
show_fig(fig)


# ### 雑誌別・年代別の合計作品数

# In[60]:


col_count = 'cname'


# In[61]:


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


# In[62]:


fig = px.bar(
    df_plot, x='years', y='ratio', color='mcname',
    barmode='stack', title='雑誌別・年代別の合計作品数')
show_fig(fig)


# In[63]:


fig = px.bar(
    df_plot, x='years', y='ratio', color='mcname',
    barmode='group', title='雑誌別・年代別の合計作品数')
show_fig(fig)


# ### 雑誌別の合計作者数

# In[53]:


col_count = 'creator'


# In[56]:


df_plot =     df.groupby('mcname')[col_count].nunique().reset_index()
df_plot['ratio'] = df_plot[col_count] / df_plot[col_count].sum()
df_plot['years'] = '全期間'
fig = px.bar(
    df_plot, x='years', y='ratio', barmode='stack', 
    color='mcname', title='雑誌別の合計作者数')
show_fig(fig)


# ### 雑誌別・年代別の合計作者数

# In[57]:


col_count = 'creator'


# In[58]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 5)
# mcname, yearsで集計
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
# years単位で集計してdf_plotにカラムを追加
df_tmp = df_plot.groupby('years')[col_count].sum().reset_index(
    name='years_total')
df_plot = pd.merge(df_plot, df_tmp, how='left', on='years')
# years合計あたりの比率を計算
df_plot['ratio'] = df_plot[col_count] / df_plot['years_total']


# In[59]:


fig = px.bar(
    df_plot, x='years', y='ratio', color='mcname',
    barmode='stack', title='雑誌別・年代別の合計作者数')
show_fig(fig)


# In[64]:


fig = px.bar(
    df_plot, x='years', y='ratio', color='mcname',
    barmode='group', title='雑誌別・年代別の合計作者数')
show_fig(fig)

