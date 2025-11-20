# VENSIM TO PYTHON (Python 3.9.7)

## Configuracion del servidor

- Tener tu servidor local (Preferencia Xampp) iniciando Apache y Mysql
- Dentro del directorio publico de tu servidor crear la ruta assets/vensim/
- Dentro de la ruta creada colocar el vensim con nombre document.mdl (hay un archivo de ejemplo en Backup)
- Dentro del servidor (Admin en Mysql) y ejecutar el archivo vensimweb.sql (el archivo se encuentra en Backup)
- Si configuras de distinta manera actualizar el .env

## Implementación

- Paso 1: Ejecutar comando: pip install -r requeriments.txt
- Paso intermedio: Tener cuenta en Ngrok y configurar el API en app.py, pero puede usar el api introducido (cuenta prueba Ngrok en Backup)
- Paso 2: Ejecutar comando: py app.py
- Paso 3: Podra visualizarlo en http://127.0.0.1:5000/ y en la url de ngrok que es publica en red para compartir por 2 horas cada que ejecuta
