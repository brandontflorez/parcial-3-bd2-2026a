CREATE DATABASE inmobiliaria;
USE inmobiliaria;

CREATE TABLE tipo_inmueble(
id_tipo INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE propietario(
id_propietario INT AUTO_INCREMENT PRIMARY KEY,
nombres VARCHAR(100) NOT NULL,
apellidos VARCHAR(100) NOT NULL,
documento VARCHAR(20) NOT NULL UNIQUE,
telefono VARCHAR(20),
correo VARCHAR(100)
);

CREATE TABLE inmueble(
id_inmueble INT AUTO_INCREMENT PRIMARY KEY,
id_tipo INT NOT NULL,
id_propietario INT NOT NULL,
direccion VARCHAR(200) NOT NULL,
area DECIMAL(10,2),
habitaciones INT,
canon_sugerido DECIMAL(12,2),
estado ENUM('Disponible','Arrendado') DEFAULT 'Disponible',
FOREIGN KEY (id_tipo) REFERENCES tipo_inmueble(id_tipo),
FOREIGN KEY (id_propietario) REFERENCES propietario(id_propietario)
);

CREATE TABLE arrendatario(
id_arrendatario INT AUTO_INCREMENT PRIMARY KEY,
nombres VARCHAR(100) NOT NULL,
apellidos VARCHAR(100) NOT NULL,
documento VARCHAR(20) UNIQUE,
telefono VARCHAR(20),
correo VARCHAR(100)
);

CREATE TABLE codeudor(
id_codeudor INT AUTO_INCREMENT PRIMARY KEY,
nombres VARCHAR(100),
apellidos VARCHAR(100),
documento VARCHAR(20) UNIQUE,
telefono VARCHAR(20)
);

CREATE TABLE contrato(
id_contrato INT AUTO_INCREMENT PRIMARY KEY,
id_inmueble INT NOT NULL,
id_arrendatario INT NOT NULL,
id_codeudor INT,
fecha_inicio DATE NOT NULL,
fecha_fin DATE NOT NULL,
canon_mensual DECIMAL(12,2) NOT NULL,
deposito DECIMAL(12,2),
dia_pago INT,
estado ENUM('Vigente','Finalizado') DEFAULT 'Vigente',
FOREIGN KEY (id_inmueble) REFERENCES inmueble(id_inmueble),
FOREIGN KEY (id_arrendatario) REFERENCES arrendatario(id_arrendatario),
FOREIGN KEY (id_codeudor) REFERENCES codeudor(id_codeudor)
);

CREATE TABLE cuota(
id_cuota INT AUTO_INCREMENT PRIMARY KEY,
id_contrato INT NOT NULL,
fecha_vencimiento DATE NOT NULL,
valor DECIMAL(12,2) NOT NULL,
interes_mora DECIMAL(12,2) DEFAULT 0,
estado ENUM('Pendiente','Pagada','Vencida') DEFAULT 'Pendiente',
FOREIGN KEY (id_contrato) REFERENCES contrato(id_contrato)
);

CREATE TABLE pago(
id_pago INT AUTO_INCREMENT PRIMARY KEY,
id_cuota INT NOT NULL,
fecha_pago DATE NOT NULL,
valor_pagado DECIMAL(12,2) NOT NULL,
FOREIGN KEY (id_cuota) REFERENCES cuota(id_cuota)
);
