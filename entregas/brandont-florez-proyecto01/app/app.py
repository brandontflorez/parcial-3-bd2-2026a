from flask import Flask, render_template, request, redirect
import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)


def conexion():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        conn = conexion()

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT *
                FROM usuario
                WHERE usuario=%s
                AND password=%s
            """, (usuario, password))

            user = cursor.fetchone()
            
            print(user)

        conn.close()

        if user:
            return redirect('/dashboard')

        return render_template(
            "login.html",
            error="Usuario o contraseña incorrectos"
)

    return render_template('login.html')

@app.route('/')
def home():
    return redirect('/login')


@app.route('/dashboard')
def inicio():

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("SELECT COUNT(*) total FROM inmueble")
        total_inmuebles = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) total
            FROM inmueble
            WHERE estado='Disponible'
        """)
        disponibles = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) total
            FROM inmueble
            WHERE estado='Arrendado'
        """)
        arrendados = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) total
            FROM contrato
            WHERE estado='Vigente'
        """)
        contratos = cursor.fetchone()['total']

        cursor.execute("""
            SELECT IFNULL(SUM(valor + interes_mora),0) total
            FROM cuota
            WHERE estado <> 'Pagada'
        """)
        deuda_total = cursor.fetchone()['total']

        cursor.execute("""
            SELECT IFNULL(SUM(valor_pagado),0) total
            FROM pago
        """)
        pagos_total = cursor.fetchone()['total']

    conn.close()

    return render_template(
        'index.html',
        total_inmuebles=total_inmuebles,
        disponibles=disponibles,
        arrendados=arrendados,
        contratos=contratos,
        deuda_total=deuda_total,
        pagos_total=pagos_total
    )
    
@app.route('/cuotas')
def cuotas():

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT
                c.id_cuota,
                a.nombres,
                a.apellidos,
                c.valor,
                c.estado,
                c.fecha_vencimiento
            FROM cuota c
            INNER JOIN contrato co ON c.id_contrato = co.id_contrato
            INNER JOIN arrendatario a ON co.id_arrendatario = a.id_arrendatario
            ORDER BY c.fecha_vencimiento
        """)

        cuotas = cursor.fetchall()

    conn.close()

    return render_template('cuotas.html', cuotas=cuotas)
    
@app.route('/pagar_cuota/<int:id>', methods=['POST'])
def pagar_cuota(id):

    monto = float(request.form['monto'])

    conn = conexion()

    with conn.cursor() as cursor:

        # 1. traer cuota
        cursor.execute("""
            SELECT id_cuota, valor, estado
            FROM cuota
            WHERE id_cuota=%s
        """, (id,))

        cuota = cursor.fetchone()

        if not cuota:
            conn.close()
            return "Cuota no encontrada", 404

        # 2. registrar pago
        cursor.execute("""
            INSERT INTO pago (id_cuota, valor_pagado, fecha_pago)
            VALUES (%s, %s, NOW())
        """, (id, monto))

        # 3. calcular total pagado
        cursor.execute("""
            SELECT IFNULL(SUM(valor_pagado),0) AS pagado
            FROM pago
            WHERE id_cuota=%s
        """, (id,))

        pagado = float(cursor.fetchone()['pagado'])

        saldo = float(cuota['valor']) - pagado

        # 4. estado
        if saldo <= 0:
            estado = "Pagada"
            saldo = 0
        elif pagado > 0:
            estado = "Parcial"
        else:
            estado = "Pendiente"

        # 5. actualizar cuota
        cursor.execute("""
            UPDATE cuota
            SET estado=%s
            WHERE id_cuota=%s
        """, (estado, id))

        conn.commit()

    conn.close()

    return redirect('/cuotas')

@app.route('/recibo/<int:id>')
def recibo(id):

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT p.*, c.id_cuota
            FROM pago p
            INNER JOIN cuota c ON p.id_cuota = c.id_cuota
            WHERE p.id_pago=%s
        """, (id,))

        pago = cursor.fetchone()

    conn.close()

    return render_template('recibo.html', pago=pago)

@app.route('/arrendatarios')
def arrendatarios():

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT *
            FROM arrendatario
            ORDER BY id_arrendatario
        """)

        arrendatarios = cursor.fetchall()

    conn.close()

    return render_template(
        'arrendatarios.html',
        arrendatarios=arrendatarios
    )

@app.route('/contratos')
def contratos():

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT
                c.id_contrato,
                i.direccion,
                a.nombres,
                a.apellidos,
                c.fecha_inicio,
                c.fecha_fin,
                c.canon_mensual,
                c.estado
            FROM contrato c
            INNER JOIN inmueble i
                ON c.id_inmueble = i.id_inmueble
            INNER JOIN arrendatario a
                ON c.id_arrendatario = a.id_arrendatario
            ORDER BY c.id_contrato DESC
        """)

        contratos = cursor.fetchall()

    conn.close()

    return render_template(
        'contratos.html',
        contratos=contratos
    )

@app.route('/nuevo_contrato', methods=['GET','POST'])
def nuevo_contrato():

    conn = conexion()

    if request.method == 'POST':

        id_inmueble = request.form['id_inmueble']
        id_arrendatario = request.form['id_arrendatario']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        canon_mensual = request.form['canon_mensual']
        deposito = request.form['deposito']
        dia_pago = request.form['dia_pago']

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO contrato
                (
                    id_inmueble,
                    id_arrendatario,
                    fecha_inicio,
                    fecha_fin,
                    canon_mensual,
                    deposito,
                    dia_pago,
                    estado
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s,%s,'Vigente'
                )
            """, (
                id_inmueble,
                id_arrendatario,
                fecha_inicio,
                fecha_fin,
                canon_mensual,
                deposito,
                dia_pago
            ))

            cursor.execute("""
                UPDATE inmueble
                SET estado='Arrendado'
                WHERE id_inmueble=%s
            """, (id_inmueble,))

            conn.commit()

        conn.close()

        return redirect('/contratos')

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT id_inmueble,direccion
            FROM inmueble
            WHERE estado='Disponible'
        """)

        inmuebles = cursor.fetchall()

        cursor.execute("""
            SELECT
                id_arrendatario,
                nombres,
                apellidos
            FROM arrendatario
        """)

        arrendatarios = cursor.fetchall()

    conn.close()

    return render_template(
        'nuevo_contrato.html',
        inmuebles=inmuebles,
        arrendatarios=arrendatarios
    )

@app.route('/nuevo_arrendatario', methods=['GET','POST'])
def nuevo_arrendatario():

    if request.method == 'POST':

        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        documento = request.form['documento']
        telefono = request.form['telefono']
        correo = request.form['correo']

        conn = conexion()

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO arrendatario
                (
                    nombres,
                    apellidos,
                    documento,
                    telefono,
                    correo
                )
                VALUES
                (%s,%s,%s,%s,%s)
            """, (
                nombres,
                apellidos,
                documento,
                telefono,
                correo
            ))

            conn.commit()

        conn.close()

        return redirect('/arrendatarios')

    return render_template('nuevo_arrendatario.html')
    
@app.route('/nuevo_inmueble', methods=['GET', 'POST'])
def nuevo_inmueble():

    if request.method == 'POST':
        
        id_propietario = request.form['id_propietario']
        id_tipo = request.form['id_tipo']
        direccion = request.form['direccion']
        area = request.form['area']
        habitaciones = request.form['habitaciones']
        canon = request.form['canon']

        conn = conexion()

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO inmueble
                (id_propietario, id_tipo, direccion, area, habitaciones, canon_sugerido, estado)
                VALUES (%s,%s,%s,%s,%s,%s,'Disponible')
            """, (
                id_propietario,
                id_tipo,
                direccion,
                area,
                habitaciones,
                canon
            ))

            conn.commit()

        conn.close()

        return redirect('/inmuebles')

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("SELECT id_propietario, nombres FROM propietario")
        propietarios = cursor.fetchall()

        cursor.execute("SELECT id_tipo, nombre FROM tipo_inmueble")
        tipos = cursor.fetchall()

    conn.close()

    return render_template(
        'nuevo_inmueble.html',
        propietarios=propietarios,
        tipos=tipos
    )

@app.route('/propietarios')
def propietarios():

    conn = conexion()

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM propietario
            ORDER BY id_propietario 
        """)
        propietarios = cursor.fetchall()

    conn.close()

    return render_template(
        'propietarios.html',
        propietarios=propietarios
    )


@app.route('/nuevo_propietario', methods=['GET', 'POST'])
def nuevo_propietario():

    if request.method == 'POST':

        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        documento = request.form['documento']
        telefono = request.form['telefono']
        correo = request.form['correo']

        conn = conexion()

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO propietario
                (nombres, apellidos, documento, telefono, correo)
                VALUES (%s,%s,%s,%s,%s)
            """, (nombres, apellidos, documento, telefono, correo))

            conn.commit()

        conn.close()

        return redirect('/propietarios')

    return render_template('nuevo_propietario.html')


@app.route('/editar_propietario/<int:id>', methods=['GET', 'POST'])
def editar_propietario(id):

    conn = conexion()

    if request.method == 'POST':

        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        documento = request.form['documento']
        telefono = request.form['telefono']
        correo = request.form['correo']

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE propietario
                SET nombres=%s,
                    apellidos=%s,
                    documento=%s,
                    telefono=%s,
                    correo=%s
                WHERE id_propietario=%s
            """, (nombres, apellidos, documento, telefono, correo, id))

            conn.commit()

        conn.close()

        return redirect('/propietarios')

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM propietario
            WHERE id_propietario=%s
        """, (id,))
        propietario = cursor.fetchone()

    conn.close()

    return render_template('editar_propietario.html', propietario=propietario)


@app.route('/eliminar_propietario/<int:id>')
def eliminar_propietario(id):

    conn = conexion()

    with conn.cursor() as cursor:
        cursor.execute("""
            DELETE FROM propietario
            WHERE id_propietario=%s
        """, (id,))

        conn.commit()

    conn.close()

    return redirect('/propietarios')

import pymysql

@app.route('/inmuebles')
def inmuebles():

    conn = conexion()

    with conn.cursor(pymysql.cursors.DictCursor) as cursor:

        cursor.execute("""
            SELECT
                i.id_inmueble,
                t.nombre AS tipo,
                i.direccion,
                i.area,
                i.habitaciones,
                i.canon_sugerido,
                i.estado
            FROM inmueble i
            INNER JOIN tipo_inmueble t
                ON i.id_tipo = t.id_tipo
            ORDER BY i.id_inmueble
        """)

        inmuebles = cursor.fetchall()

    conn.close()

    return render_template(
        'inmuebles.html',
        inmuebles=inmuebles
    )


@app.route('/cartera')
def cartera():

    conn = conexion()

    with conn.cursor() as cursor:

        # 🔥 CARTERA REAL POR CUOTAS
        cursor.execute("""
            SELECT
                a.id_arrendatario,
                a.nombres,
                a.apellidos,

                COUNT(c.id_cuota) AS cuotas,

                SUM(c.valor) AS deuda_total,

                IFNULL(SUM(pagos.total_pagado), 0) AS pagado,

                (SUM(c.valor) - IFNULL(SUM(pagos.total_pagado), 0)) AS saldo,

                CASE
                    WHEN IFNULL(SUM(pagos.total_pagado), 0) >= SUM(c.valor) THEN 'Pagada'
                    WHEN IFNULL(SUM(pagos.total_pagado), 0) > 0 THEN 'Parcial'
                    ELSE 'Pendiente'
                END AS estado

            FROM cuota c
            INNER JOIN contrato co ON c.id_contrato = co.id_contrato
            INNER JOIN arrendatario a ON co.id_arrendatario = a.id_arrendatario

            LEFT JOIN (
                SELECT id_cuota, SUM(valor_pagado) AS total_pagado
                FROM pago
                GROUP BY id_cuota
            ) pagos ON pagos.id_cuota = c.id_cuota

            GROUP BY
                a.id_arrendatario,
                a.nombres,
                a.apellidos

            ORDER BY saldo DESC
        """)

        cartera = cursor.fetchall()

        # 🔥 KPIs globales
        cursor.execute("""
            SELECT IFNULL(SUM(valor),0) total
            FROM cuota
        """)
        deuda_total = cursor.fetchone()['total'] or 0

        cursor.execute("""
            SELECT IFNULL(SUM(valor_pagado),0) total
            FROM pago
        """)
        pagos_total = cursor.fetchone()['total'] or 0

        cursor.execute("""
            SELECT COUNT(*) total
            FROM cuota
            WHERE estado='Pendiente'
        """)
        cuotas_pendientes = cursor.fetchone()['total'] or 0

        cursor.execute("""
            SELECT COUNT(*) total
            FROM cuota
            WHERE estado='Vencida'
        """)
        cuotas_vencidas = cursor.fetchone()['total'] or 0

    conn.close()

    return render_template(
        'cartera.html',
        cartera=cartera,
        deuda_total=deuda_total,
        pagos_total=pagos_total,
        cuotas_pendientes=cuotas_pendientes,
        cuotas_vencidas=cuotas_vencidas
    )



@app.route('/logout')
def logout():
    return redirect('/login')

@app.route('/editar_inmueble/<int:id>', methods=['GET', 'POST'])
def editar_inmueble(id):

    conn = conexion()

    if request.method == 'POST':

        id_tipo = request.form['id_tipo']
        direccion = request.form['direccion']
        area = request.form['area']
        habitaciones = request.form['habitaciones']
        canon = request.form['canon']
        estado = request.form['estado']

        with conn.cursor() as cursor:

            cursor.execute("""
                UPDATE inmueble
                SET
                    id_tipo=%s,
                    direccion=%s,
                    area=%s,
                    habitaciones=%s,
                    canon_sugerido=%s,
                    estado=%s
                WHERE id_inmueble=%s
            """, (
                id_tipo,
                direccion,
                area,
                habitaciones,
                canon,
                estado,
                id
            ))

            conn.commit()

        conn.close()

        return redirect('/inmuebles')

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT *
            FROM inmueble
            WHERE id_inmueble=%s
        """, (id,))

        inmueble = cursor.fetchone()

    conn.close()

    return render_template(
        'editar_inmueble.html',
        inmueble=inmueble
    )

@app.route('/eliminar_inmueble/<int:id>')
def eliminar_inmueble(id):

    conn = conexion()

    with conn.cursor() as cursor:

        cursor.execute("""
            DELETE FROM inmueble
            WHERE id_inmueble=%s
        """, (id,))

        conn.commit()

    conn.close()

    return redirect('/inmuebles')


if __name__ == '__main__':
    app.run(debug=True)