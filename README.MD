# Business Intelligence - Universidad de Palermo

En este repo se armará el proyecto para resolver el problema propuesto
A partir de 3 archivos de clientes / Tipos de clientes / Ventas (en formato .csv),
se desarrollarán actividades de exploración de datos que lleven a responder preguntas útiles a la organización.

Los archivos serán ingestados a una Base de Datos MySQL, se crearán nuevas tablas para facilitar el análisis (modelado)
la cual será luego conectada con la herramienta de BI. 

## Uso
Para encender el proyecto:

    docker compose up -build

### Base de Datos

Desde un cliente se conecta a la base de datos con:

    mysql -u root -h 127.0.0.1 -p

    mysql> create database biup;
    Query OK, 1 row affected (0,02 sec)

Utilizaremos la base de datos biup para nuestra práctica

Luego crearemos las tablas para los 3 archivos desde el contenedor load:

    docker compose exec load bash

Y dentro de contenedor:

    app@504499bbaa61:/load/app$ python createtables.py 

### Carga de Datos

Luego necesitamos colocar los archivos en el directorio 

    load/files/

Los archivos deberán tener los nombres:
- business_types.csv
- cuustomers.csv
- orders.csv

Para ingestar los datos en MySQL, desde el contenedor load:

    docker compose exec load bash

Y dentro de contenedor:

    app@504499bbaa61:/load/app$ python loadfiles.py 

