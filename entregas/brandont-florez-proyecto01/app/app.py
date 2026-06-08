from flask import Flask, render_template
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


@app.route('/')
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


@app.route('/inmuebles')
def inmuebles():

    conn = conexion()

    with conn.cursor() as cursor:

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

        cursor.execute("""
            SELECT
                a.nombres,
                a.apellidos,
                COUNT(c.id_cuota) AS cuotas,
                SUM(c.valor + c.interes_mora) AS deuda
            FROM cuota c
            INNER JOIN contrato co
                ON c.id_contrato = co.id_contrato
            INNER JOIN arrendatario a
                ON co.id_arrendatario = a.id_arrendatario
            WHERE c.estado <> 'Pagada'
            GROUP BY
                a.id_arrendatario,
                a.nombres,
                a.apellidos
            ORDER BY deuda DESC
        """)

        cartera = cursor.fetchall()

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

        cursor.execute("""
            SELECT COUNT(*) total
            FROM cuota
            WHERE estado='Pendiente'
        """)
        cuotas_pendientes = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) total
            FROM cuota
            WHERE estado='Vencida'
        """)
        cuotas_vencidas = cursor.fetchone()['total']

    conn.close()

    return render_template(
        'cartera.html',
        cartera=cartera,
        deuda_total=deuda_total,
        pagos_total=pagos_total,
        cuotas_pendientes=cuotas_pendientes,
        cuotas_vencidas=cuotas_vencidas
    )


if __name__ == '__main__':
    app.run(debug=True)