#!/usr/bin/env python
# coding: utf-8

# # Grouped bars

# ## 概要
# 
# **Grouped bars**とは，複数の要素をまとめて描画した棒グラフです．

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.bar()`で`barmode='group'`を指定することで描画可能です．

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='group')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とし，`col_group`によって色を塗り分けたGrouped barsを作図可能です．

# ## MADB Labを用いた作図例

# ### 下準備

# In[4]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[5]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[6]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[7]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週数（上位10作品）

# In[33]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
df['years'] = df['datePublished'].dt.year // 10 * 10
df['years'] = df['years'].astype(str)
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')


# In[34]:


# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(10).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# 降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(['order', 'years'], ignore_index=True)


# In[46]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', title='作品別・年代別の合計連載週数')
show_fig(fig)


# ```{note}
# `barmode='group'`の場合，`color`で指定した列の要素に応じてX軸の順序が変わってしまうことがあります．
# ```

# ### 作者別・年代別の合計連載週数（上位10名）

# In[48]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
df['years'] = df['datePublished'].dt.year // 10 * 10
df['years'] = df['years'].astype(str)
df_plot = df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')


# In[49]:


# 連載週数10名を抽出
creators = list(df.value_counts('creator').head(10).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)
# 降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(['order', 'years'], ignore_index=True)


# In[50]:


# 作図
fig = px.bar(
    df_plot, x='creator', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', title='作者別・年代別の合計連載週数')
show_fig(fig)

