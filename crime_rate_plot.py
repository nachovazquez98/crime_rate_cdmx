import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import urllib.request, json 
import os
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from data_processing import *

def crime_rate_plot():
    st.title("Tasa de criminalidad en ZMG")    



    #gui
    option = st.radio("Seleccione el tipo de gráfica: ", ['Streamgraph','Comparativo', 'Descomposición Estacional', 'Tabla de cambio porcentual'])
    if option == 'Streamgraph':
        fig, ax = plt.subplots()
        df_env = df_crime_rate_zmg.loc[:, df_crime_rate_zmg.columns != 'ZMG']
        ax.stackplot(
            df_env.index,
            *(df_env.iloc[:,i] for i in range(len(df_env.columns))),
            labels=df_env.columns,
            baseline='weighted_wiggle'
        )
        fig.suptitle('Tasa de criminalidad en la ZGM con streamgraph')
        ax.legend(bbox_to_anchor=(1.6, 1.0))
        st.pyplot(fig)
    elif option == 'Comparativo':
        sample = st.radio("Seleccione el sampleo de la serie de tiempo: ", ['M','1Q','2Q','Y'])
        municipios = st.multiselect("Seleccione los municipios", list(df_crime_rate_zmg.columns))
        #plot
        df_env = df_crime_rate_zmg.resample(sample, closed='left').last()[municipios]
        st.line_chart(df_env)
        st.dataframe(df_env)
    elif option == 'Descomposición Estacional':
        municipios = st.selectbox("Seleccione un municipio", list(df_crime_rate_zmg.columns))
        #plot
        df_env = df_crime_rate_zmg[[municipios]]
        decom = seasonal_decompose(df_env[municipios], model = 'additive', extrapolate_trend=True )
        df_env['Tendencia'] = decom.trend.values
        df_env['Residual'] = decom.resid.values
        st.line_chart(df_env)
        st.dataframe(df_env)     
    elif option == 'Tabla de cambio porcentual':
        def _color_red_or_green(val):
            color = 'green' if val < 0 else 'red'
            return 'color: %s' % color
        #Cambio porcentual de delitos en ZMG
        df_env = df_crime_rate_zmg
        (df_env.pct_change().loc['2015-01-31 00:00:00':]*100).style.applymap(_color_red_or_green).to_excel("Cambio porcentual de delitos en ZMG.xlsx")
        st.dataframe((df_env.pct_change().iloc[-24:,]*100).style.applymap(_color_red_or_green))