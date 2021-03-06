#!/usr/bin/env python
# coding: utf-8

# # Cumulative density

# ## 概要

# **Cumulative density**とは

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.histogram()`でCumulative densityを作成可能です．

# ```python
# import plotly.express as px
# fig = px.histogram(df, x='col_x', cumulative=True)
# ```

# 上記の例では，`df`の`col_x`列をX軸，その度数をY軸に取ったCumulative densityのオブジェクト`fig`を作成します．

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


# ### 作品別の合計連載週数

# In[5]:


df_plot = df.value_counts('cname').reset_index(name='weeks')


# In[6]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作品別の合計連載週数', cumulative=True)
show_fig(fig)


# In[7]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作品別の合計連載週数', cumulative=True)
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 作者別の合計連載週数

# In[8]:


df_plot = df.value_counts('creator').reset_index(name='weeks')


# In[9]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作者別の合計連載週数', cumulative=True)
show_fig(fig)


# In[10]:


fig = px.histogram(
    df_plot, x='weeks', nbins=100,
    title='作者別の合計連載週数', cumulative=True)
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# In[ ]:




