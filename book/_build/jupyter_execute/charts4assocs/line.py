#!/usr/bin/env python
# coding: utf-8

# # 折れ線グラフ（1変数）

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


# In[5]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[6]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    # 凡例でグラフが潰れないよう調整
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[7]:


df = pd.read_csv(PATH_DATA)


# ### 長期連載作品の掲載位置の推移

# In[8]:


df_tmp =     df.groupby('cname')['pageStartPosition']    .agg(['count', 'mean']).reset_index()
df_tmp =     df_tmp.sort_values('count', ascending=False, ignore_index=True)    .head(10)
cname2position = df_tmp.groupby('cname')['mean'].first().to_dict()


# In[10]:


df_plot = df[df['cname'].isin(list(cname2position.keys()))]    .reset_index(drop=True)
df_plot['position'] = df_plot['cname'].apply(
    lambda x: cname2position[x])
df_plot['datePublished'] = pd.to_datetime(df_plot['datePublished'])
df_plot =     df_plot.sort_values(['position', 'datePublished'], ignore_index=True)


# In[19]:


cnames = df_plot['cname'].unique()
for cname in cnames:
    df_c = df_plot[df_plot['cname']==cname].reset_index(drop=True)
    fig = px.line(
        df_c, x='datePublished', y='pageStartPosition',
        hover_data=['epname'], title=f'{cname}の掲載位置の推移')
    fig.update_traces(
        mode='lines+markers',
        marker=dict(line_width=1, size=10))
    fig.update_xaxes(title='発売日')
    fig.update_yaxes(title='掲載位置')
    show_fig(fig)

