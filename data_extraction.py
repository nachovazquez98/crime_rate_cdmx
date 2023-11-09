import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import urllib.request, json 
from calendar import monthrange
import pickle

zmg_poblacion_dict = {
    "Guadalajara" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140039/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Zapopan" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140120/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "San Pedro Tlaquepaque" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140098/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Tonalá" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140101/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Tlajomulco de Zúñiga" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140097/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "El Salto" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140070/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Ixtlahuacán de los Membrillos" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140044/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Juanacatlán" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140051/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Zapotlanejo" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140124/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json",
    "Acatlán de Juárez" : "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000140002/false/BISE/2.0/648e2ab0-9e88-7069-e494-dc7d2f2ab341?type=json"
}

def load_delitos_df():
    delitos_df = pd.read_csv("data/IDM_NM_sep23.csv", encoding='latin-1',thousands=',')
    delitos_df = delitos_df[delitos_df['Entidad'] == 'Jalisco']
    return delitos_df

def load_zmg_poblacion(zmg_poblacion_dict):
    year_df = pd.DataFrame(index = pd.date_range('1995', '2023', freq='Y', name='year'), columns = ['population'])
    year_df.index =year_df.index.year
    df_pobl_zmg = year_df.copy()
    for municipio, link in zmg_poblacion_dict.items():
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
            pobl_df = pd.DataFrame([
                ['1995', int(float(data['Series'][0]['OBSERVATIONS'][0]['OBS_VALUE']))],
                ['2000', int(float(data['Series'][0]['OBSERVATIONS'][1]['OBS_VALUE']))],
                ['2005', int(float(data['Series'][0]['OBSERVATIONS'][2]['OBS_VALUE']))],
                ['2010', int(float(data['Series'][0]['OBSERVATIONS'][3]['OBS_VALUE']))],
                ['2020', int(float(data['Series'][0]['OBSERVATIONS'][4]['OBS_VALUE']))],
            ], columns=['year', 'population'])
            pobl_df.index = pobl_df.year
            pobl_df = pobl_df.drop(['year'], axis=1)
            pobl_df.index= pd.to_datetime(pobl_df.index) 
            pobl_df.index = pobl_df.index.year
            #merge datetime nan d list_pobl_zmg.append(pobl_df)f 
            pobl_df = pd.merge(year_df, pobl_df,how='outer',left_index=True,right_index=True)
            pobl_df = pobl_df.drop( pobl_df.columns[0], axis = 1)
            # Split data in training (not NaN values) and missing (NaN values)
            missing = pobl_df.isna().any(axis=1)
            df_training = pobl_df[~missing]
            df_missing = pobl_df[missing]
            #apply interpol and extrapol
            f = interp1d(df_training.index, df_training.iloc[:,0], fill_value="extrapolate", kind = "quadratic")
            df_missing["population_y"] = f(df_missing.index)
            #concat og df and new rows
            pobl_df = pd.concat([df_missing,pobl_df])
            #delete nan
            pobl_df.dropna(subset = ["population_y"], inplace=True)
            #sort and round values
            pobl_df = pobl_df.round().sort_index()
            pobl_df.rename(columns={'population_y': str(municipio)}, inplace=True)
            #plot
            #pobl_df.plot(title = str(municipio))
            df_pobl_zmg[str(municipio)] = pobl_df.iloc[:,0]
    df_pobl_zmg['population'] = df_pobl_zmg.iloc[:,1:-1].sum(axis=1) 
    return df_pobl_zmg

def process_delitos_df(delitos_df, zmg_poblacion_dict):
    dict_delitos_sum = {}
    municipios_zmg_list = list(zmg_poblacion_dict.keys())
    delitos_list = delitos_df['Tipo de delito'].value_counts().index.tolist()
    
    zmg_delitos_df = delitos_df[delitos_df['Municipio'].isin(municipios_zmg_list)]
    zmg_delitos_df['delito_subtipo'] = zmg_delitos_df[zmg_delitos_df.columns[6:8]].apply(lambda x: '_'.join(x.dropna().astype(str)),axis=1)
    zmg_delito_subtipo_list = zmg_delitos_df['delito_subtipo'].value_counts().index.tolist()
    zmg_delitos_df['delito_subtipo_modalidad'] = zmg_delitos_df[zmg_delitos_df.columns[6:9]].apply(lambda x: '_'.join(x.dropna().astype(str)),axis=1)
    zmg_delito_subtipo_modalidad_list = zmg_delitos_df['delito_subtipo_modalidad'].value_counts().index.tolist()

    updated_year = zmg_delitos_df['Año'].max()
    df_lastyear = zmg_delitos_df[zmg_delitos_df['Año'] == updated_year][['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']]
    notnull_months_list = df_lastyear.columns[df_lastyear.notnull().any()].tolist()
    updated_month_1 = str(df_lastyear.columns[df_lastyear.notnull().any()].tolist().__len__() + 1).zfill(2)
    updated_month = str(df_lastyear.columns[df_lastyear.notnull().any()].tolist().__len__()).zfill(2)

    for municipio in municipios_zmg_list:
        delitos_municipio = zmg_delitos_df[zmg_delitos_df['Municipio'] == municipio]
        delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', str(updated_year)+'-'+ updated_month_1, freq='M'))
        delitos_sum_df.index.name = 'date'
        years = np.arange(2015,updated_year + 1)
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        for delito in delitos_list:
            values_delito = []
            for year in years:
                if year != updated_year:
                    for mes in meses:
                        value = delitos_municipio.loc[(delitos_municipio['Tipo de delito'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                        values_delito.append(value)
                else:
                    for mes in meses:
                        if any(mes in x  for x in notnull_months_list):
                            value = delitos_municipio.loc[(delitos_municipio['Tipo de delito'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                            values_delito.append(value)
                        else:
                            # value = int(0)
                            # values_delito.append(np.nan)
                            pass
            delitos_sum_df[str(delito)] = values_delito
            dict_delitos_sum[municipio] = delitos_sum_df

    return dict_delitos_sum, municipios_zmg_list, zmg_delitos_df, delitos_list, zmg_delito_subtipo_list, zmg_delito_subtipo_modalidad_list, updated_year, df_lastyear, notnull_months_list, updated_month_1, updated_month

def delito_zmg():
    df_delito_zmg = pd.DataFrame(index = pd.date_range('2015', str(updated_year + 1), freq='M', name='month'), columns = ['delito'])
    #eliminar hasta el ultimo mes null
    n_null_months = len(df_lastyear.columns[df_lastyear.isnull().any()].tolist())
    df_delito_zmg.drop(df_delito_zmg.tail(n_null_months).index,inplace=True) # drop last n rows

    for municipio in municipios_zmg_list:
        dict_delitos_sum[str(municipio)]['total_sum'] = dict_delitos_sum[str(municipio)].sum(axis=1)
        df_suma_delito = dict_delitos_sum[str(municipio)]['total_sum'].resample('M').sum()
        #df_suma_delito.index = df_suma_delito.index.year
        df_delito_zmg[str(municipio)] = df_suma_delito
    df_delito_zmg['delito'] = df_delito_zmg.iloc[:,1:-1].sum(axis=1)
    df_delito_zmg = df_delito_zmg.rename(columns={'delito': 'ZMG'})
    return df_delito_zmg

def crime_rate_preprocess():
    df_pobl_zmg.rename(columns={'population':'ZMG'}, inplace=True)
    df_pobl_month_zmg = df_pobl_zmg.iloc[-8:,]
    df_pobl_month_zmg.index = pd.to_datetime(df_pobl_month_zmg.index, format='%Y')
    df_pobl_month_zmg.index = df_pobl_month_zmg.index.to_period('M').to_timestamp('M')

    n_days_month = monthrange(int(updated_year), int(updated_month))[1]
    df_reindexed = df_pobl_month_zmg.reindex(pd.date_range(start='2015-01-31', end=str(updated_year)+'-'+str(updated_month)+'-'+str(n_days_month), freq='M'))
    df_reindexed.index.names = ['year']
    df_reindexed = df_reindexed.interpolate(method='quadratic', limit_direction='both')

    df_pobl_zmg.rename(columns={'population':'ZMG'}, inplace=True)
    df_pobl_month_zmg = df_pobl_zmg.iloc[-8:,]
    df_pobl_month_zmg.index = pd.to_datetime(df_pobl_month_zmg.index, format='%Y')
    df_pobl_month_zmg.index = df_pobl_month_zmg.index.to_period('M').to_timestamp('M')

    n_days_month = monthrange(int(updated_year), int(updated_month))[1]
    df_reindexed = df_pobl_month_zmg.reindex(pd.date_range(start='2015-01-31', end=str(updated_year)+'-'+str(updated_month)+'-'+str(n_days_month), freq='M'))
    df_reindexed.index.names = ['year']
    df_reindexed = df_reindexed.interpolate(method="quadratic", fill_value="extrapolate")
    #tasa de criminalidad
    # df_crime_rate_zmg = ((df_delito_zmg.loc[:, df_delito_zmg.columns != 'ZMG']/df_reindexed.loc[:, df_delito_zmg.columns != 'ZMG'])*100000)
    df_crime_rate_zmg = ((df_delito_zmg/df_reindexed)*100000)
    return df_crime_rate_zmg, df_reindexed

def trend_crime_rate():
    updated_year = zmg_delitos_df['Año'].max()
    df_lastyear = zmg_delitos_df[zmg_delitos_df['Año'] == updated_year][['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']]
    notnull_months_list = df_lastyear.columns[df_lastyear.notnull().any()].tolist()
    updated_month_1 = str(df_lastyear.columns[df_lastyear.notnull().any()].tolist().__len__() + 1).zfill(2)
    updated_month = str(df_lastyear.columns[df_lastyear.notnull().any()].tolist().__len__()).zfill(2)

    for municipio in municipios_zmg_list:
        delitos_municipio = zmg_delitos_df[zmg_delitos_df['Municipio'] == municipio]
        delitos_sum_df = pd.DataFrame(index = pd.date_range('2015-01', str(updated_year)+'-'+ updated_month_1, freq='M'))
        delitos_sum_df.index.name = 'date'
        years = np.arange(2015,updated_year + 1)
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        for delito in delitos_list:
            values_delito = []
            for year in years:
                if year != updated_year:
                    for mes in meses:
                        value = delitos_municipio.loc[(delitos_municipio['Tipo de delito'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                        values_delito.append(value)
                else:
                    for mes in meses:
                        if any(mes in x  for x in notnull_months_list):
                            value = delitos_municipio.loc[(delitos_municipio['Tipo de delito'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                            values_delito.append(value)
                        else:
                            # value = int(0)
                            # values_delito.append(np.nan)
                            pass
            delitos_sum_df[str(delito)] = values_delito
            dict_delitos_sum[municipio] = delitos_sum_df

        for delito in zmg_delito_subtipo_list:
            values_delito = []
            for year in years:
                if year != updated_year:
                    for mes in meses:
                        value = delitos_municipio.loc[(delitos_municipio['delito_subtipo'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                        values_delito.append(value)
                else:
                    for mes in meses:
                        if any(mes in x  for x in notnull_months_list):
                            value = delitos_municipio.loc[(delitos_municipio['delito_subtipo'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                            values_delito.append(value)
                        else:
                            # value = int(0)
                            # values_delito.append(value)
                            pass
            delitos_sum_df[str(delito)] = values_delito
            dict_delitos_sum[municipio] = delitos_sum_df

        for delito in zmg_delito_subtipo_modalidad_list:
            values_delito = []
            for year in years:
                if year != updated_year:
                    for mes in meses:
                        value = delitos_municipio.loc[(delitos_municipio['delito_subtipo_modalidad'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                        values_delito.append(value)
                else:
                    for mes in meses:
                        if any(mes in x  for x in notnull_months_list):
                            value = delitos_municipio.loc[(delitos_municipio['delito_subtipo_modalidad'] == delito) & (delitos_municipio['Año'] == year), mes].sum()
                            values_delito.append(value)
                        else:
                            # value = int(0)
                            # values_delito.append(value)
                            pass
            delitos_sum_df[str(delito)] = values_delito
            dict_delitos_sum[municipio] = delitos_sum_df

    #calcular tasa delictiva por delito y municipio
    dict_delitos_tasa = dict_delitos_sum.copy()
    for municipio in df_reindexed.iloc[:,1:].columns:
        for i in range(0, len(dict_delitos_tasa[str(municipio)])):
            dict_delitos_tasa[str(municipio)].iloc[:,i] = (dict_delitos_tasa[str(municipio)].iloc[:,i] / df_reindexed[str(municipio)]) * 100000

    return dict_delitos_tasa  

#global vars
delitos_df = load_delitos_df()
df_pobl_zmg = load_zmg_poblacion(zmg_poblacion_dict)
dict_delitos_sum, municipios_zmg_list, zmg_delitos_df, delitos_list, zmg_delito_subtipo_list, zmg_delito_subtipo_modalidad_list, updated_year, df_lastyear, notnull_months_list, updated_month_1, updated_month = process_delitos_df(delitos_df, zmg_poblacion_dict)

n_days_month = monthrange(int(updated_year), int(updated_month))[1]
last_datetime = str(updated_year)+'-'+str(updated_month)+'-'+str(n_days_month)
df_delito_zmg = delito_zmg()
df_crime_rate_zmg, df_reindexed = crime_rate_preprocess()
dict_delitos_tasa = trend_crime_rate()

dict_global_vars = {
    'delitos_df': delitos_df,
    'df_pobl_zmg': df_pobl_zmg,
    'dict_delitos_sum': dict_delitos_sum,
    'municipios_zmg_list': municipios_zmg_list,
    'zmg_delitos_df': zmg_delitos_df,
    'delitos_list': delitos_list,
    'zmg_delito_subtipo_list': zmg_delito_subtipo_list,
    'zmg_delito_subtipo_modalidad_list': zmg_delito_subtipo_modalidad_list,
    'updated_year': updated_year,
    'df_lastyear': df_lastyear,
    'notnull_months_list': notnull_months_list,
    'updated_month_1': updated_month_1,
    'updated_month': updated_month,
    'n_days_month': n_days_month,
    'last_datetime': last_datetime,
    'df_delito_zmg': df_delito_zmg,
    'df_crime_rate_zmg': df_crime_rate_zmg,
    'df_reindexed': df_reindexed,
    'dict_delitos_tasa': dict_delitos_tasa
}

file_global_vars = open("file_global_vars.txt", "wb") 
pickle.dump(dict_global_vars, file_global_vars)
file_global_vars.close