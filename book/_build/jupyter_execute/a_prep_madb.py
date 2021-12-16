#!/usr/bin/env python
# coding: utf-8

# # Appendix A: MADBの前処理

# `madb`から必要なデータを抽出し，扱いやすいようcsvに変換

# ## 環境構築

# In[1]:


# Notebook初期設定
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

import warnings
warnings.filterwarnings('ignore')


# In[2]:


import glob
import json
import os
import pandas as pd
from tqdm import tqdm_notebook as tqdm
import zipfile


# In[3]:


DIR_IN = '../madb/data/json-ld'
DIR_TMP = '../data/preprocess/tmp'
DIR_OUT = '../data/preprocess/out'


# In[4]:


FNS_CM = [
    'cm102',
    'cm105',
    'cm106',
]


# In[5]:


# CM105で使用するカラム
COL_CM105 = [
    'identifier',
    'label',
    'note',
    'publicationPeriodicity',
    'name',
    'publisher',
    'dayPublishedFinal',
]


# In[6]:


get_ipython().system('ls {DIR_IN}')


# ## 関数

# In[7]:


def read_json(path):
    """
    jsonファイルを辞書として読み込む関数．

    Params:
        path (str): 読込対象ファイルパス
    Returns:
        dict: 辞書
    """
    with open(path, 'r') as f:
        dct = json.load(f)

    return dct


# In[35]:


def save_json(path, dct):
    """
    辞書をjson形式で保存する関数．

    Params:
        path (str): jsonファイルの保存先
        dct (dict): 保存対象辞書
    """
    with open(path, 'w') as f:
        json.dump(dct, f, ensure_ascii=False, indent=4)


# ## 解凍
# 
# マンガ系のデータ（`*cm*`）のみ`DIR_TMP`に解凍する．

# In[22]:


ps_cm = glob.glob(f'{DIR_IN}/*_cm*')


# In[23]:


for p_from in tqdm(ps_cm):
    p_to = p_from.replace(DIR_IN, DIR_TMP).replace('.zip', '')
    
    with zipfile.ZipFile(p_from) as z:
        z.extractall(p_to)


# ## 前処理

# ### 対象

# In[9]:


ps_cm = {cm: glob.glob(f'{DIR_TMP}/*{cm}*/*') for cm in FNS_CM}


# In[10]:


ps_cm


# ### `cm105`

# In[11]:


cm105 = read_json(ps_cm['cm105'][0])


# In[12]:


df_cm105 = pd.DataFrame(cm105['@graph'])[COL_CM105]


# In[26]:


def get_published_name(name):
    """nameからpublished_nameを取得"""
    for x in name:
        if type(x) is str:
            return x
    raise Exception(f'No published_name in {name}!')


# In[31]:


# 雑誌名を取得
df_cm105['mcname'] = df_cm105['name'].apply(lambda x: get_published_name(x))


# In[32]:


# 例
df_cm105.head(3).T


# In[34]:


# mcnameからmcidを引く辞書
mcname2mcid = df_cm105.groupby('mcname')['identifier'].first().to_dict()


# In[36]:


# 保存
save_json(os.path.join(DIR_TMP, 'mcname2mcid.json'), mcname2mcid)


# ### `cm102`

# In[38]:


cm102 = read_json(ps_cm['cm102'][0])


# In[54]:


def get_items_by_genre(graph, genre):
    """graphから所定のgenreのアイテム群を取得"""
    items = [
        x for x in graph 
        if 'genre' in x.keys() and x['genre'] == genre]
    return items


# In[61]:


# 各ジャンルのアイテム群を取得
mis = get_items_by_genre(cm102['@graph'], '雑誌巻号')
eps = get_items_by_genre(cm102['@graph'], 'マンガ作品')


# In[59]:


len(mis)


# In[63]:


pd.DataFrame(mis).head(3).T


# In[60]:


len(eps)


# In[64]:


pd.DataFrame(eps).head(3).T


# misとepsで必要な情報だけ残して，あとはマージすればOK
