#!/usr/bin/env python
# coding: utf-8

# # Stacked bars

# ## 概要
# 
# **Stacked bars**（積み上げ棒グラフ）とは，例えば下図のように，棒グラフの各要素の内訳を色分けした棒グラフです．
# 
# Stacked barsを利用することで，単純な棒グラフでは確認できなかった各要素の内訳を可視化し，その**比率**を比較することができます．
# 
# ```{admonition} Stacked barsとGrouped barsの使い分け
# 私は，要素の内訳の比率に注目して欲しい場合はStacked barsを，絶対量を横並びで比較して欲しい場合はGrouped barsを利用することにしています．
# ```

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.bar()`で`barmode='stack'`を指定することで作図可能です．

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='stack')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とし，`col_group`によって色を塗り分けたStacked barsのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[3]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[4]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[5]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.show(renderer=RENDERER)


# In[6]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週（上位20作品）

# In[7]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
df['years'] = df['datePublished'].dt.year // 10 * 10
df['years'] = df['years'].astype(str)
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')


# In[30]:


# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# 降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(['order', 'years'], ignore_index=True)


# In[31]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='stack', title='作品別・年代別の合計連載週数')
show_fig(fig)


# In[32]:


import itertools


# In[33]:


df_plot[df_plot['years']==years]


# In[28]:


yearss = df_plot['years'].unique()
for cname, years in itertools.product(
        cnames, yearss):
    df_tmp = df_plot[
        (df_plot['cname']==cname)&\
        (df_plot['years']==years)
    ]
    if df_tmp.shape[0] == 0:
        df_plot = df_plot.append( 
            [cname, years, 0, cnames.index(cname)])


# In[29]:


df_plot


# In[17]:


cnames.index()


# In[18]:


cnames


# In[ ]:




