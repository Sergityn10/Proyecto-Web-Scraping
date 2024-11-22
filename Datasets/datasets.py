import pandas as pd
import numpy as np


def crear_dataframe(lista, columnas): #NO HACE FALTA QUE SE UTILIZA ESTA FUNCIÓN. CON UTILIZAR EL CONSTRUCTOR DE DATAFRAMES ES SUFICIENTE. Se puede utilizar si se desea procesar alguna información
                                        #antes de crear el dataframe. Aún así, se puede procesar una vez creada y establecer la limpieza en el dataframe y configurarlo a nuestro antojo.
    #Se crea un diccionario con los datos que se van a insertar en el dataframe
    valor = {}
    for i in range(len(lista)):
        valor[columnas[i]] = lista[columnas[i]]
        
    #Se crea el dataframe
    df = pd.DataFrame(valor)
    return df


#---------------------------------------------ESTO SIRVE---------------------------------------------


def convertir_columnas_hasheables(df,nombre_columna):
    df[nombre_columna] = df[nombre_columna].apply(lambda x: str(x) if isinstance(x, list) else x)
    

# Función para limpiar datos nulos y duplicados
def limpiar_datos(df):
    """
    Limpia datos nulos y duplicados en el DataFrame.

    :param df: DataFrame a limpiar.
    :return: DataFrame limpio.
    """
    #SE COMPRUEBA QUE TODAS LAS COLUMNAS SON HASHEABLES
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            print(f"La columna '{col}' tiene valores no hashables.")
            print("Concivertiendo la columna en valores hasheables")
            convertir_columnas_hasheables(df,col)

    # Eliminar duplicados
    df = df.drop_duplicates()
    
    # Rellenar valores nulos con métodos adecuados (media, moda, etc.)
    for column in df.columns:
        if df[column].isnull().sum() > 0:
            if df[column].dtype == "object":
                df[column].fillna(df[column].mode()[0], inplace=True)  # Rellenar con la moda
            else:
                df[column].fillna(df[column].mean(), inplace=True)  # Rellenar con la media
    print("Datos nulos y duplicados eliminados.")

    return df
# Función para guardar el DataFrame en distintos formatos
def guardar_datos(df, ruta_excel, ruta_json):
    """
    Guarda el DataFrame en archivos Excel y JSON.

    :param df: DataFrame a guardar.
    :param ruta_excel: Ruta para guardar el archivo Excel.
    :param ruta_json: Ruta para guardar el archivo JSON.
    """
    # Guardar en Excel
    df.to_excel(ruta_excel, index=False) #Index = False para que no se guarden como una columna el índice de cada tupla.
    print(f"Datos guardados en formato Excel en {ruta_excel}.")

    # Guardar en JSON
    df.to_json(ruta_json, orient="records", lines=True)
    print(f"Datos guardados en formato JSON en {ruta_json}.")




def almacenamiento_dataframe(datos, columnas=[]):
    # 1- SE CREAR EL DATAFRAME A PARTIR DEL WEB SCRAPING.
# 2- SE LIMPIA LOS DATOS
# 3- SE GUARDAN LOS DATOS EN UN ARCHIVO EXCEL Y JSON.
    ruta_json = 'datos.json'
    ruta_csv = 'datos.csv'
    ruta_excel = 'datos.xlsx'
    #1- Con el constructor por defecto, se pueden crear dataframes de cualquier forma, ya sea a partir de una lista de listas, lista de objetos, diccionarios.
    if columnas:
        df = pd.DataFrame(datos, columns=columnas) 
    else:
        df = pd.DataFrame(datos)
    
    #2 - SE LIMPIAN LOS DATOS
    df = limpiar_datos(df)

    #3 - SE GUARDAN LOS DATOS EN UN ARCHIVO EXCEL Y JSON, O CSV
    guardar_datos(df, ruta_excel=ruta_excel, ruta_json=ruta_json) 
    df.to_csv(ruta_csv)