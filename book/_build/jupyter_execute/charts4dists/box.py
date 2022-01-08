#!/usr/bin/env python
# coding: utf-8

# # Box plot

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[2]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[3]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・作品別の合計連載週数 

# In[12]:


df_plot =     df.value_counts(['mcname', 'cname']).reset_index(name='weeks')
fig = px.box(df_plot, x='mcname', y='weeks')
show_fig(fig)


# ### 作者別の合計連載週数

# In[ ]:




