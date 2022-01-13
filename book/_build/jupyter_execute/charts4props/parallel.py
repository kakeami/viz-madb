#!/usr/bin/env python
# coding: utf-8

# # Parallel sets

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[7]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'
# weekdayを曜日に変換
WD2STR = {
    0: 'Mon.',
    1: 'Tue.',
    2: 'Wed.',
    3: 'Thu.',
    4: 'Fri.',
    5: 'Sat.',
    6: 'Sun.',}


# In[3]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[17]:


def add_weekday_to_df(df):
    """曜日情報をdfに追加"""
    df_new = df.copy()
    df_new['weekday'] =         pd.to_datetime(df_new['datePublished']).dt.weekday
    df_new['weekday_str'] = df_new['weekday'].apply(
        lambda x: WD2STR[x])
    return df_new


# In[20]:


def add_mcid_to_df(df):
    """mcnameのindexをdfに追加"""
    df_new = df.copy()
    mcname2mcid = {
        x: i for i, x in enumerate(df['mcname'].unique())}
    df_new['mcid'] = df_new['mcname'].apply(
        lambda x: mcname2mcid[x])
    return df_new


# In[5]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[6]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別・曜日別の雑誌巻号数

# In[35]:


# 10年単位で区切ったyearsを追加
df_plot = df[~df['miname'].duplicated()].reset_index(drop=True)
df_plot = add_years_to_df(df_plot, 10)
df_plot = add_weekday_to_df(df_plot)
df_plot = add_mcid_to_df(df_plot)
df_plot = df_plot.sort_values(
    ['weekday', 'years', 'mcname'], ignore_index=True)


# In[36]:


fig = px.parallel_categories(
    df_plot, dimensions=['mcname', 'years', 'weekday_str'],
    color='mcid', 
    labels={
        'years': '年代', 'mcname': '雑誌名', 
        'weekday_str': '発売曜日'},
    title='雑誌別・年代別・曜日別の雑誌巻号数')
fig.update_coloraxes(showscale=False)
show_fig(fig)

