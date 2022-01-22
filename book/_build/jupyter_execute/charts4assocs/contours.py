#!/usr/bin/env python
# coding: utf-8

# # 等高線プロット

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
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[3]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別の平均掲載位置と掲載週数

# In[6]:


df_plot =     df.groupby('cname')['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns = ['cname', 'weeks', 'position']
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[8]:


fig = px.density_contour(
    df_plot, x='position', y='weeks',
    title='作品別の平均掲載位置と掲載週数')
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='掲載週数')
# 色を塗りつぶし，等高線にラベルを追加
fig.update_traces(
    contours_coloring="fill", 
    contours_showlabels = True)
show_fig(fig)


# In[9]:


fig.update_yaxes(range=[0, 200])
show_fig(fig)


# ### 雑誌別・作品別の平均掲載位置と連載週数

# In[10]:


df_plot =     df.groupby(['mcname', 'cname'])['pageStartPosition'].    agg(['count', 'mean']).reset_index()
df_plot.columns =     ['mcname', 'cname', 'weeks', 'position']
df_plot = df_plot.sort_values(
    'mcname', ignore_index=True)
df_plot =     df_plot[df_plot['weeks'] >= MIN_WEEKS].reset_index(drop=True)


# In[11]:


fig = px.density_contour(
    df_plot, x='position', y='weeks', color='mcname',
    title='雑誌別・作品別の平均掲載位置と掲載週数')
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='掲載週数')
fig.update_yaxes(range=[0, 200])
show_fig(fig)


# In[12]:


fig = px.density_contour(
    df_plot, x='position', y='weeks',
    facet_col='mcname', facet_col_wrap=2,
    title='雑誌別・作品別の平均掲載位置と掲載週数')
fig.for_each_annotation(
    lambda a: a.update(text=a.text.split("=")[-1]))
# 色を塗りつぶし，等高線にラベルを追加
fig.update_traces(
    contours_coloring="fill", 
    contours_showlabels = True)
fig.update_yaxes(range=[0, 200])
# カラーバーの表示が壊れるので非表示
fig.update_traces(showscale=False)
show_fig(fig)


# In[ ]:





# In[ ]:




