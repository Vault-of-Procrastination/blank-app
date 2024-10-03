# -*- coding: utf-8 -*-
"""
@author: gabriel.hernandez
"""

# In[0]

# Import for Streamlit
import streamlit as st

from pages import init_session_state, switch

# In[1]

st.set_page_config(page_title = 'Media Monitoring', page_icon = '🖥️', layout = 'wide', initial_sidebar_state = 'collapsed')

init_session_state(st)

# In[2]

switch(st)


