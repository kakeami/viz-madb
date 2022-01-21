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

# :::{admonition} `show_hist=False`
# `plotly.figure_factory.create_distplot()`はデフォルト設定でヒストグラムとDensity plotの両方を作図します．Density plotのみ表示したい場合は，`show_hist=False`を指定しましょう．
# :::

# ## MADB Labを用いた作図例

# ### 下準備

# In[54]:


import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[6]:


# 平均掲載位置を算出する際の最小連載数
MIN_WEEKS = 5


# In[46]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'right',
        'x': 0.99, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[47]:


df = pd.read_csv(PATH_DATA)


# ### 掲載位置の分布

# In[48]:


df_plot =     df.groupby(['mcname', 'cname', 'creator'])['pageStartPosition']    .agg(['count', 'mean']).reset_index()
df_plot = df_plot[df_plot['count'] >= MIN_WEEKS]    .reset_index(drop=True)


# In[49]:


fig = ff.create_distplot(
    [df_plot['mean'].values], ['全作品'],
    show_hist=False)
show_fig(fig)


# ヒストグラムで図示するよりも滑らかに分布を図示できていることがわかります．

# ### 長期連載作品の掲載位置の分布

# 合計連載週数が多い5作品に対して，同様に分布を図示してみましょう．

# In[62]:


df_tmp =     df_plot.sort_values(['count'], ascending=False, ignore_index=True)    .head(10)
df_tmp


# In[63]:


cnames = df_tmp.sort_values('mean')['cname'].values
data = [
    df[df['cname']==cname].reset_index(drop=True)\
    ['pageStartPosition'] for cname in cnames]


# In[66]:


fig = ff.create_distplot(
    data, cnames, show_hist=False,
    colors= px.colors.sequential.Plasma_r)
fig.update_layout(hovermode='x unified', height=600)
show_fig(fig)


# ヒストグラムと異なり，複数の凡例を同時に表示できるため，比較が楽です．

# ### 長期連載作品の話数毎の掲載位置の分布

# In[67]:


# 話数の区切り
UNIT_EP = 200


# In[75]:


cnames = df_tmp.sort_values('mean')['cname'].values
for cname in cnames:
    df_c = df[df['cname']==cname].reset_index(drop=True)
    df_c['eprange'] = (df_c.index + 1) // UNIT_EP * UNIT_EP
    eps = sorted(df_c['eprange'].unique())
    data = [
        df_c[df_c['eprange']==e]['pageStartPosition']
        for e in eps]
    labels = [f'{e}話以降' for e in eps]
    fig = ff.create_distplot(
        data, labels, show_hist=False,
        colors= px.colors.sequential.Plasma_r)
    fig.update_layout(
        hovermode='x unified', height=500,
        title_text=f'{cname}の掲載位置')
    show_fig(fig)


# 積み上げヒストグラムを用いた場合より，話数による掲載位置の推移がわかりやすくなりました．
