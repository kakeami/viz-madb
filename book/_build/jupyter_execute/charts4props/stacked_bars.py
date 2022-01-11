#!/usr/bin/env python
# coding: utf-8

# # Stacked bars

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
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[14]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[15]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[16]:


df = pd.read_csv(PATH_DATA)


# ### 雑誌別・年代別の合計作品数

# In[17]:


col_count = 'cname'


# In[19]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)
df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()


# In[23]:


df_tmp = df_plot.groupby('years')[col_count].sum()


# yearsごとに集計した合計値で割合を出す必要がある．続きは明日から

# 以下のように1変数に対して集計する場合はstacked barsは向いていないと思う．年代横軸，該当数を縦軸で出すべき

# In[ ]:





# In[9]:


df_plot =     df.groupby(['mcname', 'years'])[col_count].    nunique().reset_index()
df_plot['ratio'] =     df_plot[col_count] / df_plot[col_count].sum()
fig = px.bar(
    df_plot, x='col_x', y='ratio', color='mcname',
    barmode='stack')
show_fig(fig)


# ### 雑誌別の合計作者数

# In[ ]:




