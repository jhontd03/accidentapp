"""
Este script realiza un proceso de extracción, transformación y carga.
Usa como fuente de datos los siguientes archivos: accident_20xx.csv, almacenados en el directorio: data/accident_data/*.csv.
Estos archivos fueron descargados manualmente de la página: https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/.
Cada archivo contiene variables de los reportes de accidentes de transito generados por la Administración Nacional 
de Seguridad del Tráfico en las Carreteras (NHTSA), por cada año

Tambien se usa el archivo FRPP_GLC_-_United_States_may_9__2023.xlsx, almacenado en el directorio: data/additional_data
y que fue descargado manualmente de: https://www.gsa.gov/reference/geographic-locator-codes/glcs-for-the-us-and-us-territories
Esta archivo contiene el código y nombre de las condados y ciudades de los Estados Unidos

Realizadas todas las operaciones se genera y exporta un archivo  denominado data_accident.pkl que se usará para implementar el dashboard
"""

import os
import pandas as pd

from common import data_replace, read_data, replace_state_county_city
from rename import (state_name, dayweek_name, month_name, 
                    weather, route, lgt_cond, 
                    code_state, cols_filter, change_name)

PATH = 'data'

def main():
    
    # Se cargan todos los archivos accident_20xx.csv, desde el 2011 a 2021
    list_files = [name for name in os.listdir(os.path.join(PATH, 'accident_data'))]
    
    data_2011 = read_data(list_files[10:][1], os.path.join(PATH, 'accident_data'))
    data_2012 = read_data(list_files[10:][2], os.path.join(PATH, 'accident_data'))
    data_2013 = read_data(list_files[10:][3], os.path.join(PATH, 'accident_data'))
    data_2014 = read_data(list_files[10:][4], os.path.join(PATH, 'accident_data'))
    data_2015 = read_data(list_files[10:][5], os.path.join(PATH, 'accident_data'))
    data_2016 = read_data(list_files[10:][6], os.path.join(PATH, 'accident_data'))
    data_2017 = read_data(list_files[10:][7], os.path.join(PATH, 'accident_data'))
    data_2018 = read_data(list_files[10:][8], os.path.join(PATH, 'accident_data'))
    data_2019 = read_data(list_files[10:][9], os.path.join(PATH, 'accident_data'))
    data_2020 = read_data(list_files[10:][10], os.path.join(PATH, 'accident_data'))
    data_2021 = read_data(list_files[10:][11], os.path.join(PATH, 'accident_data'))
    
    # Se carga el archivo que contiene la información del código de las ciudades y condados
    county_city_name = pd.read_excel(os.path.join(PATH, 'additional_data\\FRPP_GLC_-_United_States_may_9__2023.xlsx'))
    
    # Se crea lista con los valores a reemplazar en los dataframes asociados a los accidentes
    # ocurridos en el año 2021-2014
    rows_replace = [state_name, dayweek_name, month_name, weather, route, lgt_cond, code_state]
    
    # Se reemplaza los valores presentes en cada uno de los elementos de las listas, para normoalizar
    # los dataframes
    data_2011 = data_replace(data_2011, rows_replace)
    data_2012 = data_replace(data_2012, rows_replace)
    data_2013 = data_replace(data_2013, rows_replace)
    data_2014 = data_replace(data_2014, rows_replace)
    
    # Se seleccionan las columnas de interés
    data_2011 = data_2011.loc[:, data_2011.columns[data_2011.columns.isin(cols_filter)]]
    data_2012 = data_2012.loc[:, data_2012.columns[data_2012.columns.isin(cols_filter)]]
    data_2013 = data_2013.loc[:, data_2013.columns[data_2013.columns.isin(cols_filter)]]
    data_2014 = data_2014.loc[:, data_2014.columns[data_2014.columns.isin(cols_filter)]]
    data_2015 = data_2015.loc[:, data_2015.columns[data_2015.columns.isin(cols_filter)]]
    data_2016 = data_2016.loc[:, data_2016.columns[data_2016.columns.isin(cols_filter)]]
    data_2017 = data_2017.loc[:, data_2017.columns[data_2017.columns.isin(cols_filter)]]
    data_2018 = data_2018.loc[:, data_2018.columns[data_2018.columns.isin(cols_filter)]]
    data_2019 = data_2019.loc[:, data_2019.columns[data_2019.columns.isin(cols_filter)]]
    data_2020 = data_2020.loc[:, data_2020.columns[data_2020.columns.isin(cols_filter)]]
    data_2021 = data_2021.loc[:, data_2021.columns[data_2021.columns.isin(cols_filter)]]
    
    # Se concatenan los dataframes
    data_join = pd.concat([data_2011,data_2012,data_2013,data_2014,data_2015,
                           data_2016,data_2017,data_2018,data_2019,data_2020,data_2021])
    
    # Se crean diccionarios asociados al nombre del condado, ciudad y su código respectivo
    county_name = [item.title() for item in county_city_name["County Name"].str.lower().unique()]
    city_name = [item.title() for item in county_city_name["City Name"].str.lower().unique()]
    
    city_code_special = {0: "Not Applicable",
                         9997: "Other",
                         9898: "Not Reported",
                         9999: "Unknown"}
    county_name_code = dict(zip(county_city_name["County Code"].unique(), county_name))
    city_name_code = dict(zip(county_city_name["City Code"].unique(), city_name))
    city_name_code.update(city_code_special)
    rows_replace.append(county_name_code)
    rows_replace.append(city_name_code)
    
    # Se reemplaza los códigos de los condados y ciudades por sus nombres respectivos
    data_join = replace_state_county_city(data_join, rows_replace)
    
    # Se transforma el nombre de las columnas a minúsculas
    data_join.columns = [item.lower() for item in data_join.columns]
    
    # Se reemplaza el nombre de las columnas a nombres legibles
    data_join = data_join.rename(columns=change_name)
    
    # Se exporta el conjunto de datos en formato pickle
    data_join.to_pickle(os.path.join(PATH, "data_accident.pkl"))  

if __name__ == "__main__":
    main()
