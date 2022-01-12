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


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[79]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[80]:


def add_week_range_to_df(df, n_ranges=4):
    """weeksをn_ranges単位で分割"""
    weeks = sorted(df['weeks'].unique())


# In[97]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[98]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別の合計作品数

# In[99]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
df_plot = df.groupby(['mcname', 'years', 'cname'])    ['epname'].count().reset_index(name='weeks')
df_plot['single'] = df_plot['weeks']==1
df_plot['single_int'] = df_plot['single'].astype(int)
df_plot = df_plot.sort_values(
    ['mcname', 'years'], ascending=True)


# In[100]:


fig = px.parallel_categories(
    df_plot, dimensions=['years', 'mcname', 'single'],
    color='single_int', color_continuous_scale=['Green', 'Red'],
    labels={'years': '年代', 'mcname': '雑誌名', 'single': '一週のみ？'},
    title='雑誌名・年代別の合計作品数')
fig.update_coloraxes(showscale=False)
show_fig(fig)


# In[ ]:




