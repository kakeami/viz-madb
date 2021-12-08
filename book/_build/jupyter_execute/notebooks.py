#!/usr/bin/env python
# coding: utf-8

# # Plotlyのテスト
# 
# 本当に埋め込めるのか

# In[1]:


import plotly.io as pio
import plotly.express as px
import plotly.offline as py

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig

