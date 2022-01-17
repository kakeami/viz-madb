#!/usr/bin/env python
# coding: utf-8

# # Scatter plot

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


# ### 前処理

# 

# In[16]:


df[['pageStart', 'pageEnd']].isna().sum()


# In[12]:


df_tmp = df.groupby('miname')['pageEnd'].max().reset_index()


# In[14]:


fig = px.histogram(df_tmp, x='pageEnd')
show_fig(fig)


# ### 雑誌別・作品別の平均掲載順位と連載週数の関係

# In[ ]:


df


# In[10]:


df.groupby('miname')['pageStart'].max().describe()


# In[ ]:




