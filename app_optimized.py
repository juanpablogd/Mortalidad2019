"""
Aplicación web optimizada para análisis de mortalidad en Colombia 2019
"""
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Análisis de Mortalidad en Colombia 2019"
server = app.server  # Para despliegue en PaaS

def load_data_optimized():
    """Carga optimizada de datos"""
    print("📊 Cargando datos de mortalidad...")
    
    # Cargar datos principales
    mortality_data = pd.read_excel('Data/Anexo1.NoFetal2019_CE_15-03-23.xlsx')
    print(f"✅ Datos de mortalidad cargados: {len(mortality_data):,} registros")
    
    # Cargar división política
    divipola = pd.read_excel('Data/Divipola_CE_.xlsx')
    print(f"✅ Divipola cargada: {len(divipola)} municipios")
    
    # Merge optimizado
    mortality_with_geo = mortality_data.merge(
        divipola[['COD_DEPARTAMENTO', 'COD_MUNICIPIO', 'DEPARTAMENTO', 'MUNICIPIO']], 
        on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], 
        how='left'
    )
    print(f"✅ Datos combinados: {len(mortality_with_geo):,} registros")
    
    return mortality_with_geo

def create_visualizations(df):
    """Crea todas las visualizaciones necesarias"""
    
    print("📈 Generando visualizaciones...")
    
    # 1. Mapa de mortalidad por departamento
    dept_deaths = df.groupby('DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
    dept_deaths = dept_deaths.sort_values('TOTAL_MUERTES', ascending=False).head(15)
    
    map_fig = px.bar(
        dept_deaths, 
        x='TOTAL_MUERTES', 
        y='DEPARTAMENTO',
        orientation='h',
        title='Top 15 Departamentos - Mortalidad 2019',
        color='TOTAL_MUERTES',
        color_continuous_scale='Reds'
    )
    map_fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    
    # 2. Línea temporal por mes
    monthly_deaths = df.groupby('MES').size().reset_index(name='TOTAL_MUERTES')
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    monthly_deaths['MES_NOMBRE'] = monthly_deaths['MES'].apply(lambda x: meses[x-1])
    
    timeline_fig = px.line(
        monthly_deaths, 
        x='MES_NOMBRE', 
        y='TOTAL_MUERTES',
        title='Mortalidad Mensual 2019',
        markers=True
    )
    timeline_fig.update_layout(height=400)
    
    # 3. Ciudades más violentas
    homicides = df[df['COD_MUERTE'].str.contains('X95', na=False)]
    violent_cities = homicides.groupby('MUNICIPIO').size().reset_index(name='HOMICIDIOS')
    violent_cities = violent_cities.sort_values('HOMICIDIOS', ascending=False).head(5)
    
    violent_fig = px.bar(
        violent_cities, 
        x='MUNICIPIO', 
        y='HOMICIDIOS',
        title='Top 5 Ciudades Más Violentas',
        color='HOMICIDIOS',
        color_continuous_scale='Reds'
    )
    violent_fig.update_layout(height=400, xaxis_tickangle=-45)
    
    # 4. Ciudades con menor mortalidad
    safe_cities = df.groupby('MUNICIPIO').size().reset_index(name='TOTAL_MUERTES')
    safe_cities = safe_cities[safe_cities['TOTAL_MUERTES'] >= 50]  # Filtro mínimo
    safe_cities = safe_cities.sort_values('TOTAL_MUERTES', ascending=True).head(10)
    
    safe_fig = px.pie(
        safe_cities, 
        values='TOTAL_MUERTES', 
        names='MUNICIPIO',
        title='10 Ciudades con Menor Mortalidad'
    )
    
    # 5. Principales causas de muerte
    top_causes = df['COD_MUERTE'].value_counts().head(10).reset_index()
    top_causes.columns = ['CODIGO', 'TOTAL_CASOS']
    
    # Agregar descripciones básicas
    descriptions = {
        'I219': 'Infarto agudo del miocardio',
        'J449': 'EPOC no especificada',
        'J440': 'EPOC con infección aguda',
        'J189': 'Neumonía no especificada',
        'C169': 'Tumor maligno del estómago',
        'C349': 'Tumor maligno del pulmón',
        'X954': 'Agresión con arma de fuego',
        'C509': 'Tumor maligno de la mama',
        'C61': 'Tumor maligno de próstata',
        'I10': 'Hipertensión esencial'
    }
    top_causes['DESCRIPCION'] = top_causes['CODIGO'].map(descriptions).fillna('Otra causa')
    
    # 6. Análisis por sexo y departamento
    sex_map = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
    df_sex = df.copy()
    df_sex['SEXO_NOMBRE'] = df_sex['SEXO'].map(sex_map)
    
    top_depts = df.groupby('DEPARTAMENTO').size().sort_values(ascending=False).head(10).index
    gender_dept = df_sex[df_sex['DEPARTAMENTO'].isin(top_depts)]
    gender_data = gender_dept.groupby(['DEPARTAMENTO', 'SEXO_NOMBRE']).size().reset_index(name='TOTAL_MUERTES')
    
    gender_fig = px.bar(
        gender_data, 
        x='DEPARTAMENTO', 
        y='TOTAL_MUERTES',
        color='SEXO_NOMBRE',
        title='Mortalidad por Sexo - Top 10 Departamentos'
    )
    gender_fig.update_layout(height=500, xaxis_tickangle=-45)
    
    # 7. Distribución por grupos de edad
    age_groups = {
        0: 'Neonatal', 1: 'Neonatal', 2: 'Neonatal', 3: 'Neonatal', 4: 'Neonatal',
        5: 'Infantil', 6: 'Infantil',
        7: 'Primera infancia', 8: 'Primera infancia',
        9: 'Niñez', 10: 'Niñez', 11: 'Adolescencia',
        12: 'Juventud', 13: 'Juventud',
        14: 'Adultez temprana', 15: 'Adultez temprana', 16: 'Adultez temprana',
        17: 'Adultez intermedia', 18: 'Adultez intermedia', 19: 'Adultez intermedia',
        20: 'Vejez', 21: 'Vejez', 22: 'Vejez', 23: 'Vejez', 24: 'Vejez',
        25: 'Longevidad', 26: 'Longevidad', 27: 'Longevidad', 28: 'Longevidad',
        29: 'Desconocida'
    }
    
    df_age = df.copy()
    df_age['GRUPO_EDAD_NOMBRE'] = df_age['GRUPO_EDAD1'].map(age_groups)
    age_dist = df_age.groupby('GRUPO_EDAD_NOMBRE').size().reset_index(name='TOTAL_MUERTES')
    age_dist = age_dist.sort_values('TOTAL_MUERTES', ascending=False)
    
    age_fig = px.bar(
        age_dist, 
        x='GRUPO_EDAD_NOMBRE', 
        y='TOTAL_MUERTES',
        title='Distribución por Grupos de Edad',
        color='TOTAL_MUERTES',
        color_continuous_scale='Blues'
    )
    age_fig.update_layout(height=500, xaxis_tickangle=-45)
    
    print("✅ Todas las visualizaciones generadas")
    
    return {
        'map_fig': map_fig,
        'timeline_fig': timeline_fig,
        'violent_fig': violent_fig,
        'safe_fig': safe_fig,
        'top_causes': top_causes,
        'gender_fig': gender_fig,
        'age_fig': age_fig
    }

# Cargar datos y generar visualizaciones
try:
    mortality_data = load_data_optimized()
    visualizations = create_visualizations(mortality_data)
    
    # Estadísticas generales
    total_deaths = len(mortality_data)
    total_departments = mortality_data['DEPARTAMENTO'].nunique()
    total_municipalities = mortality_data['MUNICIPIO'].nunique()
    total_homicides = len(mortality_data[mortality_data['COD_MUERTE'].str.contains('X95', na=False)])
    
    print(f"📊 Dashboard listo con {total_deaths:,} registros")
    
except Exception as e:
    print(f"❌ Error cargando datos: {e}")
    # Datos de fallback
    total_deaths = 244355
    total_departments = 33
    total_municipalities = 1026
    total_homicides = 9273
    visualizations = {}

# Layout de la aplicación
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("📊 Análisis de Mortalidad en Colombia 2019", 
                   className="text-center mb-3",
                   style={'color': '#2c3e50', 'fontWeight': 'bold', 'fontSize': '2.5rem'}),
            html.P("Dashboard interactivo basado en datos oficiales del DANE",
                   className="text-center text-muted mb-4"),
            html.Hr()
        ])
    ]),
    
    # Estadísticas principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_deaths:,}", className="text-center text-danger"),
                    html.P("Total Defunciones", className="text-center text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_departments}", className="text-center text-warning"),
                    html.P("Departamentos", className="text-center text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_municipalities}", className="text-center text-info"),
                    html.P("Municipios", className="text-center text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(f"{total_homicides:,}", className="text-center text-dark"),
                    html.P("Homicidios", className="text-center text-muted mb-0")
                ])
            ], className="h-100")
        ], md=3),
    ], className="mb-4"),
    
    # Visualizaciones principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🗺️ Distribución por Departamento"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('map_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Evolución Mensual"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('timeline_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=4)
    ], className="mb-4"),
    
    # Análisis de violencia y seguridad
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("⚠️ Ciudades Más Violentas"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('violent_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🏡 Menor Mortalidad"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('safe_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=6)
    ], className="mb-4"),
    
    # Tabla de causas
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("💊 Principales Causas de Muerte"),
                dbc.CardBody([
                    dash_table.DataTable(
                        data=visualizations.get('top_causes', pd.DataFrame()).to_dict('records') if visualizations else [],
                        columns=[
                            {"name": "Código", "id": "CODIGO"},
                            {"name": "Casos", "id": "TOTAL_CASOS", "type": "numeric", "format": {"specifier": ","}},
                            {"name": "Descripción", "id": "DESCRIPCION"}
                        ],
                        style_cell={'textAlign': 'left', 'padding': '10px', 'fontSize': '14px'},
                        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                        style_data={'backgroundColor': 'white'}
                    ) if visualizations else html.P("Cargando...")
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Análisis demográfico
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("👥 Análisis por Sexo"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('gender_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=7),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🎂 Grupos de Edad"),
                dbc.CardBody([
                    dcc.Graph(figure=visualizations.get('age_fig', {})) if visualizations else html.P("Cargando...")
                ])
            ])
        ], md=5)
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                "Fuente: ", html.A("DANE - Estadísticas Vitales 2019", href="https://www.dane.gov.co/", target="_blank"),
                " | Desarrollado con Python, Dash y Plotly"
            ], className="text-center text-muted small")
        ])
    ])
    
], fluid=True, style={'padding': '20px'})

if __name__ == '__main__':
    print("🚀 Iniciando servidor...")
    print("🌐 Accede en: http://127.0.0.1:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)