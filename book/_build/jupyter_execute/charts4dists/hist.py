#!/usr/bin/env python
# coding: utf-8

# # Histogram

# データのばらつきを見たいときは，ヒストグラムを利用してみると良いでしょう．

# ## 環境構築

# In[1]:


# Notebook初期設定
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

import warnings
warnings.filterwarnings('ignore')


# In[2]:


import os
import pandas as pd
import plotly.express as px


# In[11]:


DIR_IN = '../../data/preprocess/out'
FN_MG = 'magazines.csv'


# In[12]:


RENDERER = 'plotly_mimetype+notebook'


# ## 関数

# In[13]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# ## データの読み込み

# In[14]:


df = pd.read_csv(os.path.join(DIR_IN, FN_MG))


# In[15]:


df.head(2).T


# ## ページ数の分布を見る

# In[16]:


df_tmp =     df.groupby('datePublished')['numberOfPages'].first().reset_index()
fig = px.histogram(df_tmp, x='numberOfPages')
show_fig(fig)


# In[ ]:




