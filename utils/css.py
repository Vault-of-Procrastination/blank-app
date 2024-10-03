# -*- coding: utf-8 -*-
"""
@author: gabriel.hernandez
"""

# In[0]

import os

# In[1]

def add_id(st, class_id: str):
    st.write(f"<div id = '{class_id}'></div>", unsafe_allow_html = True)
    
def add_style(st, test_id: str, class_id: str, style_str: str):
    css = """<style>
    div[data-testid='%s']:has(>div>div>div>div>div#%s)
        {
            %s
        };
</style>""" % (test_id, class_id, ';\n            '.join(style_str.split(';')))
    st.markdown(css, unsafe_allow_html = True)

def get_css(file_name: str) -> str:
    file_list = os.listdir('css/')
    if f'{file_name}.css' in file_list:
        return open(f'css/{file_name}.css').read()
    else:
        return ''

def get_table(table_name: str):
    table_list = os.listdir('html')
    if f'{table_name}.html' in table_list:
        return open(f'html/{table_name}.html').read()
    return ''