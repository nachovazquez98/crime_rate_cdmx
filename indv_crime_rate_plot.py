from tokenize import Double
import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
import itertools
import random
from itertools import product
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
from data_processing import *

if "selected" in st.session_state:
    del st.session_state.selected

def indv_crime_rate_plot():
    st.title("Tasa de crimen por delito y municipio en ZMG")    
    #gui
    option = st.radio("Seleccione el tipo de gráfica: ", ['Comparativo', 'Tendencia por delito y municipio'])
    if option == 'Comparativo':
        option1 = st.radio('Seleccione el tipo de análisis: ', ['Un delito y varios municipios', 'Varios delitos y un municipio'])
        if option1 == 'Un delito y varios municipios':
            sample = st.radio("Seleccione el sampleo de la serie de tiempo: ", ['M','1Q','2Q', 'Y'])
            municipios = st.multiselect("Seleccione los municipios", list(dict_delitos_tasa.keys()))
            list_delitos = list(dict_delitos_tasa['Guadalajara'].columns)
            delitos = st.selectbox('Seleccione un delito', list(dict_delitos_tasa['Guadalajara'].columns)[:40])
            list_subdelitos = [string for string in list_delitos if delitos in string]
            sub_delitos = st.selectbox('Seleccione un subtipo de delito', list_subdelitos)

            # dict_filter = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
            # dict_env = dict_filter(dict_delitos_tasa, tuple(municipios))
            # dict_env = [dict_delitos_tasa[k] for k in municipios]
            dict_env = {x:dict_delitos_tasa[x] for x in municipios}

            new_dict = {}
            listing=list(dict_env)
            for l in listing:
                df= dict_env[l][sub_delitos]
                df = df.rename(str(l)+'_'+str(sub_delitos))
                new_dict[l] = df

            df_list = [ v for k,v in new_dict.items()] 
            df_env = pd.concat(df_list ,axis=1)   
            df_env = df_env.resample(sample, closed='left').last()     
            #plot
            st.line_chart(df_env)
            st.dataframe(df_env)
        elif option1 == 'Varios delitos y un municipio':

            sample = st.radio("Seleccione el sampleo de la serie de tiempo: ", ['M','1Q','2Q', 'Y'])
            municipio = st.selectbox("Seleccione un municipio", list(dict_delitos_tasa.keys()))
            list_delitos = list(dict_delitos_tasa['Guadalajara'].columns)

            delitos = st.multiselect('Seleccione los delitos', list(dict_delitos_tasa['Guadalajara'].columns)[:40])
            new_list1 = [i for i in list_delitos if any(b in i for b in delitos)]
            new_data = [list(b) for a, b in itertools.groupby(new_list1, key=lambda x: x.split("-")[0])]
            list_subdelitos = [random.choice(i) for i in new_data]
            
            sub_delitos = st.multiselect('Seleccione los subtipos de delito', list_subdelitos)

            df_env = dict_delitos_tasa[municipio][sub_delitos]
            df_env = df_env.resample(sample, closed='left').last()   
            #plot
            st.line_chart(df_env)
            st.dataframe(df_env)

    elif option == 'Tendencia por delito y municipio':


        municipios = st.multiselect("Seleccione los municipios", list(dict_delitos_tasa.keys()))
        delitos = st.multiselect('Seleccione los delitos', list(dict_delitos_tasa['Guadalajara'].columns)[:40])
        list_delitos = list(dict_delitos_tasa['Guadalajara'].columns)
        new_list1 = [i for i in list_delitos if any(b in i for b in delitos)]
        new_data = [list(b) for a, b in itertools.groupby(new_list1, key=lambda x: x.split("-")[0])]
        list_subdelitos = [random.choice(i) for i in new_data]
        sub_delitos = st.multiselect('Seleccione los subtipos de delito', list_subdelitos)

        type_trend = st.radio("Seleccione la tendencia respecto al tiempo: ", ['1 año', '6 meses', '3 meses','1 mes'])
        #compara la tendencia de la tasa de criminalidad respecto al año pasado
        df_tabla_total_trend = tabla_total_trend(municipios, sub_delitos, type_trend)

        st.dataframe(df_tabla_total_trend)
        if st.button('Generar graficas'):
            for index, row in df_tabla_total_trend.iterrows():
                if row['trend'].strip():
                    index_delito_municipio = df_tabla_total_trend.iloc[index,:]
                    municipio = index_delito_municipio.loc['municipio']
                    delito = index_delito_municipio.loc['delito']
                    df_delito_municipio = dict_delitos_tasa[municipio][delito]
                    df_delito_municipio = pd.DataFrame(df_delito_municipio)
                    df_delito_municipio.columns = [str(delito)+'_'+str(municipio)+'_'+str(row['trend'][:5])]
                    st.line_chart(df_delito_municipio)
                    st.dataframe(df_delito_municipio.astype(str))
                else:
                    pass
