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
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別の合計作品集数

# In[19]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
df_plot = df.groupby(['mcname', 'years', 'cname'])    ['epname'].count().reset_index(name='weeks')
df_plot = df_plot.sort_values('weeks', ascending=True)


# In[20]:


fig = px.parallel_categories(
    df_plot, dimensions=['mcname', 'years'],
    color='weeks')
show_fig(fig)


# In[13]:


df_plot = df.groupby(['mcname', 'years', 'cname'])    ['epname'].count().reset_index(name='weeks')


# In[ ]:




