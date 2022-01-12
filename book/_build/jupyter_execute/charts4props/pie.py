#!/usr/bin/env python
# coding: utf-8

# # Pie chart

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


df = pd.read_csv(PATH_DATA)


# ### 雑誌別の合計作品数

# In[5]:


df_plot =     df.groupby('mcname')['cname'].nunique().reset_index()
df_plot = df_plot.sort_values('mcname', ignore_index=True)
fig = px.pie(
    df_plot, values='cname', names='mcname',
    title='雑誌別の合計作品数')
show_fig(fig)


# ### 雑誌別の合計作者数

# In[6]:


df_plot =     df.groupby('mcname')['creator'].nunique().reset_index()
df_plot = df_plot.sort_values('mcname', ignore_index=True)
fig = px.pie(
    df_plot, values='creator', names='mcname',
    title='雑誌別の合計作者数')
show_fig(fig)


# In[ ]:





# In[ ]:




