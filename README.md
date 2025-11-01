# Análisis de Mortalidad en Colombia 2019

Aplicación web interactiva desarrollada con Python, Plotly y Dash para analizar los datos de mortalidad en Colombia durante el año 2019. Los datos utilizados provienen de fuentes oficiales del DANE.

## Características

### Visualizaciones Implementadas

1. Mapa de Mortalidad: Distribución de muertes por departamento
2. Gráfico Temporal: Evolución mensual de la mortalidad
3. Ciudades Violentas: Top 5 de ciudades con más homicidios
4. Ciudades Seguras: 10 ciudades con menor índice de mortalidad
5. Tabla de Causas: Principales causas de muerte con códigos CIE-10
6. Análisis por Sexo: Comparación de muertes por género y departamento
7. Grupos de Edad: Distribución por rangos etarios según clasificación DANE

## Estructura del Proyecto

```
Mortalidad2019/
├── Data/
│   ├── Anexo1.NoFetal2019_CE_15-03-23.xlsx
│   ├── Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx
│   ├── Divipola_CE_.xlsx
│   └── map.geojson
├── app.py                 # Aplicación principal Dash
├── app_optimized.py      # Versión optimizada de la aplicación
├── data_processing.py     # Procesamiento y visualizaciones
├── data_exploration.py    # Exploración inicial de datos
├── requirements.txt       # Dependencias Python
├── runtime.txt           # Versión de Python para despliegue
├── Procfile              # Configuración para despliegue
├── DEPLOY.md             # Guía de despliegue
└── README.md
```

## Instalación y Ejecución Local

### Requisitos previos
- Python 3.9 o superior
- pip

### Pasos para ejecutar localmente

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/juanpablogd/Mortalidad2019.git
   cd Mortalidad2019
   ```

2. Crear entorno virtual:
   ```bash
   python -m venv .venv
   ```

3. Activar entorno virtual:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

6. Acceder a la aplicación:
   Abrir navegador en: `http://127.0.0.1:8050`

## Aplicación Desplegada

La aplicación está disponible en línea en: **https://mortalidad2019.onrender.com/**

Para más información sobre el despliegue, consultar el archivo `DEPLOY.md`

## Fuentes de Datos

- DANE: Departamento Administrativo Nacional de Estadística
- Dataset: Estadísticas Vitales - EEVV 2019
- Cobertura: Colombia, año 2019
- Registros: 244,355 defunciones no fetales

## Principales Hallazgos

### Datos Relevantes

- Departamento con más muertes: Bogotá D.C. (38,760 casos)
- Mes con mayor mortalidad: Enero (21,354 casos)
- Principal causa de muerte: Infarto agudo del miocardio (35,088 casos)
- Ciudad más violenta: Santiago de Cali (971 homicidios)
- Grupo etario más afectado: Vejez 60-84 años (115,453 casos)

## Metodología

### Procesamiento de Datos
1. Carga de archivos Excel con pandas
2. Limpieza y validación de datos
3. Merge de tablas por códigos geográficos
4. Clasificación de grupos etarios según estándares DANE
5. Generación de visualizaciones interactivas con Plotly

### Clasificación de Edad
- Mortalidad neonatal: 0-4 (DANE: 0-4)
- Mortalidad infantil: 5-6 (DANE: 5-6)
- Primera infancia: 7-8 (DANE: 7-8)
- Niñez: 9-10 (DANE: 9-10)
- Adolescencia: 11 (DANE: 11)
- Juventud: 12-13 (DANE: 12-13)
- Adultez temprana: 14-16 (DANE: 14-16)
- Adultez intermedia: 17-19 (DANE: 17-19)
- Vejez: 20-24 (DANE: 20-24)
- Longevidad: 25-28 (DANE: 25-28)

## Códigos de Homicidios

Análisis basado en códigos CIE-10:
- X95: Agresión con disparo de armas de fuego
- X954: Agresión con disparo de otras armas de fuego
- Total de homicidios analizados: 9,273 casos

## Tecnologías Utilizadas

- Python 3.9: Lenguaje principal
- Dash 2.17: Framework web interactivo
- Plotly 5.17: Visualizaciones dinámicas
- Pandas 2.1: Manipulación de datos
- Bootstrap: Diseño responsivo
- Gunicorn: Servidor WSGI para producción
- Render.com: Plataforma de despliegue

## Información del Proyecto

Trabajo académico desarrollado para el curso de Aplicaciones I, Maestría en Inteligencia Artificial, Universidad de La Salle, Cohorte 2025-II.

El proyecto se enfoca en el análisis y visualización de datos de mortalidad en Colombia para el año 2019, utilizando datos públicos del DANE.
