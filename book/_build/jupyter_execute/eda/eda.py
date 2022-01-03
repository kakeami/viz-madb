#!/usr/bin/env python
# coding: utf-8

# # そもそもどんなデータを扱うの？

# ここでは，本サイトで分析対象とするデータについて簡単に紹介し，基礎分析を実施します．なお，このデータは[MADB Labでv1.0として公開されているもの](https://github.com/mediaarts-db/dataset/tree/1.0)に[こちらの前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html)を実施したものです．

# ## 環境構築

# In[147]:


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
# - 週刊少年チャンピオン
# 
# の`1970-08-02`から`2017-07-06`までのすべての掲載作品のデータを格納した`DataFrame`です．
# まずはサイズを見てみましょう．

# In[69]:


df.shape


# 各週の掲載作品を一行ずつ格納しているため，合計で約18万行程度の規模になります．
# 以下に，各列の構成を示します．

# In[70]:


df.columns


# - `mcname`: 雑誌名（**M**gazine **C**ollection **NAME**）
# - `miname`: 雑誌巻号名（**M**agazine **I**tem **NAME**）
# - `cname`: マンガ作品名（**C**omic **NAME**）
# - `epname`: 各話タイトル（**EP**isode **NAME**）
# - `creator`: 作者名
# - `pageStart`: 開始ページ
# - `pageEnd`: 終了ページ
# - `numberOfPages`: 雑誌の合計ページ数
# - `datePublished`: 雑誌の発行日
# - `price`: 雑誌の価格
# - `publisher`: 雑誌の出版社
# - `editor`: 雑誌の編集者（編集長）

# 冒頭数行を見て，データのイメージを掴んでみましょう．

# In[71]:


df.head(3).T


# `pandas`の`describe()`コマンドでざっくり集計してみます．

# In[72]:


df.describe()


# - `pageStart`はすべての行でデータがありますが，それ以外は`NaN`（数値なし）が結構ありそうです
# - `numberOfPages`の最小値，最大値が想定外に広がっていたので，あとで深堀りします
# - `price`も同様です．後で深堀りします

# 次に，`NaN`の数を列ごとに集計します．

# In[148]:


df.isna().sum().reset_index()


# ```{margin} 前処理が原因の欠測
# `numberOfPages`，`price`に関しては，想定外のパターンのデータを`NaN`に変換するよう[前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html#cm102)を施しています．
# ```
# 
# 特に`epname`と`publisher`の欠損が多いことがわかります．

# ## 列ごとの基礎分析

# ### `mcname`（雑誌名）

# In[149]:


df['mcname'].value_counts().reset_index()


# 上記は`mcname`ごとの行数を表します．それぞれ同一期間で集計しましたが，掲載作品数の違いが生じています．

# ### `miname`（雑誌巻号名）

# ユニークな`miname`数を集計します．

# In[76]:


df['miname'].nunique()


# `mcname`（雑誌）ごとに集計した`miname`（雑誌巻号）は：

# In[150]:


df.groupby('mcname')['miname'].nunique().reset_index()


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

# In[151]:


df.groupby('mcname')['cname'].nunique().reset_index()


# ジャンプが圧倒的に多いですね…．試しに`cname`（マンガ作品）ごとに掲載数を集計してみます．

# In[81]:


df_tmp = df[['mcname', 'cname']].value_counts().reset_index()
df_tmp.columns = ['mcname', 'cname', 'counts']
df_tmp


# ```{margin} あれ，あの長編作品は…？
# シーズンごとに作品名が変わっているシリーズ作品（ドカベン，刃牙，浦鉄，ジョジョ等）は，それぞれ別作品として集計されていることにご注意ください．
# ```
# 
# 連載期間が長いものを見てみましょう．こち亀，はじめの一歩，名探偵コナン，ONEPIECE，MAJORと各雑誌のレジェンドが連なります．
# 一方で，連載期間が短いものの中には，企画ものや読み切りが存在するようです．
# 
# 雑誌ごとに，マンガ作品の連載期間に関して基礎集計します．

# In[82]:


df_tmp.groupby('mcname')['counts'].describe()


# やはりジャンプの平均連載期間が，他誌と比べて短いことがわかります．

# ### `epname`（各話タイトル）

# ユニークな`epname`（各話タイトル）数を集計します．

# In[85]:


df['epname'].nunique()


# 意外と重複しているようです．集計してみます．

# In[87]:


df['epname'].value_counts().reset_index()


# プロ野球編ってことは…．

# In[88]:


df[df['epname']=='プロ野球編']['cname'].value_counts().reset_index()


# やっぱりドカベンですね！ドカベンってもしかして**〇〇編**の粒度でしかタイトルをつけないのでしょうか…？ドカベンの`epname`を集計してみます．

# In[92]:


df[df['cname']=='ドカベン']['epname'].value_counts().reset_index()


# In[93]:


df[df['cname']=='ドカベン']['epname'].isna().sum()


# プロ野球編以外のドカベンの各話タイトルは欠測しているため，これ以上のことはわからなそうです．

# ### `creator`（作者）

# `df`に存在する`creator`（作者）数を集計します．

# In[96]:


df['creator'].nunique()


# 合計作品数が多い`creator`を調べてみます．

# In[98]:


df['creator'].value_counts().reset_index().head(10)


# メンツが強すぎます…．
# 個人的にはこち亀の`秋本治`先生が一番かなと予想していましたが，`水島新司`先生が圧倒的でした．
# 
# ちなみに，こち亀の`creator`を集計すると以下のようになります．

# In[103]:


df[df['cname']=='こちら葛飾区亀有公園前派出所']['creator'].value_counts().reset_index()


# `秋本治`先生は，デビュー時`山止たつひこ`というペンネームを使っていました．
# 
# （この101話分を足しても全然追いつかない`水島新司`先生がすごすぎますが…）

# ### `pageStart`（開始ページ）

# `pageStart`（開始ページ）について`describe()`で基礎集計すると，以下のようになります．

# In[111]:


df['pageStart'].describe().reset_index()


# 異常に大きいものがあることがわかります．
# 試しに`pageStart`が`numberOfPage`より大きいものを抜き出すと：

# In[115]:


df[df['pageStart'] > df['numberOfPages']].sort_values('pageStart')[
    ['miname', 'cname', 'epname', 'pageStart', 'pageEnd', 
     'numberOfPages']]


# となります．最後の2つは明らかに`startPage`がおかしい気がするので，分析をすすめる際は注意が必要そうです．

# ### `pageEnd`（終了ページ）

# `pageEnd`（終了ページ）について`describe()`で基礎集計すると，以下のようになります．

# In[113]:


df['pageEnd'].describe().reset_index()


# `pageEnd`にも異常に大きいものが存在するようです．
# 試しに`pageEnd`が`numberOfPage`より大きいものを抜き出すと：

# In[117]:


df[df['pageEnd'] > df['numberOfPages']].sort_values('pageEnd')[
    ['miname', 'cname', 'epname', 'pageStart', 'pageEnd', 
     'numberOfPages']]


# 最後の二つは明らかにおかしいことがわかります．

# 次に，`pageEnd`から`pageStart`を引いて，各話のページ数を算出してみます．

# In[119]:


df_tmp = df.copy()
df_tmp['pages'] = df_tmp['pageEnd'] - df_tmp['pageStart']
df_tmp['pages'].describe().reset_index()


# `pages`は0より大きいことが期待されるため，最小値は小さすぎます．また，最大値も非常識的な値となっています．

# ### `numberOfPages`（各号の合計ページ数）

# `numberOfPages`（雑誌の合計ページ数）を`describe`で基礎集計します．
# なお，`df`をそのまま`describe`してしまうと掲載作品数が多い雑誌巻号にバイアスのかかった統計量になってしまうため注意が必要です．
# そこで，ここでは`miname`で中間集計した`df_tmp`を`describe`します．

# In[135]:


df_tmp = df.groupby('miname')[
    ['numberOfPages', 'datePublished', 'price']].\
    first().reset_index()
df_tmp['numberOfPages'].describe().reset_index()


# 最小値が小さすぎる気がします．
# 試しに`numberOfPages`でソートすると，

# In[136]:


df_tmp.sort_values('numberOfPages').head(10)


# 最初の二つに関しては入力ミスが疑われます．降順にソートしてみます．

# In[137]:


df_tmp.sort_values('numberOfPages', ascending=False).head(10)


# 特別号の可能性があるので，妥当性の判断が難しいです．
# 
# いずれにしても`numberOfPages`は欠測数が多いため，積極的に分析に利用する必要はなさそうに見えます．

# In[138]:


df_tmp['numberOfPages'].isna().sum()


# ### `datePublished`（発行日）

# `datePublished`（発行日）を`describe`で基礎集計します．
# 前述したように`df`を直接`describe`するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[153]:


df_tmp = df.groupby('miname')[['datePublished']].    first().reset_index()
# 日付処理を容易にするため，`pd.to_datetime`で型変換
df_tmp['datePublished'] = pd.to_datetime(df_tmp['datePublished'])
df_tmp['datePublished'].describe().reset_index()


# 次に，年単位で集計してみます．

# In[154]:


df_tmp['yearPublished'] = df_tmp['datePublished'].dt.year
df_tmp.value_counts('yearPublished').reset_index().    sort_values('yearPublished', ignore_index=True)


# 集計開始年（`1970`）および集計終了年（`2017`）以外は，年間およそ190-205回ほど発行していることがわかります．

# ### `price`（雑誌価格）

# `price`（雑誌価格）を`describe`で基礎集計します．
# 前述したように`df`を直接`describe`するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[155]:


df_tmp = df.groupby('miname')[['price']].    first().reset_index()


# In[159]:


df_tmp['price'].describe().reset_index()


# 一冊80円だった時代があったのでしょうか…？後ほど分析します．

# ### `publisher`（出版社）

# `publisher`（出版社）に関して集計します． 前述したように`df`を直接集計するとバイアスが乗るので，minameで中間集計したdf_tmpに対して分析を実施します．

# In[184]:


df_tmp = df.groupby('miname')[['mcname', 'publisher']].    first().reset_index()


# 雑誌ごとに出版社名を集計します．

# In[185]:


df_tmp.groupby('mcname')['publisher'].    value_counts().reset_index(name='count')


# かなり表記がぶれているようですが，今後積極的に使う情報ではないため，このままにしておきます．

# ### `editor`（編集者）

# `editor`（編集者）に関して集計します． 前述したように`df`を直接集計するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[188]:


df_tmp = df.groupby('miname')[['mcname', 'editor']].    first().reset_index()


# In[193]:


df_tmp.groupby('mcname')['editor'].value_counts().    reset_index(name='count')


# 誤記と思われるものがいくつかあります：
# 
# - `週刊少年サンデー`
#     - `三上伸一`さん（おそらく`三上信一`さん？）
# - `週刊少年ジャンプ`
#     - `鳥島和彦`さん（おそらく`鳥嶋和彦`さん？）
#     - `高校俊昌`さん（おそらく`高橋俊昌`さん？）

# 数も少ないですし，確証が持てないため特に修正しないことにします．
