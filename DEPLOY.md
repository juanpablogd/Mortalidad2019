# Instrucciones de Despliegue

## Despliegue en Render.com

**URL de la aplicación:** https://mortalidad2019.onrender.com/

### Configuración utilizada

**Repositorio:** juanpablogd/Mortalidad2019  
**Plataforma:** Render.com  
**Tipo:** Web Service  

### Configuración del servicio

```
Name: mortalidad2019
Environment: Python 3
Region: Oregon (US West)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:server
Instance Type: Free
```

### Archivos de configuración necesarios

**Procfile:**
```
web: gunicorn app:server
```

**runtime.txt:**
```
python-3.9.18
```

**requirements.txt:**
```
dash==2.17.1
plotly==5.17.0
pandas==2.1.4
openpyxl==3.1.2
dash-bootstrap-components==1.5.0
numpy==1.26.2
kaleido==0.2.1
gunicorn==21.2.0
```

### Configuración de puerto

La aplicación utiliza la variable de entorno PORT que Render asigna automáticamente:

```python
import os
port = int(os.environ.get('PORT', 8050))
app.run(debug=False, host='0.0.0.0', port=port)
```

### Pasos para desplegar

1. Crear cuenta en Render.com
2. Conectar repositorio de GitHub
3. Crear nuevo Web Service
4. Configurar según especificaciones arriba
5. Hacer deploy

### Problemas solucionados durante el despliegue

**Error de compatibilidad de Python:**
- pandas 2.1.4 requiere Python 3.9 o superior
- Solución: actualizar runtime.txt a python-3.9.18

**Error de puerto:**
- Render no detectaba el puerto de la aplicación
- Solución: configurar PORT desde variable de entorno

**Start command incorrecto:**
- Usar gunicorn app:server donde server = app.server está definido en app.py

### Especificaciones técnicas

**Datos procesados:**
- 244,355 registros de mortalidad no fetal 2019
- 33 departamentos de Colombia
- 1,026 municipios únicos
- Archivos: 3 Excel + 1 GeoJSON (aproximadamente 50MB total)

**Rendimiento:**
- Build time: 3-5 minutos
- Primera carga: 30-60 segundos
- Memoria utilizada: aproximadamente 500MB

### Información del proyecto

**Universidad:** Universidad de La Salle  
**Programa:** Maestría en Inteligencia Artificial  
**Materia:** Aplicaciones I  
**Cohorte:** 2025-II  

**Fuente de datos:** DANE - Estadísticas Vitales EEVV 2019  
**Tipo:** Análisis de datos públicos de mortalidad en Colombia