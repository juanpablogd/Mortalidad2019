# Instrucciones de Despliegue

## Despliegue en Render.com (Recomendado)

### Pasos para desplegar

1. Preparar repositorio:
   - Asegurar que todos los archivos estén en GitHub
   - Verificar que `requirements.txt` y `Procfile` estén presentes

2. Crear cuenta en Render:
   - Ir a https://render.com
   - Registrarse con GitHub

3. Configurar Web Service:
   - Seleccionar "New Web Service"
   - Conectar repositorio de GitHub
   - Configurar:
     - Name: `mortalidad-colombia-2019`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:server`
     - Instance Type: `Free`

4. Variables de entorno (opcional):
   ```
   PYTHON_VERSION=3.8.10
   ```

5. Desplegar:
   - Hacer clic en "Create Web Service"
   - Esperar el proceso de build (5-10 minutos aproximadamente)

### URL de ejemplo
`https://mortalidad-colombia-2019.onrender.com`

---

## Despliegue en Railway.app

1. Conectar repositorio:
   - Ir a https://railway.app
   - Conectar con GitHub
   - Seleccionar repositorio

2. Configuración automática:
   - Railway detecta automáticamente Python
   - Usa el Procfile para el comando de inicio

3. Variables de entorno:
   ```
   PORT=8050
   ```

---

## Despliegue en Heroku

```bash
# Instalar Heroku CLI
# Crear aplicación
heroku create mortalidad-colombia-2019

# Configurar variables
heroku config:set PYTHON_VERSION=3.8.10

# Desplegar
git push heroku main

# Abrir aplicación
heroku open
```

---

## Checklist Pre-Despliegue

- requirements.txt actualizado
- Procfile creado
- app.py con server = app.server
- Datos en carpeta Data/
- README.md documentado
- Repositorio en GitHub

---

## Solución de Problemas

### Error: "Application failed to bind to port"
- Verificar que el Procfile use: `web: gunicorn app:server`
- Asegurar que `server = app.server` esté en app.py

### Error: "Module not found"
- Verificar que todas las librerías estén en requirements.txt
- Usar versiones específicas (ej: pandas==2.1.4)

### Carga lenta de datos
- Los archivos Excel son grandes (aproximadamente 50MB)
- El primer arranque puede tardar 2-3 minutos
- Considerar usar CSV para mejor rendimiento

---

## Monitoreo

- Logs: Revisar logs de la plataforma para errores
- Métricas: Monitorear uso de memoria (los datos requieren aproximadamente 500MB)
- Rendimiento: Primera carga lenta, subsecuentes más rápidas