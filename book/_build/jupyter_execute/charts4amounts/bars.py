#!/usr/bin/env python
# coding: utf-8

# # 棒グラフ

# ## 概要

# **棒グラフ**とは，
# 
# > 縦軸にデータ量をとり、棒の高さでデータの大小を表したグラフです。（縦横が逆の場合もあります。）
# > 　値の高い項目や低い項目を判別するのに有効なグラフで、データの大小が、棒の高低で表されるので、データの大小を比較するのに適しています。
# 
# （「[総務省統計局，なるほど統計学園，棒グラフ](http://www.stat.go.jp/naruhodo/4_graph/shokyu/bou-graph.html)」より抜粋）
# 
# です．

# ![bars](../figs/charts/bars.png)

# 例えば上図は，作品ごとの合計掲載週数を表した棒グラフです．

# ## Plotlyによる作図方法

# Plotlyでは`plotly.express.bar()`で棒グラフを作成可能です．

# ```python
# import plotly.express as px
# fig = px.bar(df, x='col_x', y='col_y')
# ```

# 上記の例では，`df`の`col_x`列を横軸，`col_y`列を縦軸とした棒グラフのオブジェクト`fig`を作成します．また，

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='group')
# ```

# 上記のように`barmode='group'`を指定することで`col_group`でグループ化可能です．さらに，

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='stack')
# ```

# 上記のように`barmode='stack'`を指定することで`col_group`で積み上げた棒グラフを作成可能です．

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
    df_new['years'] =         pd.to_datetime(df['datePublished']).dt.year         // unit_years * unit_years
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


# ### 作品別の掲載週数（上位20作品）

# まずは，作品ごとの掲載週数を見てみましょう．

# In[8]:


df_plot = df.value_counts('cname').reset_index(name='weeks').head(20)
fig = px.bar(df_plot, x='cname', y='weeks', 
             title='作品別の掲載週数')
fig.update_xaxes(title='作品名')
fig.update_yaxes(title='掲載週数')
show_fig(fig)


# 各雑誌・各世代を代表するような作品が並びます．`こちら葛飾区亀有公園前派出所`は流石ですね…．

# ### 作品別・年代別の掲載週数（上位20作品）

# では，上記の作品は**いつ頃**掲載されたものなのでしょうか？ここでは：
# 
# - 集合棒グラフ（グループ化された棒グラフ）
# - 積上げ棒グラフ
# 
# を使って，作品別・年代別の合計掲載週を可視化します．

# In[9]:


# dfに10年区切りの年代情報を追加
df = add_years_to_df(df)


# In[10]:


# プロット用に集計
df_plot = df.groupby('cname')['years'].value_counts().    reset_index(name='weeks')
# 連載週数上位10作品を抽出
cnames = list(df.value_counts('cname').head(20).index)
df_plot = df_plot[df_plot['cname'].isin(cnames)].    reset_index(drop=True)
# cname，yearsでアップサンプリング
df_plot = resample_df_by_cname_and_years(df_plot)


# In[11]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['cname'].apply(
    lambda x: cnames.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[15]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', 
    title='作品別・年代別の合計掲載週数（集合棒グラフ）')
fig.update_xaxes(title='作品名')
fig.update_yaxes(title='合計連載週数')
show_fig(fig)


# 冒頭の棒グラフを年代ごとに分割し，作品ごとに横に並べました．このようなグラフを**集合棒グラフ**と呼びます．
# 
# 作品の掲載年に特徴が顕れており，非常に面白いですね…．`こちら葛飾区亀有公園前派出所`がいかに長期間，コンスタントに掲載されていたかわかります．

# このグラフを観察すると，集合棒グラフには次のような長所があることがわかります：
# 
# - 各作品・各年代の**絶対値**を比較しやすい
#     - 例：1970年代は`ダメおやじ`，1980年代は`こちら葛飾区亀有公園前派出所`が代表的
# - 各作品がどの年代に掲載されたか定性的にわかりやすい
#     - 例：`ダメおやじ`等は1970-1980年代，`MAJOR`は1990-2010年代に掲載された

# 一方で，次のような短所も明らかになりました：
# 
# - 年代の数に比例して凡例の数が増えてしまうため，全体的に棒が細くなり，視認性が悪くなる
# - 年代をまたがった**合計掲載週数**の比較がしづらい

# ```{admonition} group対象に欠測があるとX軸の順序が自動調整されてしまう
# おそらく`px.bar()`の仕様ですが，`barmode='group'`あるいは`barmode='stack'`を選択した際に`color`で指定した列に欠測があると，X軸の順序が変わってしまうことを確認しました．これを回避するため，`resample_df_by_cname_and_years(df_plot)`で欠測を補完しています．以降も同様です．
# ```

# In[14]:


# 作図
fig = px.bar(
    df_plot, x='cname', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='stack', 
    title='作品別・年代別の合計連載週数（積上げ棒グラフ）')
fig.update_xaxes(title='作品名')
fig.update_yaxes(title='合計連載週数')
show_fig(fig)


# こちらは同じ情報を**積上げ棒グラフ**で可視化したものです．
# 積上げ棒グラフは，年代ごとの掲載数を横に並べるのではなく，縦に積上げていることにご注意ください．

# 積上げ棒グラフの長所は：
# 
# - 各作品の年代ごとの**比率**を比較しやすい
# - 各作品の**合計掲載週**を比較しやすい
# 
# です．

# 積上げ棒グラフの短所は：
# 
# - 各作品・各年代の**絶対値**を比較しづらい
# 
# です．
# 
# 積上げ棒グラフの特徴は集合棒グラフと表裏一体です．

# ### 作家別の掲載週数（上位20名）

# 同様に，作家別に掲載週数を可視化してみましょう．

# In[20]:


df_plot = df.value_counts('creator').reset_index(name='weeks').head(20)
fig = px.bar(df_plot, x='creator', y='weeks', title='作者別の掲載週数')
fig.update_xaxes(title='作家名')
fig.update_yaxes(title='掲載週数')
show_fig(fig)


# `こちら葛飾区亀有公園前派出所`の`秋本治`先生が1位と予想しておりましたが，`水島新司`先生が圧倒的でした．

# ### 作家別・年代別の掲載週数（上位20名）

# In[21]:


# 10年単位で区切ったyearsを追加
df = add_years_to_df(df)


# In[22]:


# プロット用に集計
df_plot = df.groupby('creator')['years'].value_counts().    reset_index(name='weeks')
# 連載週刊上位20作品を抽出
creators = list(df.value_counts('creator').head(20).index)
df_plot = df_plot[df_plot['creator'].isin(creators)].    reset_index(drop=True)
# creator，yearsでアップサンプリング
df_plot = resample_df_by_creator_and_years(df_plot)


# In[23]:


# 合計連載週数で降順ソート
df_plot['order'] = df_plot['creator'].apply(
    lambda x: creators.index(x))
df_plot = df_plot.sort_values(
    ['order', 'years'], ignore_index=True)


# In[24]:


# 作図
fig = px.bar(
    df_plot, x='creator', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='group', title='作家別・年代別の掲載週数')
fig.update_xaxes(title='作家名')
fig.update_yaxes(title='掲載週数')
show_fig(fig)


# In[25]:


# 作図
fig = px.bar(
    df_plot, x='creator', y='weeks', color='years',
    color_discrete_sequence= px.colors.diverging.Portland,
    barmode='stack', title='作家別・年代別の掲載週数')
fig.update_xaxes(title='作家名')
fig.update_yaxes(title='掲載週数')
show_fig(fig)


# ## 練習問題
# 
# 1. 掲載週（`datePublished`）数ではなく，作品（`cname`）数が多い作家を可視化してみましょう．掲載週数と比較して言えることはありますか？
# 2. 年代別・作品数別に積上げ棒グラフを作成して，作家毎の特徴を考察してみましょう
