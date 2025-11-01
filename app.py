import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

from data_processing import (
	load_and_process_data,
	create_mortality_map,
	create_monthly_timeline,
	create_violent_cities_chart,
	create_safest_cities_chart,
	create_death_causes_table,
	create_gender_by_department_chart,
	create_age_groups_histogram
)

# Inicializar la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Análisis de Mortalidad en Colombia 2019"
server = app.server  # Para despliegue en PaaS

# Cargar datos
print("Iniciando aplicación...")
print("Cargando datos...")

try:
	mortality_data, death_codes, divipola = load_and_process_data()

	# Generar todas las visualizaciones
	print("Generando visualizaciones...")
	map_fig = create_mortality_map(mortality_data)
	timeline_fig = create_monthly_timeline(mortality_data)
	violent_cities_fig = create_violent_cities_chart(mortality_data)
	safest_cities_fig = create_safest_cities_chart(mortality_data)
	death_causes_df = create_death_causes_table(mortality_data, death_codes)
	gender_dept_fig = create_gender_by_department_chart(mortality_data)
	age_groups_fig = create_age_groups_histogram(mortality_data)

	print("Aplicación lista!")

except Exception as e:
	print(f"Error: {e}")
	# Crear figuras vacías en caso de error
	map_fig = timeline_fig = violent_cities_fig = safest_cities_fig = {}
	gender_dept_fig = age_groups_fig = {}
	death_causes_df = pd.DataFrame([
		{'CODIGO': 'Error', 'TOTAL_CASOS': 0, 'DESCRIPCION': 'Error cargando datos'}
	])
	mortality_data = pd.DataFrame({
		'COD_DEPARTAMENTO': [0],
		'DEPARTAMENTO': ['Error'],
		'MUNICIPIO': ['Error']
	})

# Layout de la aplicación
app.layout = dbc.Container([
	# Encabezado
	dbc.Row([
		dbc.Col([
			html.H1(
				"Análisis de Mortalidad en Colombia 2019",
				className="text-center mb-4",
				style={'color': '#2c3e50', 'fontWeight': 'bold'}
			),
			html.P(
				"Dashboard interactivo para el análisis de datos de mortalidad en Colombia durante el año 2019. "
				"Basado en datos oficiales del DANE (Departamento Administrativo Nacional de Estadística).",
				className="text-center text-muted mb-5"
			),
			html.Hr()
		])
	]),

	# Información académica
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Información del proyecto académico"),
				dbc.CardBody([
					dbc.Row([
						dbc.Col([
							html.Div([
								html.H6("Universidad", className="fw-bold mb-1"),
								html.P("Universidad de La Salle", className="mb-0")
							], className="mb-3"),
							html.Div([
								html.H6("Programa", className="fw-bold mb-1"),
								html.P("Maestría en Inteligencia Artificial 2025-II - Aplicaciones I · Unidad 2", className="mb-0")
							], className="mb-3"),
							html.Div([
								html.H6("Actividad", className="fw-bold mb-1"),
								html.P("Actividad 4 · Aplicación web interactiva para el análisis de mortalidad en Colombia", className="mb-0")
							], className="mb-3")
						], md=6),
						dbc.Col([
							html.Div([
								html.H6("Profesor", className="fw-bold mb-1"),
								html.P("Cristian Duney Bermudez Quintero", className="mb-0")
							], className="mb-3"),
							html.Div([
								html.H6("Estudiantes", className="fw-bold mb-1"),
								html.Ul([
									html.Li("Alexander David Vargas León - alvargas37@unisalle.edu.co"),
									html.Li("Juan Pablo Garzón Dueñas - jgarzon98@unisalle.edu.co"),
									html.Li("Rodolfo Rodríguez Sarmiento - rrodriguez20@unisalle.edu.co")
								], className="mb-0")
							])
						], md=6)
					], className="gy-3")
				])
			], className="mb-4 shadow-sm")
		], md=12)
	]),

	# Estadísticas generales
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4(f"{len(mortality_data):,}", className="card-title text-center"),
					html.P("Total de Defunciones", className="card-text text-center text-muted")
				])
			], color="danger", outline=True)
		], md=3),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4(f"{mortality_data['DEPARTAMENTO'].nunique()}", className="card-title text-center"),
					html.P("Departamentos", className="card-text text-center text-muted")
				])
			], color="warning", outline=True)
		], md=3),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4(f"{mortality_data['MUNICIPIO'].nunique()}", className="card-title text-center"),
					html.P("Municipios", className="card-text text-center text-muted")
				])
			], color="info", outline=True)
		], md=3),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4(
						f"{len(mortality_data[mortality_data['COD_MUERTE'].str.contains('X95', na=False)])}",
						className="card-title text-center"
					),
					html.P("Homicidios", className="card-text text-center text-muted")
				])
			], color="dark", outline=True)
		], md=3),
	], className="mb-4"),

	# Sección 1: Mapa principal de Colombia
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Mapa de Mortalidad por Departamento"),
				dbc.CardBody([
					dcc.Graph(figure=map_fig, style={'height': '70vh'})
				])
			])
		], md=12)
	], className="mb-4"),

	# Sección 2: Evolución temporal
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Evolución Temporal por Mes"),
				dbc.CardBody([
					dcc.Graph(figure=timeline_fig)
				])
			])
		], md=12)
	], className="mb-4"),

	# Sección 3: Ciudades violentas y seguras
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Ciudades Más Violentas (Homicidios)"),
				dbc.CardBody([
					dcc.Graph(figure=violent_cities_fig)
				])
			])
		], md=6),
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Ciudades con Menor Mortalidad"),
				dbc.CardBody([
					dcc.Graph(figure=safest_cities_fig)
				])
			])
		], md=6)
	], className="mb-4"),

	# Sección 4: Tabla de causas de muerte
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Principales Causas de Muerte"),
				dbc.CardBody([
					dash_table.DataTable(
						data=death_causes_df.to_dict('records'),
						columns=[
							{"name": "Código", "id": "CODIGO"},
							{"name": "Total de Casos", "id": "TOTAL_CASOS", "type": "numeric", "format": {"specifier": ","}},
							{"name": "Descripción", "id": "DESCRIPCION"}
						],
						style_cell={'textAlign': 'left', 'padding': '10px'},
						style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
						style_data={'backgroundColor': 'rgb(248, 248, 248)'},
						style_data_conditional=[
							{
								'if': {'row_index': 0},
								'backgroundColor': '#ffebee',
								'color': 'black'
							}
						]
					)
				])
			])
		])
	], className="mb-4"),

	# Sección 5: Análisis por sexo y edad
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Muertes por Sexo en Departamentos"),
				dbc.CardBody([
					dcc.Graph(figure=gender_dept_fig)
				])
			])
		], md=7),
		dbc.Col([
			dbc.Card([
				dbc.CardHeader("Distribución por Grupos de Edad"),
				dbc.CardBody([
					dcc.Graph(figure=age_groups_fig)
				])
			])
		], md=5)
	], className="mb-4"),

	# Footer
	dbc.Row([
		dbc.Col([
			html.Hr(),
			html.P([
				"Trabajo académico - Maestría IA | ",
				html.A("Fuentes: DANE", href="https://www.dane.gov.co/", target="_blank"),
				" | Estadísticas Vitales 2019"
			], className="text-center text-muted small"),
			html.P(
				"Universidad de La Salle · Aplicaciones I · Cohorte 2025-II",
				className="text-center text-muted small"
			)
		])
	])

], fluid=True)

# Callback para interactividad si se requiere en el futuro
# Actualmente todas las visualizaciones son estáticas

if __name__ == '__main__':
    print("Iniciando servidor web...")
    print("Accede a: http://127.0.0.1:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)

