import pandas as pd
import numpy as np

def explore_data():
    """Explora la estructura de los datos de mortalidad"""
    
    print("=== EXPLORACIÓN DE DATOS DE MORTALIDAD COLOMBIA 2019 ===\n")
    
    # Cargar datos de mortalidad
    print("1. Cargando datos de mortalidad...")
    mortality_data = pd.read_excel('Data/Anexo1.NoFetal2019_CE_15-03-23.xlsx')
    print(f"Dimensiones: {mortality_data.shape}")
    print(f"Columnas: {list(mortality_data.columns)}")
    print(f"Primeras 5 filas:")
    print(mortality_data.head())
    print(f"Tipos de datos:")
    print(mortality_data.dtypes)
    print("\n" + "="*80 + "\n")
    
    # Cargar códigos de muerte
    print("2. Cargando códigos de muerte...")
    death_codes = pd.read_excel('Data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx')
    print(f"Dimensiones: {death_codes.shape}")
    print(f"Columnas: {list(death_codes.columns)}")
    print(f"Primeras 5 filas:")
    print(death_codes.head())
    print("\n" + "="*80 + "\n")
    
    # Cargar división político-administrativa
    print("3. Cargando división político-administrativa...")
    divipola = pd.read_excel('Data/Divipola_CE_.xlsx')
    print(f"Dimensiones: {divipola.shape}")
    print(f"Columnas: {list(divipola.columns)}")
    print(f"Primeras 5 filas:")
    print(divipola.head())
    print("\n" + "="*80 + "\n")
    
    # Análisis específico de mortalidad
    print("4. Análisis específico de datos de mortalidad...")
    
    # Ver valores únicos de algunas columnas clave
    print("Valores únicos en SEXO:")
    print(mortality_data['SEXO'].value_counts())
    print("\nValores únicos en GRUPO_EDAD1:")
    print(mortality_data['GRUPO_EDAD1'].value_counts().sort_index())
    print("\nRango de fechas (MES):")
    print(f"Min: {mortality_data['MES'].min()}, Max: {mortality_data['MES'].max()}")
    
    # Ver valores únicos en COD_MUERTE
    print("\nPrimeros 10 códigos de muerte más frecuentes:")
    print(mortality_data['COD_MUERTE'].value_counts().head(10))
    
    # Verificar códigos de homicidios en los datos de mortalidad
    print("\nBúsqueda de códigos de homicidios (X95):")
    x95_codes = mortality_data[mortality_data['COD_MUERTE'].str.contains('X95', na=False)]
    print(f"Casos con código X95: {len(x95_codes)}")
    
    # Verificar estructura del archivo de códigos de muerte
    print("\nEstructura del archivo de códigos de muerte:")
    # Intentar cargar desde diferentes filas para encontrar la estructura correcta
    for skip_rows in [0, 5, 10, 15]:
        try:
            death_codes_test = pd.read_excel('Data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx', skiprows=skip_rows)
            print(f"Saltando {skip_rows} filas:")
            print(f"Columnas: {list(death_codes_test.columns)}")
            print(f"Primeras 3 filas:")
            print(death_codes_test.head(3))
            print("-" * 40)
        except:
            continue
    
    print("\n" + "="*80 + "\n")
    print("Exploración completada!")

if __name__ == "__main__":
    explore_data()