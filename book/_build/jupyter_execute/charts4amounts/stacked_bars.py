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


# In[44]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         df['datePublished'].dt.year // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[107]:


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


# In[108]:


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


# In[109]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週（上位20作品）

# In[110]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[111]:


# プロット用に集計
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週数上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# cname，yearsでアップサンプリング
df_plot = resample_df_by_cname_and_years(df_plot)


# In[112]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[113]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='stack', title='作品別・年代別の合計連載週数')
show_fig(fig)


# ### 作者別・年代別の合計連載週数（上位20名）

# In[114]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[115]:


# プロット用に集計
df_plot = df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位20作品を抽出
creators = list(df.value_counts('creator').head(20).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)
# creator，yearsでアップサンプリング
df_plot = resample_df_by_creator_and_years(df_plot)


# In[116]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[117]:


# 作図
fig = px.bar(
    df_plot, x='creator', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='stack', title='作者別・年代別の合計連載週数')
show_fig(fig)

