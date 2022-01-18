#!/usr/bin/env python
# coding: utf-8

# # ヒストグラム

# ## 概要

# **ヒストグラム**とは，例えば下図のように，

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.histogram()`でヒストグラムを作成可能です．

# ```python
# import plotly.express as px
# fig = px.histogram(df, x='col_x')
# ```

# 上記の例では，`df`の`col_x`列をX軸，その度数をY軸に取ったヒストグラムのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 各話のページ数の分布

# In[6]:


fig = px.histogram(
    df, x='pages', title='各話のページ数')
show_fig(fig)


# これでは少し見づらいので，表示範囲を`fig.update_xaxis()`で変更します．

# In[7]:


fig.update_xaxes(range=[0, 50])
show_fig(fig)


# ### 雑誌別の各話のページ数の分布

# In[8]:


df = df.sort_values('mcname', ignore_index=True)
fig = px.histogram(
    df, x='pages', color='mcname', barmode='stack',
    color_discrete_sequence= px.colors.diverging.Portland,
    title='雑誌別の各話のページ数')
fig.update_xaxes(range=[0, 50])
show_fig(fig)


# In[9]:


for mcname in sorted(df['mcname'].unique()):
    df_tmp = df[df['mcname']==mcname].reset_index(drop=True)
    fig = px.histogram(
        df_tmp, x='pages', title=f'{mcname}の各話のページ数',)
    fig.update_xaxes(range=[0, 50])
    show_fig(fig)


# In[ ]:




