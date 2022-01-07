#!/usr/bin/env python
# coding: utf-8

# # Density plot

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# ### 下準備

# In[5]:


import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

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


# In[4]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の合計連載週数

# In[18]:


df_plot = df.value_counts('cname').reset_index(name='weeks')
fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作品別の合計連載週数')
show_fig(fig)


# ### 作品別の合計連載週数

# In[ ]:




