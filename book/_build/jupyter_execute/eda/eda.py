#!/usr/bin/env python
# coding: utf-8

# # そもそもどんなデータを扱うの？

# ここでは，本サイトで分析対象とするデータについて簡単に紹介します．
# なお，このデータは，[MADB Lab v1.0](https://github.com/mediaarts-db/dataset/tree/1.0)を[こちら](https://kakeami.github.io/viz-madb/appendix/preprocess.html)の手順で前処理したものです．

# ## 環境構築

# In[66]:


import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# In[67]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/magazines.csv'


# In[68]:


df = pd.read_csv(PATH_DATA)


# ## 概要

# `df`は
# 
# - 週刊少年ジャンプ
# - 週刊少年サンデー
# - 週刊少年マガジン
# 
# の`1969-11-03`から`2017-07-12`までのすべてのマンガ作品のデータを格納した`DataFrame`です．サイズを見てみます．

# In[69]:


df.shape


# マンガ作品x週を1行に格納するため，約18万行のデータとなっています．列は下記です．

# In[70]:


df.columns


# - `mcname`: 雑誌名
# - `miname`: 雑誌巻号名
# - `cname`: マンガ作品名
# - `epname`: 各話タイトル
# - `creator`: 作者名
# - `pageStart`: 開始ページ
# - `pageEnd`: 終了ページ
# - `numberOfPages`: 雑誌の合計ページ数
# - `datePublished`: 雑誌の発行日
# - `price`: 雑誌の価格
# - `publisher`: 雑誌の発行元
# - `editor`: 雑誌の編集者（編集長）

# 冒頭数行を見てみましょう．

# In[71]:


df.head(3).T


# `pandas`の`describe()`コマンドでざっくり集計してみます．

# In[72]:


df.describe()


# - `pageStart`はすべての行でデータがありますが，それ以外は`NaN`（数値なし）が結構ありそうです
# - `numberOfPages`の最小値，最大値が想定外に広がっていたので，あとで深堀りします
# - `price`も同様です．後で深堀りします

# 次に，`NaN`の数を列ごとに集計します．

# In[74]:


df.isna().sum()


# 特に`epname`と`publisher`の欠損が多いことがわかります．

# ## 各列

# ### `mcname`（雑誌名）

# In[75]:


df['mcname'].value_counts()


# 上記は`mcname`ごとの行数を表します．それぞれ同一期間で集計しましたが，掲載作品数の違いが生じています．

# ### `miname`（雑誌巻号名）

# ユニークな`miname`数を集計します．

# In[76]:


df['miname'].nunique()


# `mcname`（雑誌）ごとに集計した`miname`（雑誌巻号）は：

# In[77]:


df.groupby('mcname')['miname'].nunique()


# ほぼ同数ですが，雑誌によって微妙に巻号数が異なることがわかります．
# 
# 次は，`miname`（雑誌巻号）ごとに`mcname`（マンガ作品）数を集計してみます．

# In[78]:


df.groupby('miname')['cname'].nunique().sort_values().reset_index()


# 1970年付近の黎明期は掲載数が少なめだったようです．また，雑誌によってタイミングはバラバラですが，非常に沢山のマンガを掲載する**外れ値**が存在することもわかります．

# ### `cname`（マンガ作品名）

# ユニークな`cname`（マンガ作品）数を集計します．

# In[79]:


df['cname'].nunique()


# `mcname`（雑誌）ごとに`cname`（マンガ作品）数を集計します．

# In[80]:


df.groupby('mcname')['cname'].nunique()


# ジャンプが圧倒的に多いですね…．試しに`cname`（マンガ作品）ごとに掲載数を集計してみます．

# In[81]:


df_tmp = df[['mcname', 'cname']].value_counts().reset_index()
df_tmp.columns = ['mcname', 'cname', 'counts']
df_tmp


# 連載期間が長い方を見てみると，こち亀，はじめの一歩，名探偵コナンと各雑誌のレジェンドが連なり面白いですね．
# 
# 逆に連載期間が短い方を見てみると，読み切り作品も登録されているようなので，そのあたりも合計マンガ作品数の差に響いているのかもしれません．
# 
# 雑誌ごとに，マンガ作品の連載期間に関して基礎集計します．

# In[82]:


df_tmp.groupby('mcname')['counts'].describe()


# やはりジャンプの平均掲載期間が，他誌と比べて短いことがわかります．

# ### `epname`

# ### `creator`

# ### `pageStart`

# ### `pageEnd`

# ### `numberOfPages`

# ### `datePublished`

# ### `publisher`

# ### `editor`
