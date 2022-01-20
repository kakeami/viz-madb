#!/usr/bin/env python
# coding: utf-8

# # 折れ線グラフ

# ## 概要

# ## Plotlyによる作図方法

# ## MADB Labを用いた作図例

# In[2]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[3]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[4]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[5]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[6]:


df = pd.read_csv(PATH_DATA)


# ## 作品別の掲載位置

# In[30]:


N_CNAMES = 5


# In[34]:


mcnames = sorted(df['mcname'].unique())
for mcname in mcnames:
    df_tmp = df[df['mcname']==mcname].reset_index(drop=True)
    df_cname =         df_tmp.value_counts('cname').reset_index(name='weeks')
    df_cname =         df_cname.sort_values(
            'weeks', ascending=False, ignore_index=True)
    cnames = df_cname['cname'][:N_CNAME].values
    df_plot = df_tmp[df_tmp['cname'].isin(cnames)].        reset_index(drop=True)
    fig = px.line(
        df_plot, x='datePublished', y='pageStartPosition',
        color='cname', title=f'{mcname}の長期連載作品')
    show_fig(fig)


# In[33]:


cnames


# In[28]:


df_cname


# In[23]:


df_tmp =     df.value_counts('cname').reset_index(name='weeks')
cnames = df_tmp['cname'][:5].values
df_plot =     df[df['cname'].isin(cnames)].reset_index(drop=True)
df_plot['datePublished'] = pd.to_datetime(
    df_plot['datePublished'])


# In[24]:


fig = px.line(
    df_plot, x='datePublished', y='pageStartPosition',
    color='cname')
show_fig(fig)


# In[ ]:




