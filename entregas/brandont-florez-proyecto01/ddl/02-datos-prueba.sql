INSERT INTO tipo_inmueble(nombre)
VALUES
('Casa'),
('Apartamento'),
('Local Comercial'),
('Oficina');

INSERT INTO propietario(nombres,apellidos,documento,telefono,correo)
VALUES
('Carlos','Perez','1001','3001111111','[carlos@mail.com](mailto:carlos@mail.com)'),
('Ana','Gomez','1002','3001111112','[ana@mail.com](mailto:ana@mail.com)'),
('Luis','Martinez','1003','3001111113','[luis@mail.com](mailto:luis@mail.com)'),
('Martha','Rojas','1004','3001111114','[martha@mail.com](mailto:martha@mail.com)'),
('Jorge','Diaz','1005','3001111115','[jorge@mail.com](mailto:jorge@mail.com)'),
('Sandra','Lopez','1006','3001111116','[sandra@mail.com](mailto:sandra@mail.com)'),
('Pedro','Garcia','1007','3001111117','[pedro@mail.com](mailto:pedro@mail.com)'),
('Laura','Torres','1008','3001111118','[laura@mail.com](mailto:laura@mail.com)');

INSERT INTO arrendatario(nombres,apellidos,documento,telefono,correo)
VALUES
('Juan','Ramirez','2001','3100000001','[juan@mail.com](mailto:juan@mail.com)'),
('Maria','Suarez','2002','3100000002','[maria@mail.com](mailto:maria@mail.com)'),
('Felipe','Vargas','2003','3100000003','[felipe@mail.com](mailto:felipe@mail.com)'),
('Camila','Ruiz','2004','3100000004','[camila@mail.com](mailto:camila@mail.com)'),
('Andres','Castro','2005','3100000005','[andres@mail.com](mailto:andres@mail.com)'),
('Diana','Moreno','2006','3100000006','[diana@mail.com](mailto:diana@mail.com)'),
('Sofia','Gil','2007','3100000007','[sofia@mail.com](mailto:sofia@mail.com)'),
('Miguel','Ortiz','2008','3100000008','[miguel@mail.com](mailto:miguel@mail.com)'),
('Paula','Velez','2009','3100000009','[paula@mail.com](mailto:paula@mail.com)'),
('Julian','Herrera','2010','3100000010','[julian@mail.com](mailto:julian@mail.com)'),
('Kevin','Mora','2011','3100000011','[kevin@mail.com](mailto:kevin@mail.com)'),
('Valentina','Reyes','2012','3100000012','[valentina@mail.com](mailto:valentina@mail.com)');

INSERT INTO codeudor(nombres,apellidos,documento,telefono)
VALUES
('Ricardo','Lopez','3001','3200000001'),
('Monica','Castro','3002','3200000002'),
('Fernando','Perez','3003','3200000003'),
('Claudia','Rojas','3004','3200000004'),
('Diego','Martinez','3005','3200000005');

INSERT INTO inmueble(id_tipo,id_propietario,direccion,area,habitaciones,canon_sugerido,estado)
VALUES
(1,1,'Calle 10 #12-30',120,4,1200000,'Disponible'),
(1,2,'Carrera 20 #15-40',100,3,1000000,'Arrendado'),
(2,3,'Calle 30 #22-15',80,2,900000,'Arrendado'),
(2,4,'Carrera 18 #10-05',75,2,850000,'Disponible'),
(1,5,'Calle 45 #50-20',150,5,1500000,'Arrendado'),
(3,6,'Centro Comercial Local 12',60,0,2000000,'Disponible'),
(4,7,'Edificio Empresarial Of. 302',90,0,2500000,'Arrendado'),
(2,8,'Barrio Centro Apto 201',70,2,800000,'Disponible'),
(1,1,'Calle 8 #14-11',110,3,1100000,'Disponible'),
(2,2,'Carrera 11 #9-18',65,2,750000,'Arrendado'),
(1,3,'Calle 50 #20-10',140,4,1600000,'Disponible'),
(3,4,'Local Plaza 5',55,0,1800000,'Disponible'),
(4,5,'Oficina Torre Norte 402',100,0,2800000,'Arrendado'),
(2,6,'Apto 305 Barrio Nuevo',68,2,780000,'Disponible'),
(1,7,'Casa Campestre Km 2',200,5,2200000,'Disponible');
