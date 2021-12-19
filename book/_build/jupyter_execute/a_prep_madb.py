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
import numpy as np
import os
import pandas as pd
from pprint import pprint
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


# cm102, genre=='雑誌巻号'
COLS_MIS = {
    'identifier': 'miid',
    'label': 'miname',
    'datePublished': 'datePublished',
    'isPartOf': 'mcid',
    'issueNumber': 'issueNumber',
    'numberOfPages': 'numberOfPages',
    'publisher': 'publisher',
    'volumeNumber': 'volumeNumber',
    'price': 'price',
    'editor': 'editor',
}


# In[7]:


# cm102, genre=='マンガ作品'
COLS_EPS = {
    'relatedCollection': 'cid',
    'creator': 'creator',
    'note': 'note',
    'alternativeHeadline': 'epname',
    'pageStart': 'pageStart',
    'pageEnd': 'pageEnd',
    'isPartOf': 'miid',
}


# In[47]:


# cm106
COLS_CS = {
    'identifier': 'cid', 
    'name': 'cname'
}


# In[8]:


get_ipython().system('ls {DIR_IN}')


# ## 関数

# In[9]:


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


# In[10]:


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

# In[11]:


ps_cm = {cm: glob.glob(f'{DIR_TMP}/*{cm}*/*') for cm in FNS_CM}


# In[48]:


pprint(ps_cm)


# ### `cm105`
# 
# 漫画雑誌に関するデータを整形し，分析対象のIDを特定．

# In[13]:


def format_magazine_name(name):
    """nameからpublished_nameを取得"""
    for x in name:
        if type(x) is str:
            return x
    raise Exception(f'No magazine name in {name}!')


# In[14]:


cm105 = read_json(ps_cm['cm105'][0])


# In[15]:


df_cm105 = pd.DataFrame(cm105['@graph'])[COL_CM105]


# In[16]:


# 雑誌名を取得
df_cm105['mcname'] = df_cm105['name'].apply(
    lambda x: format_magazine_name(x))


# In[17]:


# 週刊少年ジャンプのmcidを取得
df_cm105[df_cm105['mcname']=='週刊少年ジャンプ']


# In[18]:


mcids = ['C119459']


# ### `cm102`
# 
# 雑誌巻号およびマンガ作品に関するデータを整形し，一次保存．

# In[19]:


def format_cols(df, cols_rename):
    """cols_renameのcolのみを抽出し，renmae"""
    df_new = df.copy()
    df_new = df_new[cols_rename]
    df_new = df_new.rename(columns=cols_rename)
    return df_new


# In[20]:


def get_items_by_genre(graph, genre):
    """graphから所定のgenreのアイテム群を取得"""
    items = [
        x for x in graph 
        if 'genre' in x.keys() and x['genre'] == genre]
    return items


# In[21]:


def get_id_from_url(url):
    """url表記から末尾のidを取得"""
    if url is np.nan:
        return None
    else:
        return url.split('/')[-1]


# In[22]:


def format_nop(numberOfPages):
    """numberOfPagesからpやPを除外"""
    nop = numberOfPages
    if nop is np.nan:
        return None
    else:
        return int(nop.replace('p', '').replace('P', ''))


# In[23]:


def format_price(price):
    """priceを整形"""
    if price is np.nan:
        return None
    elif price == 'JUMPガラガラウなかも':
        # M544740, 週刊少年ジャンプ 1971年 表示号数47
        # price = 'JUMPガラガラウなかも'
        return None
    elif price == '238p':
        # M542801, 週刊少年ジャンプ 2010年 表示号数42
        # price = '238p'
        return 238
    else:
        price_new = price.replace('円', '').replace('+税', '')
        return int(price_new)


# In[24]:


def format_creator(creator):
    """creatorから著者名を取得"""
    if creator is np.nan:
        return None
    for x in creator:
        if type(x) is str:
            return x
    raise Exception('No creator name!')


# In[25]:


def create_df_mis(mis, mcids):
    """辞書形式のmisからdf_misを構築
    ただし，mcidsに含まれるデータのみ抽出"""
    df_mis = pd.DataFrame(mis)
    # 列を整理
    df_mis = format_cols(df_mis, COLS_MIS)
    # mcidを取得
    df_mis['mcid'] = df_mis['mcid'].apply(
        lambda x: get_id_from_url(x))
    # 特定のmcidsに該当する行のみ抽出
    df_mis = df_mis[df_mis['mcid'].isin(mcids)].reset_index(drop=True)
    # datePublishedでソート
    df_mis['datePublished'] = pd.to_datetime(df_mis['datePublished'])
    df_mis  = df_mis.sort_values('datePublished', ignore_index=True)
    # numberOfPagesを整形
    df_mis['numberOfPages'] = df_mis['numberOfPages'].apply(
        lambda x: format_nop(x))
    # priceを整形
    df_mis['price'] = df_mis['price'].apply(
        lambda x: format_price(x))
    return df_mis


# In[26]:


def create_df_eps(eps, miids):
    """辞書形式のepsからdf_epsを構築
    ただし，miidsに含まれるデータのみ抽出"""
    df_eps = pd.DataFrame(eps)
    # 列を整形
    df_eps = format_cols(df_eps, COLS_EPS)
    # url表記から各idを取得
    df_eps['cid'] = df_eps['cid'].apply(lambda x: get_id_from_url(x))
    df_eps['miid'] = df_eps['miid'].apply(lambda x: get_id_from_url(x))
    # miidsに該当するepsのみ抽出
    df_eps = df_eps[df_eps['miid'].isin(miids)].reset_index(drop=True)
    # 著者名を取得
    df_eps['creator'] = df_eps['creator'].apply(
        lambda x: format_creator(x))
    return df_eps


# In[27]:


for i, p in tqdm(enumerate(ps_cm['cm102'])):
    cm102 = read_json(p)
    
    # 各ジャンルのアイテム群を取得
    mis = get_items_by_genre(cm102['@graph'], '雑誌巻号')
    eps = get_items_by_genre(cm102['@graph'], 'マンガ作品')
    del cm102
    # pd.DataFrameとして整形
    df_mis = create_df_mis(mis, mcids)
    miids = set(df_mis['miid'].unique())
    df_eps = create_df_eps(eps, miids)
    del mis, eps
    
    # 保存
    fn_mis = os.path.join(DIR_TMP, f'mis_{i+1:05}.csv')
    fn_eps = os.path.join(DIR_TMP, f'eps_{i+1:05}.csv')
    df_mis.to_csv(fn_mis, index=False)
    df_eps.to_csv(fn_eps, index=False)


# ### `cm106`
# 
# 掲載作品に関するデータを整形し，一次保存．

# In[40]:


def format_cname(cname):
    """cnameから著者名を取得"""
    if cname is np.nan:
        return None
    for x in cname:
        if type(x) is str:
            return x
    raise Exception('No comic name!')


# In[30]:


cm106 = read_json(ps_cm['cm106'][0])


# In[43]:


# 雑誌掲載ジャンルのアイテムを抽出
cs = get_items_by_genre(cm106['@graph'], '雑誌掲載')
# DataFrame化
df_cs = pd.DataFrame(cs)
# カラムを整理
df_cs = format_cols(df_cs, COLS_CS)
# cnameを整形
df_cs['cname'] = df_cs['cname'].apply(
    lambda x: format_cname(x))


# In[45]:


# 保存
df_cs.to_csv(os.path.join(DIR_TMP, 'cs.csv'), index=False)


# ## 結合

# In[53]:


def read_and_concat_csvs(pathes):
    """pathesのcsvを順番に呼び出し，concat"""
    df_all = pd.DataFrame()
    for p in pathes:
        df = pd.read_csv(p)
        df_all = pd.concat([df_all, df], ignore_index=True)
    return df_all


# In[65]:


def sort_date(df, col_date):
    """dfをcol_dateでソート"""
    df_new = df.copy()
    df_new[col_date] = pd.to_datetime(df_new[col_date])
    df_new = df_new.sort_values(col_date, ignore_index=True)
    return df_new


# In[76]:


# 各ファイルのパスを抽出
ps_mis = glob.glob(f'{DIR_TMP}/mis*.csv')
ps_eps = glob.glob(f'{DIR_TMP}/eps*.csv')
ps_cs = glob.glob(f'{DIR_TMP}/cs*.csv')


# In[77]:


# データの読み出し
df_mis = read_and_concat_csvs(ps_mis)
df_eps = read_and_concat_csvs(ps_eps)
df_cs = read_and_concat_csvs(ps_cs)


# In[81]:


# 結合
df_all = pd.merge(df_eps, df_cs, on='cid', how='left')
df_all = pd.merge(df_all, df_mis, on='miid', how='left')


# In[104]:


# ソート
df_all['datePublished'] = pd.to_datetime(df_all['datePublished'])
df_all = df_all.sort_values(['datePublished', 'pageStart'], ignore_index=False)


# In[114]:


# 保存
df_all.to_csv(os.path.join(DIR_OUT, 'wj.csv'), index=False)

