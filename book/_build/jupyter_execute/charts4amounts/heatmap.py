#!/usr/bin/env python
# coding: utf-8

# # ヒートマップ

# ## 概要
# 
# **ヒートマップ**とは，例えば下図のように，2変数の組み合わせに対して定まる量的変数を可視化するための手法です．
# 
# ![heatmap](../figs/heatmap.png)

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

# In[21]:


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


# In[18]:


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


# In[43]:


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


# In[5]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週数（上位20作品）

# In[52]:


# 1年単位で区切ったyearsを追加
df = add_years_to_df(df, 1)


# In[53]:


# プロット用に集計
df_plot =     df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# 作図用に空白期間を0埋め
df_plot =     resample_df_by_cname_and_years(df_plot)


# In[54]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[55]:


fig = px.density_heatmap(
    df_plot, x='years', y='cname', z='weeks')
show_fig(fig)


# ### 作者別・年代別の合計連載週数（上位20名）

# In[56]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df, 1)


# In[57]:


# プロット用に集計
df_plot =     df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('creator').head(20).index)
df_plot = df_plot[df_plot['creator'].isin(cnames)].    reset_index(drop=True)
# 作図用に空白期間を0埋め
df_plot =     resample_df_by_creator_and_years(df_plot)


# In[58]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[59]:


fig = px.density_heatmap(
    df_plot, x='years', y='creator', z='weeks')
show_fig(fig)


# 水島新司先生の1970年代の働きぶりは異常ですね…
