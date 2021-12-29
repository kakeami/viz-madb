#!/usr/bin/env python
# coding: utf-8

# # ヒストグラム

# データのばらつきを見たい場合は，ヒストグラムを利用します．

# ## 環境構築

# In[2]:


# Notebook初期設定
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

import warnings
warnings.filterwarnings('ignore')


# In[9]:


import os
import pandas as pd
import plotly.express as px


# In[6]:


DIR_IN = '../data/preprocess/out'
FN_WJ = 'wj.csv'


# In[7]:


RENDERER = 'plotly_mimetype+notebook'


# ## 関数

# In[12]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# ## データの読み込み

# In[10]:


df = pd.read_csv(os.path.join(DIR_IN, FN_WJ))


# In[14]:


df.head(2).T


# ## 掲載作品数の分布

# 掲載作品数の分布を見てみます．

# In[34]:


df_tmp = df.value_counts('datePublished').reset_index()
df_tmp.columns = ['date', '掲載作品数']
fig = px.histogram(df_tmp, x='掲載作品数')
show_fig(fig)


# - 最小で12，最大で57の漫画作品が掲載されており，
# - 掲載数16および20にピークがある
# 
# ことがわかります．

# 掲載作品数が少ないのは，

# In[37]:


df_tmp.sort_values('掲載作品数').head()


# 過去の巻号が多そうです．そこで，subplotを使って年代ごとにヒストグラムを描いてみます．

# In[48]:


df_tmp['year'] = pd.to_datetime(df_tmp['date']).dt.year
df_tmp['year_10'] = df_tmp['year'] // 10 * 10 # 10年刻み
year_10s = sorted(df_tmp['year_10'].unique())


# In[ ]:


fig = px.histogram(df_tmp, x='


# In[45]:


df_tmp['year'] // 10 * 10


# ## ページ数の分布

# 合計ページ数の分布を見てみます．

# In[26]:


df_tmp =     df.groupby('datePublished')['numberOfPages'].first().reset_index()
fig = px.histogram(df_tmp, x='numberOfPages')
show_fig(fig)


# In[ ]:




