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

def crime_plot():
    st.title("Suma total de delitos en ZMG")    
    #gui
    option = st.radio("Seleccione el tipo de gráfica: ", ['Comparativo', 'Descomposición Estacional'])
    if option == 'Comparativo':
        sample = st.radio("Seleccione el sampleo de la serie de tiempo: ", ['M','1Q','2Q', 'Y'])
        municipios = st.multiselect("Seleccione los municipios", list(df_delito_zmg.columns))
        #plot
        df_env = df_delito_zmg.resample(sample, closed='left').last()[municipios]
        st.line_chart(df_env)
        st.dataframe(df_env)
    elif option == 'Descomposición Estacional':
        municipios = st.selectbox("Seleccione un municipio", list(df_delito_zmg.columns))
        #plot
        df_env = df_delito_zmg[[municipios]]
        decom = seasonal_decompose(df_env[municipios], model = 'additive', extrapolate_trend=True )
        df_env['Tendencia'] = decom.trend.values
        df_env['Residual'] = decom.resid.values
        st.line_chart(df_env)
        st.dataframe(df_env)     
