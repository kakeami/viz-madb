#!/usr/bin/env python
# coding: utf-8

# # Grouped bars

# ## 概要
# 
# **Grouped bars**とは，複数の要素をまとめて描画した棒グラフです．

# ## Plotlyによる作図方法

# Plotlyでは，`plotly.express.bar()`で`barmode='group'`を指定することで描画可能です．

# ```python
# import plotly.express as px
# fig = px.bar(
#     df, x='col_x', y='col_y',
#     color='col_group', barmode='group')
# ```

# 上記の例では，`df`の`col_x`を横軸，`col_y`を縦軸とし，`col_group`によって色を塗り分けたGrouped barsを作図可能です．

# ## MADB Labを用いた作図例

# In[ ]:




