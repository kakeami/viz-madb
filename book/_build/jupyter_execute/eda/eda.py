#!/usr/bin/env python
# coding: utf-8

# # そもそもどんなデータを扱うの？

# ここでは，本書で分析対象とするデータについて簡単に紹介し，基礎分析を実施します．なお，このデータは[MADB Labでv1.0として公開されているもの](https://github.com/mediaarts-db/dataset/tree/1.0)に[こちらの前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html)を実施したものです．

# ## 下準備

# In[1]:


import pandas as pd

import warnings
warnings.filterwarnings('ignore')


# In[2]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'


# In[3]:


df = pd.read_csv(PATH_DATA)


# ## 概要

# `df`は
# 
# - 週刊少年サンデー
# - 週刊少年ジャンプ
# - 週刊少年チャンピオン
# - 週刊少年マガジン
# 
# の`1970-07-27`から`2017-07-06`までのすべての掲載作品のデータを格納した`DataFrame`です．
# まずはサイズを見てみましょう．

# In[4]:


df.shape


# 各週の掲載作品を一行ずつ格納しているため，合計で約18万行程度の規模になります．
# 以下に，各列の構成を示します．

# In[5]:


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
# - `pages`: 各話のページ数（`pageEnd` - `pageStart` + 1）
# - `pageEndMax`: 雑誌に掲載されているマンガ作品のうち，`pageEnd`の最大値
# - `pageStartPosition`: 各話の`pageStart`の相対的な位置（`pageStart` / `pageEndMax`）

# 冒頭数行を見て，データのイメージを掴んでみましょう．

# In[112]:


df.head()


# `pandas`の`describe()`コマンドでざっくり集計してみます．

# In[113]:


df.describe()


# In[114]:


df.isna().sum().reset_index()


# ```{admonition} 前処理が原因の欠測
# `numberOfPages`，`price`に関しては，想定外のパターンのデータを`NaN`に変換するよう[前処理](https://kakeami.github.io/viz-madb/appendix/preprocess.html#cm102)を施しています．詳細はAppendixをご参照ください．
# ```
# 
# 特に`epname`と`publisher`の欠測が多いことがわかります．

# ## 列ごとの基礎分析

# ### `mcname`（雑誌名）

# In[115]:


df['mcname'].value_counts().reset_index()


# 上記は`mcname`ごとの行数を表します．それぞれ同一期間で集計しましたが，掲載作品数の違いが生じています．

# ### `miname`（雑誌巻号名）

# ユニークな`miname`数を集計します．

# In[116]:


df['miname'].nunique()


# `mcname`（雑誌）ごとに集計した`miname`（雑誌巻号）は：

# In[117]:


df.groupby('mcname')['miname'].nunique().reset_index()


# ほぼ同数ですが，雑誌によって微妙に巻号数が異なることがわかります．
# 
# 次は，`miname`（雑誌巻号）ごとに`mcname`（マンガ作品）数を集計してみます．

# In[118]:


df.groupby('miname')['cname'].nunique().sort_values().reset_index()


# 1970年付近の黎明期は掲載数が少なめだったようです．また，雑誌によってタイミングはバラバラですが，非常に沢山のマンガを掲載する**外れ値**が存在することもわかります．

# ### `cname`（マンガ作品名）

# ユニークな`cname`（マンガ作品）数を集計します．

# In[119]:


df['cname'].nunique()


# `mcname`（雑誌）ごとに`cname`（マンガ作品）数を集計します．

# In[120]:


df.groupby('mcname')['cname'].nunique().reset_index()


# ジャンプが圧倒的に多いですね…．試しに`cname`（マンガ作品）ごとに掲載数を集計してみます．

# In[121]:


df_tmp = df[['mcname', 'cname']].value_counts().reset_index()
df_tmp.columns = ['mcname', 'cname', 'counts']
df_tmp


# ```{admonition} あれ，あの長編作品は…？
# シーズンごとに作品名が変わっているシリーズ作品（ドカベン，刃牙，浦鉄，ジョジョ等）は，それぞれ別作品として集計されていることにご注意ください．
# ```
# 
# 連載期間が長いものを見てみましょう．こち亀，はじめの一歩，名探偵コナン，ONEPIECE，MAJORと各雑誌のレジェンドが連なります．
# 一方で，連載期間が短いものの中には，企画ものや読み切りが存在するようです．
# 
# 雑誌ごとに，マンガ作品の連載期間に関して基礎集計します．

# In[122]:


df_tmp.groupby('mcname')['counts'].describe()


# やはりジャンプの平均連載期間が，他誌と比べて短いことがわかります．

# ### `epname`（各話タイトル）

# ユニークな`epname`（各話タイトル）数を集計します．

# In[123]:


df['epname'].nunique()


# 意外と重複しているようです．集計してみます．

# In[124]:


df['epname'].value_counts().reset_index()


# プロ野球編ってことは…．

# In[125]:


df[df['epname']=='プロ野球編']['cname'].value_counts().reset_index()


# やっぱりドカベンですね！ドカベンってもしかして**〇〇編**の粒度でしかタイトルをつけないのでしょうか…？ドカベンの`epname`を集計してみます．

# In[126]:


df[df['cname']=='ドカベン']['epname'].value_counts().reset_index()


# In[127]:


df[df['cname']=='ドカベン']['epname'].isna().sum()


# プロ野球編以外のドカベンの各話タイトルは欠測しているため，これ以上のことはわからなそうです．

# ### `creator`（作者）

# `df`に存在する`creator`（作者）数を集計します．

# In[128]:


df['creator'].nunique()


# 合計作品数が多い`creator`を調べてみます．

# In[129]:


df['creator'].value_counts().reset_index().head(10)


# メンツが強すぎます…．
# 個人的にはこち亀の`秋本治`先生が一番かなと予想していましたが，`水島新司`先生が圧倒的でした．
# 
# ちなみに，こち亀の`creator`を集計すると以下のようになります．

# In[130]:


df[df['cname']=='こちら葛飾区亀有公園前派出所']['creator'].value_counts().reset_index()


# `秋本治`先生は，デビュー時`山止たつひこ`というペンネームを使っていました．
# 
# （この101話分を足しても全然追いつかない`水島新司`先生がすごすぎますが…）

# ### `pageStart`（開始ページ）

# `pageStart`（開始ページ）について`describe()`で基礎集計すると，以下のようになります．

# In[131]:


df['pageStart'].describe().reset_index()


# ### `pageEnd`（終了ページ）

# `pageEnd`（終了ページ）について`describe()`で基礎集計すると，以下のようになります．

# In[132]:


df['pageEnd'].describe().reset_index()


# ### `numberOfPages`（各号の合計ページ数）

# `numberOfPages`（雑誌の合計ページ数）を`describe`で基礎集計します．
# なお，`df`をそのまま`describe`してしまうと掲載作品数が多い雑誌巻号にバイアスのかかった統計量になってしまうため注意が必要です．
# そこで，ここでは`miname`で中間集計した`df_tmp`を`describe`します．

# In[133]:


df_tmp = df.groupby('miname')[
    ['numberOfPages']].first().reset_index()
df_tmp['numberOfPages'].describe().reset_index()


# 最小値が小さすぎる気がします．
# 試しに`numberOfPages`でソートすると，

# In[134]:


df_tmp.sort_values('numberOfPages').head(10)


# 最初の二つに関しては入力ミスが疑われます．降順にソートしてみます．

# In[135]:


df_tmp.sort_values('numberOfPages', ascending=False).head(10)


# 特別号の可能性があるので，妥当性の判断が難しいです．
# 
# いずれにしても`numberOfPages`は欠測数が多いため積極的に分析に利用せず，後述する`pageEndMax`で代用します．

# In[136]:


df_tmp['numberOfPages'].isna().sum()


# ### `datePublished`（発行日）

# `datePublished`（発行日）を`describe`で基礎集計します．
# 前述したように`df`を直接`describe`するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[137]:


df_tmp = df.groupby('miname')[['datePublished']].    first().reset_index()
# 日付処理を容易にするため，`pd.to_datetime`で型変換
df_tmp['datePublished'] = pd.to_datetime(df_tmp['datePublished'])
df_tmp['datePublished'].describe().reset_index()


# 次に，年単位で集計してみます．

# In[138]:


df_tmp['yearPublished'] = df_tmp['datePublished'].dt.year
df_tmp.value_counts('yearPublished').reset_index().    sort_values('yearPublished', ignore_index=True)


# 集計開始年（`1970`）および集計終了年（`2017`）以外は，年間およそ190-205回ほど発行していることがわかります．

# ### `price`（雑誌価格）

# `price`（雑誌価格）を`describe`で基礎集計します．
# 前述したように`df`を直接`describe`するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[139]:


df_tmp = df.groupby('miname')[['price']].    first().reset_index()
df_tmp['price'].describe().reset_index()


# 一冊80円だった時代があったのでしょうか…？後ほど分析します．

# ### `publisher`（出版社）

# `publisher`（出版社）に関して集計します． 前述したように`df`を直接集計するとバイアスが乗るので，minameで中間集計したdf_tmpに対して分析を実施します．

# In[140]:


df_tmp = df.groupby('miname')[['mcname', 'publisher']].    first().reset_index()


# 雑誌ごとに出版社名を集計します．

# In[141]:


df_tmp.groupby('mcname')['publisher'].    value_counts().reset_index(name='count')


# かなり表記がぶれているようですが，今後積極的に使う情報ではないため，このままにしておきます．

# ### `editor`（編集者）

# `editor`（編集者）に関して集計します． 前述したように`df`を直接集計するとバイアスが乗るので，`miname`で中間集計した`df_tmp`に対して分析を実施します．

# In[142]:


df_tmp = df.groupby('miname')[['mcname', 'editor']].    first().reset_index()


# In[143]:


df_tmp.groupby('mcname')['editor'].value_counts().    reset_index(name='count')


# 誤記と思われるものがいくつかあります：
# 
# - `週刊少年サンデー`
#     - `三上伸一`さん（おそらく`三上信一`さん？）
# - `週刊少年ジャンプ`
#     - `鳥島和彦`さん（おそらく`鳥嶋和彦`さん？）
#     - `高校俊昌`さん（おそらく`高橋俊昌`さん？）

# 数も少ないですし，確証が持てないため特に修正しないことにします．

# ### `pages`（各話のページ数）

# `pages`（各話のページ数）を`describe`で基礎集計します．

# In[144]:


df['pages'].describe().reset_index()


# 四分位は納得感がありますが，最小・最大が想定外です．昇順で並び替えてみます．

# In[145]:


df.sort_values('pages').head()


# `週刊少年ジャンプ 2004年 表示号数20`について[メディア芸術データベースで調べた](https://mediaarts-db.bunka.go.jp/id/M543111/)ところ，`BLEACH`は通常連載に加えて綴込み付録で`-17. 逸れゆく星々の為の前奏曲`を掲載したようです．
# `pageStart`および`pageEnd`が中途半端な小数になっているのはそのためでしょう．

# In[147]:


df.sort_values('pages', ascending=False).head()


# `週刊少年ジャンプ 2015年 表示号数48`について[メディア芸術データベースで調べた](https://mediaarts-db.bunka.go.jp/id/M675741/)ところ，`磯部磯兵衛物語～浮世はつらいよ～`は二周年記念で巻頭カラーをもらっていたようです．巻末の定位置での掲載はなかったことから，おそらく`pageEnd`は誤入力と思われます．

# ### `pageEndMax`（雑誌巻号の最大の`pageEnd`）

# `pageEndMax`（雑誌巻号の最大の`pageEnd`）を`describe`で基礎集計します．なお，`df`をそのまま`describe`してしまうと掲載作品数が多い雑誌巻号にバイアスのかかった統計量になってしまうため注意が必要です． そこで，ここでは`miname`で中間集計した`df_tmp`を`describe`します．

# In[148]:


df_tmp = df.groupby('miname')[
    ['pageEndMax']].first().reset_index()
df_tmp['pageEndMax'].describe().reset_index()


# ### `pageStartPosition`（各話の相対的な掲載位置）

# `pageStartPosition`（各話の相対的な掲載位置）について，`describe`で基礎集計します．

# In[149]:


df['pageStartPosition'].describe().reset_index()


# 概ね想定通りの結果が出ましたが，最大値が1なのが少し気になるので，深堀りしてみます．

# In[151]:


df[df['pageStartPosition']==1].    value_counts('cname').reset_index(name='counts')


# `ハレハレまんが時評`は週刊少年チャンピオンの巻末の目次ページに掲載されていた4コマ漫画のようです（恥ずかしながら，知りませんでした）．他のものに関しても同様でしょうか．
