#!/usr/bin/env python
# coding: utf-8

# # 密度プロット

# ## 概要

# **密度プロット**とは

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.figure_factory.create_distplot()`でDensity plotを作成可能です．

# ```python
# import plotly.figure_factory as ff
# fig = ff.create_distplot(
#     df['x_col'].values.reshape(1, -1), 
#     ['label'], show_hist=False)
# ```

# 上記の例では，`df`の`col_x`列をX軸，その確率密度をY軸にとったDensity plotのオブジェクト`fig`を作成します．
# ただし，`label`のように凡例名を指定する必要があることにご注意ください．

# ```{admonition} `show_hist=False`
# `plotly.figure_factory.create_distplot()`はデフォルト設定でヒストグラムとDensity plotの両方を作図します．Density plotのみ表示したい場合は，`show_hist=False`を指定しましょう．
# ```

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import pandas as pd
import plotly.figure_factory as ff

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


# In[4]:


df = pd.read_csv(PATH_DATA)


# ### 各話のページ数の分布

# In[5]:


df_plot = df.copy()


# In[6]:


fig = ff.create_distplot(
    df_plot['pages'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='各話のページ数')
show_fig(fig)


# In[6]:


fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作品別の合計連載週数')
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 作品別の合計連載週数

# In[7]:


df_plot = df.value_counts('creator').reset_index(name='weeks')
fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作者別の合計連載週数')
show_fig(fig)


# In[8]:


fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作者別の合計連載週数')
fig.update_xaxes(range=[0, 200])
show_fig(fig)


# In[ ]:





# In[ ]:




