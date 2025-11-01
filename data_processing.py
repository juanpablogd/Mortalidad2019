import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json

def load_and_process_data():
    """Carga y procesa todos los datos necesarios para la aplicación"""
    
    print("Cargando datos...")
    
    # 1. Cargar datos de mortalidad
    mortality_data = pd.read_excel('Data/Anexo1.NoFetal2019_CE_15-03-23.xlsx')
    
    # 2. Cargar códigos de muerte
    try:
        # Los datos comienzan en la fila 10
        death_codes = pd.read_excel('Data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx', skiprows=10)
        death_codes.columns = ['CAPITULO', 'NOMBRE_CAPITULO', 'CODIGO_3', 'DESCRIPCION_3', 'CODIGO_4', 'DESCRIPCION_4']
        print(f"Códigos de muerte cargados: {death_codes.shape}")
    except:
        print("Error cargando códigos de muerte, usando datos básicos")
        death_codes = pd.DataFrame()
    
    # 3. Cargar división política
    divipola = pd.read_excel('Data/Divipola_CE_.xlsx')
    
    # 4. Merge con divipola para obtener nombres de departamentos y municipios
    mortality_with_geo = mortality_data.merge(
        divipola, 
        on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], 
        how='left'
    )
    
    print(f"Datos de mortalidad con geografía: {mortality_with_geo.shape}")
    print(f"Departamentos únicos: {mortality_with_geo['DEPARTAMENTO'].nunique()}")
    print(f"Municipios únicos: {mortality_with_geo['MUNICIPIO'].nunique()}")
    
    return mortality_with_geo, death_codes, divipola

def create_mortality_map(df):
    """Crea mapa coroplético de distribución de muertes por departamento"""
    
    # Cargar GeoJSON
    with open('Data/map.geojson', 'r', encoding='utf-8') as f:
        colombia_geojson = json.load(f)
    
    # Extraer códigos disponibles en el GeoJSON
    codigos_geojson = set([feature['properties']['codigo'] for feature in colombia_geojson['features']])
    print(f"Códigos en GeoJSON: {len(codigos_geojson)} departamentos")
    
    # Agrupar por código de departamento
    dept_deaths = df.groupby('COD_DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
    
    # Convertir COD_DEPARTAMENTO a string con formato de 2 dígitos
    dept_deaths['codigo'] = dept_deaths['COD_DEPARTAMENTO'].astype(int).astype(str).str.zfill(2)
    
    # Filtrar solo departamentos que existen en el GeoJSON
    dept_deaths_mapa = dept_deaths[dept_deaths['codigo'].isin(codigos_geojson)].copy()
    
    print(f"Departamentos en datos: {len(dept_deaths)}")
    print(f"Departamentos con geometría en mapa: {len(dept_deaths_mapa)}")
    print("\nTop 10 departamentos con más muertes:")
    print(dept_deaths_mapa.sort_values('TOTAL_MUERTES', ascending=False).head(10)[['codigo', 'TOTAL_MUERTES']])
    
    # Crear diccionario para mapeo rápido
    deaths_dict = dict(zip(dept_deaths_mapa['codigo'], dept_deaths_mapa['TOTAL_MUERTES']))
    
    # Crear mapa con Choroplethmapbox para mejor control
    fig = go.Figure(go.Choroplethmapbox(
        geojson=colombia_geojson,
        locations=dept_deaths_mapa['codigo'],
        z=dept_deaths_mapa['TOTAL_MUERTES'],
        featureidkey="properties.codigo",
        colorscale='Reds',
        zmin=0,
        zmax=dept_deaths_mapa['TOTAL_MUERTES'].max(),
        marker_opacity=0.7,
        marker_line_width=2,
        marker_line_color='white',
        colorbar=dict(title="Total de Muertes"),
        hovertemplate='<b>Código: %{location}</b><br>Muertes: %{z:,}<extra></extra>'
    ))
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4.5,
        mapbox_center={"lat": 4.5709, "lon": -74.2973},
        height=700,
        margin={"r":0,"t":50,"l":0,"b":0},
        title_text='Mapa de Mortalidad por Departamento - Colombia 2019',
        title_x=0.5
    )
    
    return fig

def create_monthly_timeline(df):
    """Crea gráfico de líneas de muertes por mes"""
    
    monthly_deaths = df.groupby('MES').size().reset_index(name='TOTAL_MUERTES')
    
    # Agregar nombres de meses
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
             7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    monthly_deaths['MES_NOMBRE'] = monthly_deaths['MES'].map(meses)
    
    print("Muertes por mes:")
    print(monthly_deaths)
    
    fig = px.line(
        monthly_deaths, 
        x='MES_NOMBRE', 
        y='TOTAL_MUERTES',
        title='Total de Muertes por Mes - Colombia 2019',
        labels={'TOTAL_MUERTES': 'Total de Muertes', 'MES_NOMBRE': 'Mes'},
        markers=True
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    
    return fig

def create_violent_cities_chart(df):
    """Crea gráfico de las 5 ciudades más violentas"""
    
    # Filtrar homicidios (códigos X95 y relacionados)
    homicides = df[df['COD_MUERTE'].str.contains('X95', na=False)]
    
    # Agrupar por municipio
    city_violence = homicides.groupby('MUNICIPIO').size().reset_index(name='HOMICIDIOS')
    city_violence = city_violence.sort_values('HOMICIDIOS', ascending=False).head(5)
    
    print("Top 5 ciudades más violentas:")
    print(city_violence)
    
    fig = px.bar(
        city_violence, 
        x='MUNICIPIO', 
        y='HOMICIDIOS',
        title='5 Ciudades Más Violentas - Homicidios 2019',
        labels={'HOMICIDIOS': 'Número de Homicidios', 'MUNICIPIO': 'Ciudad'},
        color='HOMICIDIOS',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=400
    )
    
    return fig

def create_safest_cities_chart(df):
    """Crea gráfico circular de las 10 ciudades con menor mortalidad"""
    
    # Calcular mortalidad por ciudad (solo ciudades con al menos 100 casos para evitar sesgos)
    city_deaths = df.groupby('MUNICIPIO').size().reset_index(name='TOTAL_MUERTES')
    city_deaths = city_deaths[city_deaths['TOTAL_MUERTES'] >= 100]  # Filtrar ciudades pequeñas
    safest_cities = city_deaths.sort_values('TOTAL_MUERTES', ascending=True).head(10)
    
    print("Top 10 ciudades con menor mortalidad (min 100 casos):")
    print(safest_cities)
    
    fig = px.pie(
        safest_cities, 
        values='TOTAL_MUERTES', 
        names='MUNICIPIO',
        title='10 Ciudades con Menor Índice de Mortalidad'
    )
    
    return fig

def create_death_causes_table(df, death_codes):
    """Crea tabla de las 10 principales causas de muerte"""
    
    # Top 10 causas de muerte
    top_causes = df['COD_MUERTE'].value_counts().head(10).reset_index()
    top_causes.columns = ['CODIGO', 'TOTAL_CASOS']
    
    # Si tenemos los códigos de muerte, hacer merge para obtener descripciones
    if not death_codes.empty:
        try:
            # Crear diccionario de códigos
            codes_dict = {}
            for _, row in death_codes.iterrows():
                if pd.notna(row.get('CODIGO_4')):
                    codes_dict[row['CODIGO_4']] = row.get('DESCRIPCION_4', 'Sin descripción')
            
            top_causes['DESCRIPCION'] = top_causes['CODIGO'].map(codes_dict)
            top_causes['DESCRIPCION'] = top_causes['DESCRIPCION'].fillna('Descripción no disponible')
        except:
            top_causes['DESCRIPCION'] = 'Descripción no disponible'
    else:
        top_causes['DESCRIPCION'] = 'Descripción no disponible'
    
    print("Top 10 causas de muerte:")
    print(top_causes)
    
    return top_causes

def create_gender_by_department_chart(df):
    """Crea gráfico de barras apiladas de muertes por sexo y departamento"""
    
    # Mapear sexos
    sex_map = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
    df_copy = df.copy()
    df_copy['SEXO_NOMBRE'] = df_copy['SEXO'].map(sex_map)
    
    # Agrupar por departamento y sexo
    gender_dept = df_copy.groupby(['DEPARTAMENTO', 'SEXO_NOMBRE']).size().reset_index(name='TOTAL_MUERTES')
    
    # Tomar solo los top 15 departamentos por total de muertes
    top_depts = df_copy.groupby('DEPARTAMENTO').size().sort_values(ascending=False).head(15).index
    gender_dept = gender_dept[gender_dept['DEPARTAMENTO'].isin(top_depts)]
    
    print("Muertes por sexo y departamento (top 15 departamentos):")
    print(gender_dept.head(10))
    
    fig = px.bar(
        gender_dept, 
        x='DEPARTAMENTO', 
        y='TOTAL_MUERTES',
        color='SEXO_NOMBRE',
        title='Muertes por Sexo en cada Departamento (Top 15)',
        labels={'TOTAL_MUERTES': 'Total de Muertes', 'DEPARTAMENTO': 'Departamento', 'SEXO_NOMBRE': 'Sexo'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig

def create_age_groups_histogram(df):
    """Crea histograma de distribución por grupos de edad"""
    
    # Mapear grupos de edad según la tabla de referencia
    age_groups_map = {
        0: 'Mortalidad neonatal (Cod 0-4)', 1: 'Mortalidad neonatal (Cod 0-4)', 2: 'Mortalidad neonatal (Cod 0-4)',
        3: 'Mortalidad neonatal (Cod 0-4)', 4: 'Mortalidad neonatal (Cod 0-4)',
        5: 'Mortalidad infantil (Cod 5-6)', 6: 'Mortalidad infantil (Cod 5-6)',
        7: 'Primera infancia (Cod 7-8)', 8: 'Primera infancia (Cod 7-8)',
        9: 'Ninez (Cod 9-10)', 10: 'Ninez (Cod 9-10)',
        11: 'Adolescencia (Cod 11)',
        12: 'Juventud (Cod 12-13)', 13: 'Juventud (Cod 12-13)',
        14: 'Adultez temprana (Cod 14-16)', 15: 'Adultez temprana (Cod 14-16)', 16: 'Adultez temprana (Cod 14-16)',
        17: 'Adultez intermedia (Cod 17-19)', 18: 'Adultez intermedia (Cod 17-19)', 19: 'Adultez intermedia (Cod 17-19)',
        20: 'Vejez (Cod 20-24)', 21: 'Vejez (Cod 20-24)', 22: 'Vejez (Cod 20-24)', 23: 'Vejez (Cod 20-24)', 24: 'Vejez (Cod 20-24)',
        25: 'Longevidad (Cod 25-28)', 26: 'Longevidad (Cod 25-28)', 27: 'Longevidad (Cod 25-28)', 28: 'Longevidad (Cod 25-28)',
        29: 'Edad desconocida (Cod 29)'
    }
    
    df_copy = df.copy()
    df_copy['GRUPO_EDAD_NOMBRE'] = df_copy['GRUPO_EDAD1'].map(age_groups_map)
    
    # Agrupar por categorías de edad
    age_distribution = df_copy.groupby('GRUPO_EDAD_NOMBRE').size().reset_index(name='TOTAL_MUERTES')
    age_distribution = age_distribution.sort_values('TOTAL_MUERTES', ascending=False)
    
    print("Distribución por grupos de edad:")
    print(age_distribution)
    
    fig = px.bar(
        age_distribution, 
        x='GRUPO_EDAD_NOMBRE', 
        y='TOTAL_MUERTES',
        title='Distribución de Muertes por Grupos de Edad - Colombia 2019',
        labels={'TOTAL_MUERTES': 'Total de Muertes', 'GRUPO_EDAD_NOMBRE': 'Grupo de Edad'},
        color='TOTAL_MUERTES',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=430
    )
    
    return fig

if __name__ == "__main__":
    # Cargar datos
    mortality_data, death_codes, divipola = load_and_process_data()
    
    print("\n" + "="*80)
    print("GENERANDO VISUALIZACIONES...")
    print("="*80 + "\n")
    
    # Generar todas las visualizaciones
    map_fig = create_mortality_map(mortality_data)
    timeline_fig = create_monthly_timeline(mortality_data)
    violent_cities_fig = create_violent_cities_chart(mortality_data)
    safest_cities_fig = create_safest_cities_chart(mortality_data)
    death_causes_table = create_death_causes_table(mortality_data, death_codes)
    gender_dept_fig = create_gender_by_department_chart(mortality_data)
    age_groups_fig = create_age_groups_histogram(mortality_data)
    
    print("\n" + "="*80)
    print("VISUALIZACIONES GENERADAS EXITOSAMENTE")
    print("="*80)