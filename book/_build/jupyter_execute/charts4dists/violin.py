#!/usr/bin/env python
# coding: utf-8

# # Violins

# In[ ]:





# 表示範囲変更すること

# In[ ]:





# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[8]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[9]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[10]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[19]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・作品別の合計連載週数

# In[22]:


df_plot =     df.value_counts(['mcname', 'cname']).reset_index(name='weeks')
# X軸の表示順を調整
df_plot = df_plot.sort_values('mcname', ignore_index=True)
fig = px.violin(
    df_plot, x='mcname', y='weeks', 
    title='雑誌別・作品別の合計連載週数')
show_fig(fig)


# In[23]:


fig = px.violin(
    df_plot, x='mcname', y='weeks', 
    title='雑誌別・作品別の合計連載週数')
fig.update_yaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作者別の合計連載週数

# In[24]:


df_plot =     df.value_counts(['mcname', 'creator']).reset_index(name='weeks')
# X軸の表示順を調整
df_plot = df_plot.sort_values('mcname', ignore_index=True)
fig = px.violin(
    df_plot, x='mcname', y='weeks', 
    title='雑誌別・作者別の合計連載週数')
show_fig(fig)


# In[25]:


fig = px.violin(
    df_plot, x='mcname', y='weeks', 
    title='雑誌別・作者別の合計連載週数')
fig.update_yaxes(range=[0, 200])
show_fig(fig)


# In[ ]:




