# Normalización del Proyecto Inmobiliaria de Arrendamientos

## Primera Forma Normal (1FN)

Todas las tablas poseen atributos atómicos y no existen grupos repetitivos.

## Segunda Forma Normal (2FN)

Todos los atributos dependen completamente de la clave primaria de cada entidad.

## Tercera Forma Normal (3FN)

No existen dependencias transitivas entre atributos no clave.

## Entidades Principales

* Tipo_Inmueble
* Propietario
* Inmueble
* Arrendatario
* Codeudor
* Contrato
* Cuota
* Pago

## Relaciones

* Un propietario puede tener muchos inmuebles.
* Un inmueble pertenece a un propietario.
* Un contrato pertenece a un inmueble.
* Un contrato pertenece a un arrendatario.
* Un contrato puede tener un codeudor.
* Un contrato genera muchas cuotas.
* Una cuota puede registrar varios pagos.
