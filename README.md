# Explorando las condiciones que conllevan a la accidentalidad en las carreteras de los Estados Unidos

## [Contenido](#Contenido)

- [Introducción](#Introducción)
- [Instalación](#Instalación)
- [Requisitos](#Requisitos)
- [Uso](#Uso)
- [Estructura del repositorio](#Estructura-del-repositorio)
- [Resultados](#Resultados)
- [Licencia](#Licencia)
- [Autor](#Autor)

## Introducción

El presente proyecto hace parte de la práctica final de la Asignatura Visualización de Datos del [Máster Universitario en Ciencia de Datos de la UOC](https://www.uoc.edu/es/estudios/masters/master-universitario-data-science). 

El conjunto de datos seleccionado se deriva de los reportes de la [Administración Nacional  de Seguridad del Tráfico en las Carreteras](https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/), cuya compilación de informes se crearon para los Estados Unidos, con el objetivo de proporcionar una medida global de la seguridad de las carreteras. Para el desarrollo de este proyecto se ha considerado los datos del periodo 2011-2021.

Con base en esta información se implementa un dashboard con python y la librería [streamlit](https://streamlit.io/), donde se presentan distintas visualizaciones interactivas cuyo propósito es explorar e identificar 
las condiciones que conllevan a un mayor o menor grado de accidentalidad en las carreteras de los Estados Unidos. 

## Instalación

## Requisitos

Para la ejecución de la aplicación es necesario instalar  [python 3.9.16](https://www.python.org/downloads/release/python-3916/) y los paquetes incluidos en el archivo [requeriments.txt](https://github.com/jhontd03/accidentapp/blob/master/requirements.txt). 
Para usuarios de windows se recomienda usar el emulador de la terminal de comandos [cmder](https://cmder.app/)  similar al bash de linux. 

En caso que el archivo python.exe no se puede ejectuar desde la terminal de comandos, es necesario que los usuarios de windows agreguen el directorio de instalación de python a las variables de entorno, tal como se describe
en el siguiente [tutorial.](https://realpython.com/add-python-to-path/)

## Uso

Clone el presente repositorio cree un entorno virtual, instale los paquetes y ejecute el código python directamente.

```
git clone https://github.com/jhontd03/accidentapp.git
cd accidentapp
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app_main.py
```

## Estructura del repositorio

El árbol de directorios del repositorio es el siguiente:
```
.
¦   app_main.py
¦   common.py
¦   EDA_accident.ipynb
¦   etl_process.py
¦   graphs.py
¦   rename.py
¦   __init__.py
¦   
+---.ipynb_checkpoints
¦       EDA_accident-checkpoint.ipynb
¦       
+---data
¦   ¦   data_accident.pkl
¦   ¦   
¦   +---accident_data
¦   ¦       accident_2011.CSV
¦   ¦       accident_2012.csv
¦   ¦       accident_2013.csv
¦   ¦       accident_2014.csv
¦   ¦       accident_2015.csv
¦   ¦       accident_2016.CSV
¦   ¦       accident_2017.CSV
¦   ¦       accident_2018.csv
¦   ¦       accident_2019.CSV
¦   ¦       accident_2020.CSV
¦   ¦       accident_2021.csv
¦   ¦       
¦   +---additional_data
¦           FRPP_GLC_-_United_States_may_9__2023.xlsx
¦           
+---__pycache__
        columns_selection.cpython-39.pyc
        common.cpython-39.pyc
        graphs.cpython-39.pyc
```

## Resultados

Se obtuvo un dashboard que permite explorar de forma interactiva distintas variables del conjunto de datos, con lo cual se identifican algunas condiciones en las que se presentan accidentes de transito en Estados Unidos. El dashboard tambien incluye mapas que permiten explorar la ubicación geográfica de los accidentes en los distitos estados, condados y ciudades de los Estados Unidos. El dashboard se puede ejecutar directamente desde linea de [comandos,](#Uso) o a traves del siguiente [enlace.](https://jhontd03-accidentapp-app-main-dnkwms.streamlit.app/)

## Licencia

El código del presente proyecto se distribuye bajo licencia [MIT](https://github.com/jhontd03/accidentapp/blob/master/LICENSE). Por la presente se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados (el "Software"), para comerciar con el Software sin restricciones, incluyendo sin limitación los derechos de uso, copia, modificación, fusión, publicación, distribución, sublicencia y/o venta de copias del Software.


## Autor

Jhon Jairo Realpe

jrealpe0@uoc.edu
