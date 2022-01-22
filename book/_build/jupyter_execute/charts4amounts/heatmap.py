#!/usr/bin/env python
# coding: utf-8

# # ヒートマップ

# ## 概要
# 
# **ヒートマップ**とは，二変数の組み合わせに対して定まる量的変数を可視化するための手法です．例えば下図のようなものです．
# 
# ![heatmap](../figs/charts/heatmap.png)

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.density_heatmap()`を用いて作図できます．

# ```python
# import plotly.express as px
# fig = px.density_heatmap(
#     df, x='col_x', y='col_y', z='col_z')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とし，`col_z`の量に応じて色を塗り分けたヒートマップのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[1]:


import itertools
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


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[4]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         pd.to_datetime(df['datePublished'])        .dt.year // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[5]:


def resample_df_by_cname_and_years(df):
    """cnameとyearsのすべての組み合わせが存在するように0埋め
    この処理を実施しないと作図時にX軸方向の順序が変わってしまう"""
    df_new = df.copy()
    yearss = df['years'].unique()
    cnames = df['cname'].unique()
    for cname, years in itertools.product(cnames, yearss):
        df_tmp = df_new[
            (df_new['cname'] == cname)&\
            (df_new['years'] == years)]
        if df_tmp.shape[0] == 0:
            s = pd.Series(
                {'cname': cname,
                 'years': years,
                 'weeks': 0,},
                index=df_tmp.columns)
            df_new = df_new.append(
                s, ignore_index=True)
    return df_new


# In[6]:


def resample_df_by_creator_and_years(df):
    """creatorとyearsのすべての組み合わせが存在するように0埋め
    この処理を実施しないと作図時にX軸方向の順序が変わってしまう"""
    df_new = df.copy()
    yearss = df['years'].unique()
    creators = df['creator'].unique()
    for creator, years in itertools.product(creators, yearss):
        df_tmp = df_new[
            (df_new['creator'] == creator)&\
            (df_new['years'] == years)]
        if df_tmp.shape[0] == 0:
            s = pd.Series(
                {'creator': creator,
                 'years': years,
                 'weeks': 0,},
                index=df_tmp.columns)
            df_new = df_new.append(
                s, ignore_index=True)
    return df_new


# In[7]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の掲載週数（上位20作品）

# まずは，棒グラフと同様に作品別・年代別の掲載週数を確認してみましょう．
# 
# ただし，ここでは細かい粒度（1年区切り）で年代を集計している点にご注意ください．

# In[8]:


# 1年単位で区切ったyearsを追加
df = add_years_to_df(df, 1)


# In[9]:


# プロット用に集計
df_plot =     df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# 作図用に空白期間を0埋め
df_plot =     resample_df_by_cname_and_years(df_plot)


# In[10]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[11]:


fig = px.density_heatmap(
    df_plot, x='years', y='cname', z='weeks',
    title='作品別・年代別の合計掲載週数', height=500)
fig.update_xaxes(title='掲載年')
fig.update_yaxes(title='作品名')
show_fig(fig)


# 各作品の栄枯盛衰がわかり，歴史資料集の冒頭の年表のようです．

# ### 作家別・年代別の合計掲載週数（上位20名）

# In[13]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 1)


# In[14]:


# プロット用に集計
df_plot =     df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
creators = list(df.value_counts('creator').head(20).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)
# 作図用に空白期間を0埋め
df_plot =     resample_df_by_creator_and_years(df_plot)


# In[15]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[16]:


fig = px.density_heatmap(
    df_plot, x='years', y='creator', z='weeks',
    title='作家別・年代別の合計掲載週数', height=500)
fig.update_xaxes(title='掲載年')
fig.update_yaxes(title='作家名')
show_fig(fig)


# `水島新司`先生（特に1976年）の働きぶりが常軌を逸しています．一年間は約52週しかないはずなのに，**合計143話**を週刊雑誌に掲載するとは一体…？

# ### 作家別・作品別・年代別の合計掲載週数

# 上記の作家に対して，作品別の掲載数を可視化します．特に`水島新司`先生は必見です．

# In[17]:


df_plot = df[df['creator'].isin(creators)].reset_index(drop=True)
df_plot =     df_plot.groupby(['creator', 'cname'])['years'].value_counts()    .reset_index(name='weeks')


# In[18]:


for creator in creators:
    df_c = df_plot[df_plot['creator']==creator]        .reset_index(drop=True)
    df_c = df_c.sort_values('years', ignore_index=True)
    n_works = df_c['cname'].nunique()
    fig = px.density_heatmap(
        df_c, x='years', y='cname', z='weeks',
        height=max(n_works*20, 300),
        title=f'{creator}先生の掲載履歴')
    fig.update_xaxes(title='掲載年')
    fig.update_yaxes(title='作品名')
    show_fig(fig)


# `水島新司`先生の作品数が多いのは，`野球狂の詩`として連載を開始する前に不定期（とは言えほぼ月1本ペース）で掲載されていた短編が多数存在するためと思われます．繰返しですが，週刊連載を2本掛け持ちしながら月イチで短編を描くってどういうことでしょうか…？

# また，複数本の代表作を持つ先生方が，連載の合間に短編作品を掲載していることがわかります．

# ## 練習問題

# 1. 一定以上の長期連載作品（例えば100週以上）に絞り，雑誌ごとに掲載作品の栄枯盛衰を可視化してみましょう
#     - 横軸：年代
#     - 縦軸：作品名
#     - 色：掲載週数
# 2. 一定以下の短期連載作品（例えば10週以下）数を掲載年・雑誌ごとに集計し，週刊連載の厳しさを可視化してみましょう
#     - 横軸：年代
#     - 縦軸：雑誌
#     - 色：短期連載作品数
