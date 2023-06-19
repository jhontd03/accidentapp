import copy
from graphs import count_graph, scatter_graph, map_accident, sum_stats_study, choropleth_graph
from common import load_data_pickle
import streamlit as st

base="dark"
textColor="#c1c1c1"

st.set_page_config(layout="wide")
st.title("Explorando las condiciones que conllevan a la accidentalidad en las carreteras de los Estados Unidos")
st.subheader('Aplicación desarrollada por: [Jhon Jairo Realpe](https://github.com/jhontd03)')

'''
La presente aplicación hace parte de la práctica final de la Asignatura Visualización de Datos del 
[Máster Universitario en Ciencia de Datos de la UOC](https://www.uoc.edu/es/estudios/masters/master-universitario-data-science). 

El conjunto de datos seleccionado se deriva de los reportes de la [Administración Nacional 
de Seguridad del Tráfico en las Carreteras](https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/), 
cuya compilación de informes se crearon para los Estados Unidos, con el objetivo de proporcionar una medida global de la seguridad de las carreteras.
Para el desarrollo de esta aplicación se ha considerado los datos del periodo 2011-2021.

Con base en esta información se presentan distintas visualizaciones interactivas cuyo propósito es explorar e identificar 
las condiciones que conllevan a un mayor o menor grado de accidentalidad en las carreteras de los Estados Unidos.
'''

###############################################################################
# Load data and select variables 
###############################################################################

PATH = "data/data_accident.pkl"

data_accident = load_data_pickle(PATH)

states = list(data_accident['State'].unique())
years= list(data_accident['Year'].unique())
cat_study = ['State', 'City', 'County', 'Day of month', 
             'Month', 'Year', 'Day of week', 'Hour', 'Route', 'Ligth condition', 'Climatic condition']     
vars_study = ['Fatals', 'Total vehicles involved', 'Vehicles in motion', 
              'Parked vehicles', 'Pedestrian', 'Cyclists', 'Persons in Vehicles']

###############################################################################
# Sider page 
###############################################################################

st.sidebar.markdown("### Seleccione una opción: ")

list_states=[]
list_states=states[:]
list_states.append('Todos los estados')
state_filter = st.sidebar.selectbox('Estado', list_states)
if 'Todos los estados' in state_filter:
 	state_filter=states

years_string = [str(item) for item in years]
list_years = []
list_years = years_string[:]
list_years.append('Todos los años')
year_filter = st.sidebar.selectbox('Año', list_years)
if 'Todos los años' in year_filter:
 	year_filter = years_string

view_map = st.sidebar.selectbox('Visualizar mapa', ['No', 'Si'])

###############################################################################
# Body page 
###############################################################################

expander_1 = st.expander('Análisis general', expanded=True)

tab1, tab2, tab3 = expander_1.tabs(["Conteo accidentes por año", "Conteo variables categóricas", "Suma total variables numéricas"])

with tab1:
    st.plotly_chart(count_graph(data_accident, state_filter, years, 'Year'), 
                    theme="streamlit", use_container_width=True)

with tab2:
    cat_tab2 = copy.deepcopy(cat_study) 
    cat_tab2.remove('Year')
    cat_filter_1 = st.selectbox('Categoría', cat_tab2)
    st.plotly_chart(count_graph(data_accident, state_filter, year_filter, cat_filter_1), 
                    theme="streamlit", use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:       
        cat_filter_2 = st.selectbox('Categoría estudio', cat_tab2)        
    with col2:
        study_filter = st.selectbox('Variable estudio', vars_study)
    st.plotly_chart(sum_stats_study(data_accident, state_filter, year_filter, study_filter, cat_filter_2), 
                    theme="streamlit", use_container_width=True)
    
expander_2 = st.expander('Análisis Correlación', expanded=True)
col1, col2, col3 = expander_2.columns(3)
with col1:
    x_var = st.selectbox('Variable 1', vars_study)
with col2:
    y_var = st.selectbox('Variable 2', vars_study)
with col3:
    z_var = st.selectbox('Variable 3', vars_study)

expander_2.plotly_chart(scatter_graph(data_accident, 
                                      year_filter, 
                                      state_filter, 
                                      x_var=x_var,
                                      y_var=y_var, 
                                      z_var=z_var), 
                                      theme="streamlit", 
                                      use_container_width=True)
if view_map == 'Si':
    expander_3 = st.expander('Mapa Accidentes', expanded=True)
    var_filter = expander_3.selectbox("Parámetro Estudio", vars_study)

    tab1, tab2 = expander_3.tabs(["Suma total por Estados", "Ubicación de Accidentes por Estados"])

    with tab1:  
        st.plotly_chart(choropleth_graph(data_accident, year_filter, var_filter), 
                        theme="streamlit", 
                        use_container_width=True)
    with tab2:  
        map_accident(data_accident, state_filter, year_filter, var_filter)
