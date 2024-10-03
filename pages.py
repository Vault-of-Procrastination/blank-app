# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

# Import General
from io import BytesIO
from functools import partial
import numpy as np, pandas as pd, time, os
from datetime import datetime as dt2, time as t2, date as d2, timedelta as td

# Import Graphs
# import altair as alt
# from plotly import express as px, graph_objects as go
# from streamlit_extras.stylable_container import stylable_container

# Import Streamlit
from utils.css import get_css, get_table
from streamlit_extras.stylable_container import stylable_container

# In[1]

def init_session_state(st):
    # '🎛️🎙️📻📱🎥📺📷📸📹🔎🔍📰📑📱📅📊'
    if 'logged_in' not in st.session_state:
        st.session_state['page'] = 'login'
        st.session_state['logged_in'] = False
        st.session_state['username'] = 'user'
        st.session_state['password'] = 'password'
        st.session_state['token'] = 'token'
        st.session_state['database'] = st.secrets['database']
        
        df = pd.read_csv('data/data.csv')
        df = df.reset_index().rename(columns = {'index': 'id'})
        df['fecha'] = pd.to_datetime(df['fecha'], format = '%m/%d/%Y').dt.date
        df['hora'] = pd.to_datetime(df['hora'], format = '%I:%M:%S %p').dt.time
        df['etiquetas'] = df['etiquetas'].str.split(',')
        
        st.session_state['df'] = df
        st.session_state['filtered_df'] = df

def switch(st):
    match st.session_state['page']:
        case 'login':
            login(st)
        case 'register':
            register(st)
        case 'table':
            table(st)
        case 'dashboard':
            dashboard(st)

def set_page(st, page: str):
    st.session_state['page'] = page
    st.rerun()

# In[2]
# st.query_params.to_dict()


# st.markdown(f"<style>{get_css('main_1')}</style>", unsafe_allow_html = True)

def login(st):
    with st.form('login', True, border = False):
        col1, col2, col3 = st.columns(3)
        with col2:
            st.header('Welcome to Media Monitor', divider = 'red')
            with st.container(): # stylable_container('login_container', get_css('login_register')):
                st.header('Log In')
                username = st.text_input('Username')
                password = st.text_input('Password', type = 'password')
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    login_button = st.form_submit_button('Login')
                with col1_2:
                    register_button = st.form_submit_button('Register')
        
                if login_button:
                    # Verificar las credenciales
                    if username == st.session_state['username'] and password == st.session_state['password']:
                        st.session_state.logged_in = True
                        st.success('Login successful!')
                        time.sleep(1.5)
                        set_page(st, 'table')
                    else:
                        st.error('Invalid username or password. Please try again.')#, icon = '🚫')
                
                if register_button:
                    set_page(st, 'register')

def register(st):
    with st.form('signin', True, border = False):
        col1, col2, col3 = st.columns(3)
        with col2:
            st.header('Bienvenido a Media Monitor', divider = 'red')
            with st.container(): # stylable_container('register_container', get_css('login_register')):
                st.header('Registro')
                username = st.text_input('Username')
                password = st.text_input('Password', type = 'password')
                token = st.text_input('Token')
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    return_button = st.form_submit_button('Return')
                with col1_2:
                    register_button = st.form_submit_button('Register')
        
                if return_button:
                    set_page(st, 'login')
                if register_button:
                    if token == st.session_state['token']:
                        st.session_state['username'] = username
                        st.session_state['password'] = password
                        st.success('Register successful!')
                        time.sleep(1.5)
                        set_page(st, 'login')
                    else:
                        st.error('Invalid Token. Please try again.')

# st.markdown(f"<style>{get_css('main_2')}</style>", unsafe_allow_html = True)

def note(st, note_id: int = None):
    @st.dialog('Alta' if note_id is None else 'Edicion', width  = 'large')
    def show_dialog():
        default_data = {'categoria': [f'Categoria {x}' for x in range(11)],
                        'etiquetas': [f'Etiqueta {x}' for x in range(11)],
                        'periodista': [f'Periodista {x}' for x in range(11)],
                        'funcionario': [f'Funcionario {x}' for x in range(11)],
                        'dependencia': [f'Dependencia {x}' for x in range(11)],
                        'convenio': [f'Convenio {x}' for x in range(11)],
                        'partido': [f'Partido {x}' for x in range(11)],
                        'candidato': [f'Candidato {x}' for x in range(11)],
                        'estatus': ['Positivo', 'Negativo', 'Neutro']}
        
        if note_id is None:
            fecha_val, hora_val, minuto_val = (lambda x: [x.date(), x.hour, x.minute])(dt2.now())
            init_data = {'categoria': None, 'etiquetas': None, 'canal': None, 'periodista': None, 'funcionario': None,
                         'dependencia': None, 'convenio': None, 'web': None, 'partido': None, 'candidato': None, 'tiempo': 0,
                         'fecha': fecha_val, 'hora': hora_val, 'minuto': minuto_val, 'estatus': 0, 'nota': None}
            data = {'id': 0 if st.session_state['df'] is None else st.session_state['df']['id'].max() + 1}
        else:
            init_data = st.session_state['df'].iloc[note_id].to_dict()
            init_data['categoria'] = default_data['categoria'].index(init_data['categoria'])
            init_data['etiquetas'] = None if len(init_data['etiquetas']) == 0 else init_data['etiquetas']
            init_data['periodista'] = default_data['periodista'].index(init_data['periodista'])
            init_data['funcionario'] = default_data['funcionario'].index(init_data['funcionario'])
            init_data['dependencia'] = default_data['dependencia'].index(init_data['dependencia'])
            init_data['convenio'] = default_data['convenio'].index(init_data['convenio'])
            init_data['partido'] = default_data['partido'].index(init_data['partido'])
            init_data['candidato'] = default_data['candidato'].index(init_data['candidato'])
            init_data['minuto'] = init_data['hora'].minute
            init_data['hora'] = init_data['hora'].hour
            init_data['estatus'] = default_data['estatus'].index(init_data['estatus'])
            data = {'id': note_id}
        
        show = False
        
        with st.form('register', True, border = False):
            col_n1_1, col_n1_2 = st.columns([0.4, 0.6])
            with col_n1_1:
                data['categoria'] = st.selectbox('Categoria', default_data['categoria'], init_data['categoria'], key = 'diag_cat')
            with col_n1_2:
                data['etiquetas'] = st.multiselect('Etiquetas', default_data['etiquetas'], init_data['etiquetas'], key = 'diag_tag')
            
            data['canal'] = st.text_input('Canal/Titulo', init_data['canal'], key = 'diag_chan')
            
            col_n2_1, col_n2_2 = st.columns(2)
            with col_n2_1:
                data['periodista'] = st.selectbox('Periodista', default_data['periodista'], init_data['periodista'])
            with col_n2_2:
                data['funcionario'] = st.selectbox('Funcionario', default_data['funcionario'], init_data['funcionario'])
                
            col_n3_1, col_n3_2 = st.columns(2)
            with col_n3_1:
                data['dependencia'] = st.selectbox('Dependencia', default_data['dependencia'], init_data['dependencia'])
            with col_n3_2:
                data['convenio'] = st.selectbox('Convenio', default_data['convenio'], init_data['convenio'])
            
            data['web'] = st.text_input('Pagina Web', init_data['web'])
                
            col_n4_1, col_n4_2 = st.columns([0.35, 0.65])
            with col_n4_1:
                data['partido'] = st.selectbox('Partido', default_data['partido'], init_data['partido'])
            with col_n4_2:
                data['candidato'] = st.selectbox('Candidato', default_data['candidato'], init_data['candidato'])
            
            
            col_n5_1, col_n5_2, col_n5_3, col_n5_4 = st.columns([0.45, 0.15, 0.15, 0.25], vertical_alignment = 'bottom')
            with col_n5_1:
                data['tiempo'] = st.number_input('Tiempo en medios (min):', 0, value = init_data['tiempo'])
            with col_n5_2:
                data['fecha'] = st.date_input('Fecha', init_data['fecha'])
            with col_n5_3:
                with st.popover('Horario'):
                    col_n6_p1_1, col_n6_p1_2 = st.columns(2)
                    with col_n6_p1_1:
                        hora = st.number_input('Hora', 0, 23, init_data['hora'])
                    with col_n6_p1_2:
                        minuto = st.number_input('Minuto', 0, 59, init_data['minuto'])
                    data['hora'] = t2(hora, minuto)
            with col_n5_4:
                data['estatus'] = st.selectbox('Estatus', default_data['estatus'], init_data['estatus'])
            
            data['nota'] = st.text_area('Nota:', init_data['nota'])
            
            uploaded_image = st.file_uploader('Imagen', ['jpg', 'pgn'], True)
            if show and uploaded_image is not None:
                if isinstance(uploaded_image, list):
                    bytes_image = []
                    for upload_image in uploaded_image:
                        bytes_image.append(BytesIO(upload_image.getvalue()))
                        st.image(bytes_image[-1])
                else:
                    bytes_image = BytesIO(uploaded_image.getvalue())
                    st.image(bytes_image)
            
            uploaded_video = st.file_uploader('Video', ['mp4'], True)
            if show and uploaded_video is not None:
                if isinstance(uploaded_video, list):
                    bytes_video = []
                    for upload_video in uploaded_video:
                        bytes_video.append(BytesIO(upload_video.getvalue()))
                        st.video(bytes_video[-1])
                else:
                    bytes_video = BytesIO(uploaded_video.getvalue())
                    st.video(bytes_video)
            
            uploaded_audio = st.file_uploader('Audio', ['mp3', 'wav'], True)
            if show and uploaded_audio is not None:
                if isinstance(uploaded_audio, list):
                    bytes_audio = []
                    for upload_audio in uploaded_audio:
                        bytes_audio.append(BytesIO(upload_audio.getvalue()))
                        st.audio(bytes_audio[-1])
                else:
                    bytes_audio = BytesIO(uploaded_audio.getvalue())
                    st.audio(bytes_audio)
            
            col_n7_1, col_n7_2, col_n7_3 = st.columns([0.7, 0.15, 0.15])
            with col_n7_2:
                guardar = st.form_submit_button('Guardar')
            with col_n7_3:
                cancelar = st.form_submit_button('Cancelar')
            
            if guardar:
                if note_id is None:
                    st.session_state['df'] = pd.concat([st.session_state['df'], pd.DataFrame([data])])
                else:
                    st.session_state['df'].iloc[note_id] = pd.Series(data)
                st.session_state['filtered_df'] = st.session_state['df']
                st.rerun()
            if cancelar:
                st.rerun()
    show_dialog()

# with st.sidebar:
#     st.logo('./media/ai_logo.jpg')

def table(st):
    df = st.session_state['df']
    
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.header('Monitor')
    with col2:
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            pass
        with col2_2:
            st.button('Registrar', on_click = note, args = (st,))
    with stylable_container('search_filter', get_css('search')):
        with st.form('search', True, border = False):
            st.header('Filtros de busqueda', divider = 'gray')
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns([0.19, 0.19, 0.19, 0.19, 0.19, 0.05], vertical_alignment = 'bottom')
            with col_s1:
                today, min_date, max_date = d2.today(), df['fecha'].min(), df['fecha'].max()
                dates = st.date_input('Rango de Fechas', [min(today, max_date) for _ in range(2)], min_date, max_date)
            with col_s2:
                categories = st.selectbox('Categorias', [f'Categoria {x}' for x in range(10)], None)
            with col_s3:
                tags = st.multiselect('Etiquetas', [f'Etiqueta {x}' for x in range(10)])
            with col_s4:
                canal_list = df['canal'].unique().tolist()
                channel = st.selectbox('Canal/Titulo', canal_list, None)
            with col_s5:
                paragraph = st.text_input('Conjunto de Palabras')
            with col_s6:
                search = st.form_submit_button('Buscar')
    
    if search:
        filter_df = df['fecha'].between(*dates)
        if not categories is None:
            filter_df = filter_df & (df['categoria'] == categories)
        if len(tags) > 0:
            filter_df = filter_df & df['etiquetas'].apply(lambda x: len(set(x) & set(tags)) > 0)
        if not channel is None:
            filter_df = filter_df & (df['canal'] == channel)
        if not paragraph == '':
            filter_df = filter_df & df['nota'].str.contains(paragraph)
        
        df = st.session_state['df'][filter_df]
        st.session_state['filtered_df'] = df
    
    with stylable_container('table_data', get_css('table')):
        st.header('Reporte', divider = 'gray')
        columns = ['id', 'estatus', 'etiquetas', 'categoria', 'canal', 'nota', 'fecha', 'hora']
        df_config = {'id': st.column_config.Column('#', width = 'small'),
                     'categoria': st.column_config.Column('Categoria', width = 'medium'),
                     'etiquetas': st.column_config.ListColumn('Etiquetas', width = 'large'),
                     'canal': st.column_config.Column('Canal/Titulo', width = 'medium'),
                     'periodista': st.column_config.Column('Periodista', width = 'medium'),
                     'funcionario': st.column_config.Column('Funcionario', width = 'medium'),
                     'dependencia': st.column_config.Column('Dependencia', width = 'medium'),
                     'convenio': st.column_config.Column('Convenio', width = 'medium'),
                     'partido': st.column_config.Column('Partido', width = 'small'),
                     'candidato': st.column_config.Column('Candidato', width = 'medium'),
                     'tiempo': st.column_config.NumberColumn('Tiempo', width = 'small'),
                     'fecha': st.column_config.DateColumn('Fecha', format = 'MM/DD/YYYY', width = 'small'),
                     'hora': st.column_config.TimeColumn('Hora', format = "HH:mm", width = 'small'),
                     'estatus': st.column_config.TextColumn('Estatus', width = 'small'),
                     'nota': st.column_config.TextColumn('Breve Informativo', max_chars = 50, width = 'large')}
        index_df = st.dataframe(st.session_state['filtered_df'], use_container_width = True, hide_index = True, column_order = columns,
                                column_config = df_config, on_select = 'rerun', selection_mode = 'single-row')
        
        col_t1, col_t2, col_t3 = st.columns([0.9, 0.05, 0.05])
        with col_t1:
            st.write('Mostrando los primeros 100 datos.')
        with col_t2:
            st.button('Anterior', disabled = True)
        with col_t3:
            st.button('Despues', disabled = True)
    
    if len(index_df['selection']['rows']) > 0:
        with stylable_container('table_data', get_css('info')):
            
            sdf = {x: y for x, y in df.iloc[index_df['selection']['rows'][0]].to_dict().items() if x not in ['tiempo']}
            
            sdf['etiquetas'] = '<li>' + '</li>\n                    <li>'.join(sdf['etiquetas']) + '</li>'
            sdf['fecha'] = sdf['fecha'].strftime('%m/%d/%Y')
            sdf['hora'] = sdf['hora'].strftime('%H:%M')
            sdf['class_estatus'] = sdf['estatus'].lower()
            
            col_i1_1, col_i1_2, col_i1_3, col_i1_4 = st.columns([0.4, 0.5, 0.05, 0.05], vertical_alignment = 'bottom')
            with col_i1_1:
                st.header('Info de Fila', divider = 'gray')
            with col_i1_2:
                st.header('Info de la nota', divider = 'gray')
            with col_i1_3:
                st.link_button('Link', sdf['web'], type = "secondary")
            with col_i1_4:
                st.button('Editar', on_click = note, args = (st, sdf['id']))
            
            
            col_i2_1, col_i2_2 = st.columns([0.4, 0.6])
            with col_i2_1:
                st.markdown(get_table('info') % sdf, unsafe_allow_html = True)
            with col_i2_2:
                st.text_area('Informacion de la nota', sdf['nota'], 500, disabled = True)

def dashboard(st):
    st.write('dashboard')


