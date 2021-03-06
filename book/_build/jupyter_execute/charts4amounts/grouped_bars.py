#!/usr/bin/env python
# coding: utf-8

# # Grouped bars

# ## 概要
# 
# **Grouped bars**とは，例えば下図のように，複数の要素をまとめて描画した棒グラフです．
# 
# ![grouped_bars](../figs/grouped_bars.png)
# 
# Grouped barsを利用することで，単純な棒グラフでは確認できなかった各要素の内訳を可視化し，その**絶対量**を比較することができます．

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.bar()`で`barmode='group'`を指定することで描画可能です．

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='group')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とし，`col_group`によって色を塗り分けたGrouped barsのオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[11]:


import itertools
import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[12]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[13]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show(renderer=RENDERER)


# In[14]:


def add_years_to_df(df, unit_years=10):
    """unit_years単位で区切ったyears列を追加"""
    df_new = df.copy()
    df_new['years'] =         df['datePublished'].dt.year // unit_years * unit_years
    df_new['years'] = df_new['years'].astype(str)
    return df_new


# In[15]:


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


# In[16]:


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
                 'weeks': 0,})
            df_new = df_new.append(
                s, ignore_index=True)
    return df_new


# In[17]:


df = pd.read_csv(PATH_DATA)


# ### 作品別・年代別の合計連載週数（上位10作品）

# In[18]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[19]:


# プロット用に集計
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
cnames = list(df.value_counts('cname').head(10).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# cname，yearsでアップサンプリング
df_plot = resample_df_by_cname_and_years(df_plot)


# In[20]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[21]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', title='作品別・年代別の合計連載週数')
show_fig(fig)


# ```{admonition} group対象に欠測があるとX軸の順序が自動調整されてしまう
# おそらく`px.bar()`の仕様ですが，`barmode='group'`を選択した際に`color`で指定した列に欠測があると，X軸の順序が変わってしまうことを確認しました．これを回避するため，`resample_df_by_cname_and_years(df_plot)`で欠測を補完しています．以降も同様です．
# ```

# ### 作者別・年代別の合計連載週数（上位10名）

# In[22]:


# datePublishedを10年単位で区切るyears列を追加
df['datePublished'] = pd.to_datetime(df['datePublished'])
# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[23]:


# プロット用に集計
df_plot = df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位10作品を抽出
creators = list(df.value_counts('creator').head(10).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)
# creator，yearsでアップサンプリング
df_plot = resample_df_by_creator_and_years(df_plot)


# In[24]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[25]:


# 作図
fig = px.bar(
    df_plot, x='creator', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', title='作者別・年代別の合計連載週数')
show_fig(fig)

