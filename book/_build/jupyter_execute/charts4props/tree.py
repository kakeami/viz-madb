#!/usr/bin/env python
# coding: utf-8

# # ツリーマップ

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
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[4]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別の合計作品数

# In[6]:


col_count = 'cname'


# In[7]:


# 1年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
# mcname, yearsで集計
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
df_plot =     df_plot.sort_values(['years', 'mcname'], ignore_index=True)


# In[8]:


fig = px.treemap(
    df_plot, path=[px.Constant('all'), 'mcname', 'years'],
    values=col_count)
fig.update_traces(root_color='lightgrey')
show_fig(fig)


# ### 雑誌別・作品別の合計連載週数

# In[10]:


df_plot =     df.groupby('mcname')['cname'].value_counts().    reset_index(name='weeks')
# 描画用に10週以上の作品に絞る
df_plot = df_plot[df_plot['weeks']>=10].reset_index(drop=True)
fig = px.treemap(
    df_plot, path=[px.Constant('all'), 'mcname', 'cname'],
    values='weeks')
fig.update_traces(root_color='lightgrey')
show_fig(fig)


# ### 雑誌別・年代別の合計作者数

# In[11]:


col_count = 'creator'


# In[12]:


# 1年単位で区切ったyearsを追加
df = add_years_to_df(df, 10)
# mcname, yearsで集計
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
df_plot =     df_plot.sort_values(['years', 'mcname'], ignore_index=True)


# In[13]:


fig = px.treemap(
    df_plot, path=[px.Constant('all'), 'mcname', 'years'],
    values=col_count)
fig.update_traces(root_color='lightgrey')
show_fig(fig)


# ### 雑誌別・作者別の合計連載週数

# In[14]:


df_plot =     df.groupby('mcname')['creator'].value_counts().    reset_index(name='weeks')
# 描画用に10週以上の作者に絞る
df_plot = df_plot[df_plot['weeks']>=10].reset_index(drop=True)
fig = px.treemap(
    df_plot, path=[px.Constant('all'), 'mcname', 'creator'],
    values='weeks')
fig.update_traces(root_color='lightgrey')
show_fig(fig)


# In[ ]:




