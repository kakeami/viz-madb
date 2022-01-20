#!/usr/bin/env python
# coding: utf-8

# # 2次元ヒストグラム

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[15]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[16]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[17]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[18]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[19]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と連載週数

# In[20]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[23]:


fig = px.density_heatmap(
    df_plot, x='position', y='weeks')
show_fig(fig)


# In[24]:


fig.update_yaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数

# In[10]:


df_plot =     df.groupby(['mcname', 'cname'])['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns =     ['mcname', 'cname', 'weeks', 'position']
df_plot = df_plot.sort_values(
    'mcname', ignore_index=True)
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[13]:


fig = px.density_heatmap(
    df_plot, x='position', y='weeks',
    facet_col='mcname',
    facet_col_wrap=2)
fig.for_each_annotation(
    lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_yaxes(range=[0, 200])
show_fig(fig)

