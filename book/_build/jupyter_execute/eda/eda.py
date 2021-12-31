#!/usr/bin/env python
# coding: utf-8

# # そもそもどんなデータを扱うの？

# 本サイトで扱うデータについてまとめます．

# ## 環境構築

# In[1]:


import pandas as pd


# In[3]:


PATH_DATA = '../../data/preprocess/out/magazines.csv'


# In[7]:


df = pd.read_csv(PATH_DATA)


# ## 概要

# まず，データサイズを見てみます．

# In[5]:


df.shape


# カラムは次のようなものです．

# In[6]:


df.columns


# - `cid`: マンガ作品のID
# - `creator`: 作者名
# - `note`: 補足
# - `epname`: サブタイトル
# - `pageStart`: 雑誌掲載時の開始ページ数
# - `pageEnd`: 雑誌掲載時の終了ページ数
# - `miid`: 雑誌巻号のID
# - `cname`: マンガ作品名
# - `miname`: 雑誌巻号名
# - `datePublished`: 雑誌発行日
# - `mcid`: 雑誌のID
# - `issueNumber`:
# - `numberOfPages`
# - `publisher`
# - `volumeNumber`
# - `price`
# - `editor`

# In[9]:


for c in df.columns:
    print(f'- `{c}`')


# In[ ]:




