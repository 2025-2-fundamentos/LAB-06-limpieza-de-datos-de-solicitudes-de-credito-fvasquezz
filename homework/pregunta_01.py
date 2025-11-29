"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os 

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    base=base_data()
    base_limpia=limpieza_general(base)
    guardar_datos(base_limpia)


def base_data():
    base=pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")
    return base

def limpieza_general(base):
    base_1=base.copy()
    base_1.drop(columns=["Unnamed: 0"], inplace=True)
    base_1=base_1.dropna()
    base_1=base_1.drop_duplicates()

    columnas_texto=["sexo","tipo_de_emprendimiento","idea_negocio","línea_credito"]
    for col in columnas_texto:
        base_1[col]=(base_1[col].str.lower()
                    .str.replace(r'[-_]'," ", regex=True)
                    .str.strip())    
        
    base_1["barrio"]=base_1["barrio"].str.lower().str.replace(r'[-_]'," ", regex=True)

    columnas_numericas=["comuna_ciudadano","estrato"]
    for col in columnas_numericas:
        base_1[col]=base_1[col].apply(lambda x: str(int(x)))

    base_1["fecha_de_beneficio"]=(base_1["fecha_de_beneficio"]
                              .str.replace("/","-")
                              .str.replace(
                                  r'^(\d{1,2})-(\d{1,2})-(\d{4})$',
                                  r'\3-\2-\1',                       
                                regex=True))
    base_1["fecha_de_beneficio"]=pd.to_datetime(base_1["fecha_de_beneficio"], format="%Y-%m-%d",errors="coerce")

    base_1["monto_del_credito"]=(base_1["monto_del_credito"].
                             str.replace(r'[$,]',"",regex=True).
                             apply(lambda x: float(x)))

    base_1=base_1.drop_duplicates()
    base_1=base_1.dropna()

    return base_1

def guardar_datos(df):
    carpeta_salida="files/output"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    ruta_completa=os.path.join(carpeta_salida,"solicitudes_de_credito.csv")
    df.to_csv(ruta_completa,sep=';',index=False, encoding='utf-8')



