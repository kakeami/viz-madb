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

# 上記の例では，`df`の`col_x`列をX軸，その度数をY軸に取ったヒストグラムのオブジェクト`fig`を作成します．また，

# ```python
# fig = px.histogram(df, x='col_x', cumulative=True)
# ```

# `cumulative=True`オプションを指定することで，累積ヒストグラムを作図可能です．更に，

# ```python
# fig = px.histogram(df, x='col_x', color='col_stack', barmode='stack')
# ```

# `barmode='stack'`を指定することで，`col_stack`列に関する積み上げヒストグラムを作図可能です．
# もちろん，`cumulative`との組み合わせて使うこともできます．

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


# 平均掲載位置を算出する際の最小連載数
MIN_WEEKS = 5


# In[4]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 掲載位置の分布

# `MIN_WEEKS`以上連載したマンガ作品の平均掲載位置の分布を見てみます．

# In[6]:


df_plot =     df.groupby(['mcname', 'cname', 'creator'])['pageStartPosition']    .agg(['count', 'mean']).reset_index()
df_plot = df_plot[df_plot['count'] >= MIN_WEEKS]    .reset_index(drop=True)


# In[7]:


fig = px.histogram(
    df_plot, x='mean', title='作品ごとの掲載位置')
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='作品数')
show_fig(fig)


# 0.6 - 0.7付近にピークのある分布であることがわかります．

# In[9]:


fig = px.histogram(
    df_plot, x='mean', cumulative=True,
    title='作品ごとの掲載位置')
fig.update_xaxes(title='平均掲載位置')
fig.update_yaxes(title='累積作品数')
show_fig(fig)


# 累積ヒストグラムで見ると，平均掲載位置を低いことがどの程度珍しいかわかります．平均掲載位置が0.5以下の作品（つまり，平均的に雑誌の前半に掲載されることが多い作品）は半分以下です．

# 具体的にはどのような作品の平均掲載位置が低いのでしょうか？

# In[53]:


df_plot.sort_values('mean').reset_index(drop=True).head(10)


# 各雑誌を代表するような先生方の作品であることがわかります．ちなみに`ピクル`は板垣先生のバキシリーズのスピンオフです．

# ### 長期連載作品の掲載位置の分布

# 長期連載した人気作品ほど掲載位置が上位なのでしょうか？
# 
# これを検証するため，[合計連載週数が多い10作品](https://kakeami.github.io/viz-madb/charts4amounts/bars.html#id4)に対して，それぞれ掲載位置の分布を図示します．

# In[79]:


df_tmp =     df_plot.sort_values(['count'], ascending=False, ignore_index=True)    .head(10)
df_tmp


# In[107]:


cnames = df_tmp.sort_values('mean')['cname'].values
for cname in cnames:
    df_c = df[df['cname']==cname].reset_index(drop=True)
    pos = df_c['pageStartPosition'].mean()
    n = df_c.shape[0]
    fig = px.histogram(
        df_c, x='pageStartPosition', nbins=20,
        title=f'{cname}の掲載位置（全{n}話，平均{pos:.3f}）')
    fig.update_xaxes(title='掲載位置')
    fig.update_yaxes(title='話数')
    show_fig(fig)


# 作品によって掲載位置の分布に特徴があることがわかります．巻頭カラー常連の作品もあれば，根強いファンがついて雑誌後半が定位置となった作品もあるようです．

# ### 長期連載作品の話数毎の掲載位置の分布

# では，上記の作品が話数別にどの程度掲載位置が変動したか，定性的に見てみましょう．

# In[105]:


# 話数の区切り
UNIT_EP = 200


# In[108]:


cnames = df_tmp.sort_values('mean')['cname'].values
for cname in cnames:
    df_c = df[df['cname']==cname].reset_index(drop=True)
    df_c['eprange'] = (df_c.index + 1) // UNIT_EP * UNIT_EP
    pos = df_c['pageStartPosition'].mean()
    n = df_c.shape[0]
    fig = px.histogram(
        df_c, x='pageStartPosition', color='eprange',
        barmode='stack', nbins=20,
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        title=f'{cname}の掲載位置（全{n}話，平均{pos:.3f}）')
    fig.update_xaxes(title='掲載位置')
    fig.update_yaxes(title='話数')
    show_fig(fig)


# 定性的にではありますが，`BLEACH`，`銀魂`，`こちら葛飾区亀有公園前派出所`，`ジョジョの奇妙な冒険`に関しては話数が進むほど平均掲載位置が増加（雑誌後方に移動）していることがわかります．
