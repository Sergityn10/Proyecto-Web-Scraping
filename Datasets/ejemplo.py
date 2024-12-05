import pandas as pd
import numpy as np
# -------------------------------PRUEBAS---------------------------------------
mi_dataframe =pd.DataFrame()

valor = {
    'Nombre': ['Juan', 'Pedro', 'Maria', 'Juan', 'Pedro'],
    'Apellido': ['Perez', 'Garcia', 'Lopez', 'Perez','Martín']
}

valor_lista = [
    ['Juan', 'Perez'],
    ['Pedro', 'Garcia'],
    ['Maria', 'Lopez'],
    ['Juan', 'Perez'],
    ['Pedro', 'Martín']

]
valor_lista_objetos = [
    {'Nombre': 'Juan', 'Apellido': 'Perez'},
    {'Nombre': 'Pedro', 'Apellido': 'Garcia'},
    {'Nombre': 'Maria', 'Apellido': 'Lopez'},
    {'Nombre': 'Juan', 'Apellido': 'Perez'},
    {'Nombre': 'Pedro', 'Apellido': 'Martín'}

]
# Crear un DataFrame
mi_dataframe = pd.DataFrame(valor)

mi_dataframe.add({
    'Nombre': 'Sergio',
    'Apellido': 'Martín'
})
nuevo_valor = {
    'Nombre': 'Sergio',
    'Apellido': 'Martín',
    'Edad' : 18
}
mi_dataframe.insert(value=[18,18,18,18,18],loc=mi_dataframe.shape[1],column='Edad')
# print(mi_dataframe['Nombre'])

# print(mi_dataframe)

#---------------------------------FUNCION PRINCIPAL------------------------------------------


#Se carga y se crea el Dataframe, a partir de la lista que se ha scrapeado en la web. DEPENDE DE COMO SE MANEJE LA OBTENCIÓN DE LA INFORMACIÓN
#   1- Si se realiza en formato de objetos o diccionarios
#   2- Si se realiza en formato de lista de objetos
#   3- Si se realiza en formato de lista de listas



def crear_dataframe(lista, columnas): #NO HACE FALTA QUE SE UTILIZA ESTA FUNCIÓN. CON UTILIZAR EL CONSTRUCTOR DE DATAFRAMES ES SUFICIENTE. Se puede utilizar si se desea procesar alguna información
                                        #antes de crear el dataframe. Aún así, se puede procesar una vez creada y establecer la limpieza en el dataframe y configurarlo a nuestro antojo.
    #Se crea un diccionario con los datos que se van a insertar en el dataframe
    valor = {}
    for i in range(len(lista)):
        valor[columnas[i]] = lista[columnas[i]]
        
    #Se crea el dataframe
    df = pd.DataFrame(valor)
    return df

# print(range(len(valor_lista)))
df = pd.DataFrame(valor_lista_objetos) #EJEMPLO 
# print(crear_dataframe(valor,columnas))

#---------------------------------------------ESTO SIRVE---------------------------------------------
# Función para limpiar datos nulos y duplicados
def limpiar_datos(df):
    """
    Limpia datos nulos y duplicados en el DataFrame.

    :param df: DataFrame a limpiar.
    :return: DataFrame limpio.
    """
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


columnas = [] #En esta lista, se deben de establecer el nombre de las columnas que vamos a querer establecer en nuestro dataset
columnas = ['Nombre', 'Apellido', 'Edad'] #EJEMPLO
columnas = ['Nombre', 'Apellido'] #EJEMPLO
# 1- SE CREAR EL DATAFRAME A PARTIR DEL WEB SCRAPING.
# 2- SE LIMPIA LOS DATOS
# 3- SE GUARDAN LOS DATOS EN UN ARCHIVO EXCEL Y JSON.
ruta_json = 'datos.json'
ruta_csv = 'datos.csv'
ruta_excel = 'datos.xlsx'
#Con el constructor por defecto, se pueden crear dataframes de cualquier forma, ya sea a partir de una lista de listas, lista de objetos, diccionarios.
df = pd.DataFrame(valor_lista, columns=columnas) #EJEMPLO de lista de listas
print(f"EJemplo de lista de listas \n {df}")
df = pd.DataFrame(valor, columns=columnas) #EJEMPLO diccionario
print(f"EJemplo de diccionario \n {df}")
df = pd.DataFrame(valor_lista_objetos, columns=columnas) #EJEMPLO 
print(f"EJemplo de lista de objetos \n {df}")

#2 - SE LIMPIAN LOS DATOS
df = limpiar_datos(df)

#3 - SE GUARDAN LOS DATOS EN UN ARCHIVO EXCEL Y JSON, O CSV
guardar_datos(df, ruta_excel=ruta_excel, ruta_json=ruta_json) 
df.to_csv(ruta_csv)
# Supongamos que ya tenemos el DataFrame cargado como `df`
# df = pd.read_csv("ruta_a_tu_dataset.csv")


def almacenamiento_dataframe(datos):
    ruta_json = 'datos.json'
    ruta_csv = 'datos.csv'
    ruta_excel = 'datos.xlsx'
    #Con el constructor por defecto, se pueden crear dataframes de cualquier forma, ya sea a partir de una lista de listas, lista de objetos, diccionarios.
    df = pd.DataFrame(datos, columns=columnas) #EJEMPLO de lista de listas
    print(f"EJemplo de lista de listas \n {df}")
    df = pd.DataFrame(datos, columns=columnas) #EJEMPLO diccionario
    print(f"EJemplo de diccionario \n {df}")
    df = pd.DataFrame(valor_lista_objetos, columns=columnas) #EJEMPLO 
    print(f"EJemplo de lista de objetos \n {df}")

    #2 - SE LIMPIAN LOS DATOS
    df = limpiar_datos(df)

    #3 - SE GUARDAN LOS DATOS EN UN ARCHIVO EXCEL Y JSON, O CSV
    guardar_datos(df, ruta_excel=ruta_excel, ruta_json=ruta_json) 
    df.to_csv(ruta_csv)
    # Supongamos que ya tenemos el DataFrame cargado como `df`
    # df = pd.read_csv("ruta_a_tu_dataset.csv")