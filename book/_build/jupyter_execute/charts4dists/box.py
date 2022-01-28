#!/usr/bin/env python
# coding: utf-8

# # 箱ひげ図

# ## 概要

# **箱ひげ図**とは，
# 
# > 統計学において，ばらつきのあるデータを見やすく表示するための図式。品質管理をはじめさまざまな分野で利用される。通常は，最小値，第1四分位数，中央値（第2四分位数），第3四分位数，最大値を，箱と線（ひげ）を用いて一つの図に表すが，平均値（→算術平均）をあわせて図示することもある。あるデータにおいて，最大値から最小値を引いた値をデータ分布の範囲（レンジ）という。データ分布の範囲は，箱ひげ図ではひげまで含めた図の長さとして表されるが，これは極端にはずれた値の影響を受けやすい。データによっては，第3四分位数から第1四分位数を引いた四分位範囲を用いることで，より的確に散らばり具合を表すことができる。四分位範囲を箱として表す箱ひげ図は，データの分布の様子を視覚化するのに有用である。
# 
# （[ブリタニカ国際大百科事典 小項目事典]より抜粋）
# 
# です．分布の細かい情報が削ぎ落とされてしまいますが，複数の分布を比較する際は非常に便利です．

# ![](../figs/charts/box.png)

# 例えば上図は，作品ごとの掲載位置の分布を示した箱ひげ図です．
# [ヒストグラム](https://kakeami.github.io/viz-madb/charts4dists/hist.html)
# や
# [密度プロット](https://kakeami.github.io/viz-madb/charts4dists/density.html)
# と異なり，各作品の分布形状はわからなくなってしまいましたが，直感的な比較が可能になりました．

# ## Plotlyによる作図方法

# Plotlyにおいては，`plotly.express.box()`関数で箱ひげ図を作図できます．

# ```python
# import plotly.express as px
# fig = px.box(df, x='col_x', y='col_y')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸に取った箱ひげ図のオブジェクト`fig`を作成します．

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


# ### 長期連載作品の掲載位置の分布

# In[6]:


df_tmp =     df.groupby('cname')['pageStartPosition']    .agg(['count', 'mean']).reset_index()
df_tmp =     df_tmp.sort_values('count', ascending=False, ignore_index=True)    .head(10)
cname2position = df_tmp.groupby('cname')['mean'].first().to_dict()


# In[7]:


df_plot = df[df['cname'].isin(list(cname2position.keys()))]    .reset_index(drop=True)
df_plot['position'] = df_plot['cname'].apply(
    lambda x: cname2position[x])
df_plot = df_plot.sort_values('position', ignore_index=True)


# In[9]:


fig = px.box(
    df_plot, x='cname', y='pageStartPosition',
    title='長期連載作品の掲載位置')
fig.update_xaxes(title='作品名')
fig.update_yaxes(title='掲載位置')
show_fig(fig)


# ヒストグラムや密度プロットより簡易に，作品ごとの掲載位置の分布を比較しやすくなりました．一方で，サンプル数や分布形状の情報が削ぎ落とされていることにご注意ください．

# ### 長期連載作品の話数毎の掲載位置の分布

# In[10]:


# 話数の区切り
UNIT_EP = 200


# In[47]:


cnames = df_plot['cname'].unique()
for cname in cnames:
    df_c = df_plot[df_plot['cname']==cname].reset_index(drop=True)
    df_c['eprange'] = (df_c.index + 1) // UNIT_EP * UNIT_EP
    df_c['eprange'] = df_c['eprange'].apply(
        lambda x: f'{x}話以降')
    fig = px.box(
        df_c, x='eprange', y='pageStartPosition',
        title=f'{cname}の掲載位置')
    fig.update_xaxes(title='話数')
    fig.update_yaxes(title='掲載位置')
    show_fig(fig)


# こちらに関しても，比較が容易になった一方で，細かな分布形状の情報が失われていることがわかります．
