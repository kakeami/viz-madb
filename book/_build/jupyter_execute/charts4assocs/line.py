#!/usr/bin/env python
# coding: utf-8

# # 折れ線グラフ（1変数）

# ## 概要

# **折れ線グラフ（Line Chart）** は，主に **時間とともに変化する量的変数** を対象に， その推移を **直線** で表現するグラフです．
# 横軸に日付や時刻等の変数をとり，縦軸に変化を追いたい量的変数を取ります．

# ![](../figs/charts/line.png)

# 例えば上図は，`ONE PIECE`の掲載位置の推移を表した折れ線グラフです．

# ## Plotlyによる作図方法

# Plotlyにおいては，`plotly.express.line()`で作図できます．

# ```python
# import plotly.express
# fig = px.line(
#     df, x='col_x', y='col_y')
# ```

# 例えば上記の例では，`df`の`col_x`列（時間的な変数であることが多いです）を横軸，`col_y`列を縦軸に取った棒グラフオブジェクト`fig`を作成します．

# ## MADB Labを用いた作図例

# ### 下準備

# In[3]:


import pandas as pd
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')


# In[4]:


# 前処理の結果，以下に分析対象ファイルが格納されていることを想定
PATH_DATA = '../../data/preprocess/out/episodes.csv'
# Jupyter Book用のPlotlyのrenderer
RENDERER = 'plotly_mimetype+notebook'


# In[5]:


# 連載週数の最小値
MIN_WEEKS = 5


# In[6]:


def show_fig(fig):
    """Jupyter Bookでも表示可能なようRendererを指定"""
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    # 凡例でグラフが潰れないよう調整
    fig.update_layout(legend={
        'yanchor': 'top',
        'xanchor': 'left',
        'x': 0.01, 'y': 0.99})
    fig.show(renderer=RENDERER)


# In[7]:


df = pd.read_csv(PATH_DATA)


# ### 長期連載作品の掲載位置の推移

# In[52]:


df_tmp =     df.groupby('cname')['pageStartPosition']    .agg(['count', 'mean']).reset_index()
df_tmp =     df_tmp.sort_values('count', ascending=False, ignore_index=True)    .head(10)
cname2position = df_tmp.groupby('cname')['mean'].first().to_dict()


# In[53]:


df_plot = df[df['cname'].isin(list(cname2position.keys()))]    .reset_index(drop=True)
df_plot['position'] = df_plot['cname'].apply(
    lambda x: cname2position[x])
df_plot['datePublished'] = pd.to_datetime(df_plot['datePublished'])
df_plot =     df_plot.sort_values(['position', 'datePublished'], ignore_index=True)


# In[55]:


cnames = df_plot['cname'].unique()
for cname in cnames:
    df_c = df_plot[df_plot['cname']==cname].reset_index(drop=True)
    fig = px.line(
        df_c, x='datePublished', y='pageStartPosition',
        hover_data=['epname'], title=f'{cname}の掲載位置の推移')
    fig.update_traces(
        mode='lines+markers',
        marker=dict(line_width=1, size=10))
    fig.update_xaxes(title='発売日')
    fig.update_yaxes(title='掲載位置', range=[-.1, 1.1])
    fig.update_layout(hovermode='x unified')
    show_fig(fig)


# マンガ好きの方であれば，マウスをホバーさせて各話情報を眺めるだけでも楽しめるのではないでしょうか？

# ### 番外編：`ONE PIECE`の企画ページを除外する

# ところで，`ONE PIECE`にしては明らかに掲載位置が後ろすぎるデータが散見されます．

# In[42]:


# 作品名ONE PIECEで抽出
df_op = df_plot[df_plot['cname']=='ONE PIECE'].reset_index(drop=True)


# In[67]:


# 降順で先頭10例を表示
df_op.sort_values('pageStartPosition', ascending=False).head(10)


# 本編ではない企画ページが含まれているようです．
# 
# そもそも合計データ数が

# In[68]:


df_op.shape[0]


# であるのに対し，最新の話数は

# In[69]:


df_op.sort_values('datePublished').tail(1)['epname']


# ですので，単純に考えると

# In[70]:


890 - 869


# 話分のデータを除外する必要がありそうです．以下では，これらを除外することを考えます．

# 企画ページは本編と比較して短いことが考えられるので，5ページ以下のデータを抽出してみます．

# In[71]:


(df_op['pages'] <= 5).sum()


# In[72]:


df_op[df_op['pages'] <= 5][['pages', 'epname']].reset_index()


# この抽出条件で良さそうです．
# 上記以外のデータで，再度折れ線グラフを描いてみましょう．

# In[73]:


df_op_new = df_op[df_op['pages'] > 5].reset_index(drop=True)
fig = px.line(
    df_op_new, x='datePublished', y='pageStartPosition',
    hover_data=['epname'], 
    title=f'ONE PIECEの掲載位置の推移（修正後）')
fig.update_traces(
    mode='lines+markers',
    marker=dict(line_width=1, size=10))
fig.update_xaxes(title='発売日')
fig.update_yaxes(title='掲載位置', range=[-.1, 1.1])
fig.update_layout(hovermode='x unified')
show_fig(fig)


# 興味があるので，掲載位置で降順ソートしてみましょう．

# In[74]:


df_op_new.sort_values('pageStartPosition', ascending=False)[
    ['miname', 'datePublished', 'epname', 'pageStartPosition']].\
    head(10)


# `ONE PIECE`は，`第565話 オーズの道`の除き，全て雑誌の前半に掲載されていることがわかります．
# 人気（等）に応じて掲載位置が決まると言われる`週刊少年ジャンプ`では驚異的なことです．
