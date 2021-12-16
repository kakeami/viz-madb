#!/usr/bin/env python
# coding: utf-8

# # 前処理

# - `madb`からcsv形式でデータを取得
# - `pytrend`で各漫画作品のGoogle検索量を取得

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

