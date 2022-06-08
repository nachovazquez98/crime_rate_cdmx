import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import urllib.request, json 
import os
import matplotlib.pyplot as plt
from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import product
import math  
import pickle
##############
def tabla_total_trend(municipios, delitos, type_trend):
    df1 = pd.DataFrame(list(product(municipios_zmg_list, delitos_list)), columns=['municipio', 'delito'])
    df2 = pd.DataFrame(list(product(municipios_zmg_list, zmg_delito_subtipo_list)), columns=['municipio', 'delito'])
    df3 = pd.DataFrame(list(product(municipios_zmg_list, zmg_delito_subtipo_modalidad_list)), columns=['municipio', 'delito'])

    df_dsct = pd.concat([df1,df2,df3])
    df_dsct['trend'] = ""

    for municipio in municipios:
        for delito in delitos:
            df_delito_municipio = dict_delitos_tasa[municipio].sort_values(['date'])[delito]
            if type_trend == '1 año':
                sem1 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 23) : substract_dates(date = last_datetime, n_months = 12)].sum()
                sem2 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 11) : last_datetime].sum()
            if type_trend == '6 meses':
                sem1 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 11) : substract_dates(date = last_datetime, n_months = 6)].sum()
                sem2 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 5) : last_datetime].sum()
            if type_trend == '3 meses':
                sem1 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 5) : substract_dates(date = last_datetime, n_months = 3)].sum()
                sem2 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 2) : last_datetime].sum()
            if type_trend == '1 mes':
                sem1 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 3) : substract_dates(date = last_datetime, n_months = 2)].sum()
                sem2 = df_delito_municipio[substract_dates(date = last_datetime, n_months = 1) : last_datetime].sum()

            trend = pd.Series([sem1, sem2]).pct_change()[1]
            if np.isinf(trend) or np.isnan(trend):
                trend = math.inf

            df_dsct.loc[(df_dsct['municipio'] == municipio) & (df_dsct['delito'] == delito), ['trend']] = trend
    df_dsct = df_dsct[~df_dsct.isin([np.nan, np.inf, -np.inf]).any(1)]
    df_dsct.drop(df_dsct[df_dsct['trend'] == "inf"].index, inplace = True)
    df_dsct.drop(df_dsct[df_dsct['trend'] == "nan"].index, inplace = True)
    df_dsct['trend'] = df_dsct['trend'].astype(str)
    df_dsct = df_dsct.sort_values(by=['trend'],ignore_index=True, ascending = False)
    return df_dsct
#####
def substract_dates(date, n_months):
    date_format = '%Y-%m-%d'
    dtObj = datetime.delitos_dfstrptime(date, date_format)
    past_date = dtObj - relativedelta(months = n_months)
    substacted_date = past_date.strftime(date_format)
    substacted_date = datetime.strptime(substacted_date, date_format)
    year = substacted_date.year
    month = str(substacted_date.month).zfill(2)
    day = monthrange(int(year), int(month))[1]
    return str(year)+'-'+str(month)+'-'+str(day)

#delitos df
data_load_state = st.text('Loading data...')

with open('file_global_vars.txt', 'rb') as f:
    dict = pickle.load(f)

#global vars
delitos_df = dict['delitos_df']
df_pobl_zmg = dict['df_pobl_zmg']
dict_delitos_sum = dict['dict_delitos_sum']
municipios_zmg_list = dict['municipios_zmg_list']
zmg_delitos_df = dict['zmg_delitos_df']
delitos_list = dict['delitos_list']
zmg_delito_subtipo_list = dict['zmg_delito_subtipo_list']
zmg_delito_subtipo_modalidad_list = dict['zmg_delito_subtipo_modalidad_list']
updated_year = dict['updated_year']
df_lastyear = dict['df_lastyear']
notnull_months_list = dict['notnull_months_list']
updated_month_1 = dict['updated_month_1']
updated_month = dict['updated_month']
n_days_month = dict['n_days_month']
last_datetime = dict['last_datetime']
df_delito_zmg = dict['df_delito_zmg']
df_crime_rate_zmg = dict['df_crime_rate_zmg']
df_reindexed = dict['df_reindexed']
dict_delitos_tasa = dict['dict_delitos_tasa']

#global vars
data_load_state.text("Done! (using st.cache)")