# Proyecto 01 - Inmobiliaria de Arrendamientos

## Autor

Brandont Florez

## Descripción

Aplicación web desarrollada con Flask y MySQL para la gestión de una inmobiliaria de arrendamientos.

Permite administrar:

* Propietarios
* Inmuebles
* Arrendatarios
* Codeudores
* Contratos
* Cuotas
* Pagos

Además, permite consultar cartera pendiente y el estado de los inmuebles.

## Tecnologías utilizadas

* Python 3
* Flask
* MySQL
* HTML
* Bootstrap

## Creación de la Base de Datos

Ejecutar:

```sql
source ddl/01-crear-bd.sql;
```

## Carga de datos de prueba

Ejecutar:

```sql
source ddl/02-datos-prueba.sql;
```

## Instalación

Instalar dependencias:

```bash
pip install flask pymysql
```

## Ejecución

Desde la carpeta app:

```bash
python app.py
```

## Usuario de prueba

Administrador

```text
Usuario: admin
Contraseña: admin123
```

## Funcionalidades

* Gestión de inmuebles
* Gestión de propietarios
* Gestión de arrendatarios
* Gestión de contratos
* Gestión de cuotas
* Registro de pagos
* Reportes de cartera
* Consulta de inmuebles disponibles
