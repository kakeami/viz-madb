#!/usr/bin/env python
# coding: utf-8

# # Heatmap

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


# In[5]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         df['datePublished'].dt.year // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[4]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週数（上位20作品）

# In[13]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[14]:


# プロット用に集計
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)


# In[15]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[17]:


fig = px.density_heatmap(
    df_plot, x='cname', y='years', z='weeks')
show_fig(fig)


# ### 作者別・年代別の合計連載週数（上位20名）

# In[18]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[19]:


# プロット用に集計
df_plot = df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
creators = list(df.value_counts('creator').head(20).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)


# In[20]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[21]:


fig = px.density_heatmap(
    df_plot, x='creator', y='years', z='weeks')
show_fig(fig)

