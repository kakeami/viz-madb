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

# In[5]:


import pandas as pd
import plotly.figure_factory as ff

import warnings
warnings.filterwarnings('ignore')


# In[6]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[7]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[8]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の合計連載週数

# In[13]:


df_plot = df.value_counts('cname').reset_index(name='weeks')


# In[14]:


fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作品別の合計連載週数')
show_fig(fig)


# In[15]:


fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作品別の合計連載週数

# In[16]:


df_plot =     df.value_counts(['mcname', 'cname']).reset_index(name='weeks')


# In[17]:


df_plot =     df.value_counts(['mcname', 'cname']).reset_index(name='weeks')
# distplot用に中間集計
mcnames = df_plot.mcname.unique()
hist_data = [
    df_plot[df_plot['mcname']==mc]['weeks'].values.reshape(-1)
    for mc in mcnames]
fig = ff.create_distplot(
    hist_data, mcnames, show_hist=False)
fig.update_layout(title_text='雑誌別・作品別の合計連載週数')
show_fig(fig)


# In[18]:


fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 作品別の合計連載週数

# In[19]:


df_plot = df.value_counts('creator').reset_index(name='weeks')
fig = ff.create_distplot(
    df_plot['weeks'].values.reshape(1, -1), 
    ['全雑誌'], show_hist=False)
fig.update_layout(title_text='作者別の合計連載週数')
show_fig(fig)


# In[20]:


fig.update_xaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作者別の合計連載週数

# In[21]:


df_plot =     df.value_counts(['mcname', 'creator']).reset_index(name='weeks')
# distplot用に中間集計
mcnames = df_plot.mcname.unique()
hist_data = [
    df_plot[df_plot['mcname']==mc]['weeks'].values.reshape(-1)
    for mc in mcnames]
fig = ff.create_distplot(
    hist_data, mcnames, show_hist=False)
fig.update_layout(title_text='雑誌別・作者別の合計連載週数')
show_fig(fig)


# In[22]:


fig.update_xaxes(range=[0, 200])
show_fig(fig)


# In[ ]:




