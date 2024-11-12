import smtplib
from flask import Flask, flash, jsonify, request, render_template, redirect, url_for, session
import pymysql
import pandas as pd
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from flask import session
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash
from io import BytesIO
import base64

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='Pipe2468*',
                           db='nominabdd',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def generar_hash_sha256(cadena):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(cadena.encode('utf-8'))
    return sha256_hash.hexdigest()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT rol, contrasenaHash FROM usuarios WHERE nombreUsuario = %s", [usuario])
            usuarios = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if usuarios:
            contrasena_hash = generar_hash_sha256(contrasena)
            if usuarios['contrasenaHash'] == contrasena_hash:
                if usuarios['rol'] == 'Admin':
                    return redirect(url_for('admin_dashboard'))
                elif usuarios['rol'] == 'Empleado':
                    return redirect(url_for('empleado_dashboard'))
            else:
                mensaje = "Contraseña incorrecta."
        else:
            mensaje = "Usuario no registrado."

        return render_template('index.html', mensaje=mensaje)

    return render_template('index.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
   
    return render_template('index.html')



@app.route('/admin_dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM areatrabajo")
    areatrabajo = cursor.fetchall()

    cursor.execute("SELECT * FROM cargos")
    cargos = cursor.fetchall()

    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()

    cursor.execute("SELECT * FROM eps")
    eps = cursor.fetchall()

    cursor.execute("SELECT * FROM nomina")
    nomina = cursor.fetchall()

    cursor.execute("SELECT * FROM novedades")
    novedades = cursor.fetchall()

    cursor.execute("SELECT * FROM pension")
    pension = cursor.fetchall()

    cursor.execute("SELECT * FROM reportes")
    reportes = cursor.fetchall()

    cursor.execute("SELECT * FROM saludpension")
    saludpension = cursor.fetchall()

    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()

    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('Administrador.html',areatrabajo=areatrabajo, cargos=cargos, eps=eps, nomina=nomina, novedades=novedades, pension=pension, reportes=reportes, saludpension=saludpension, empleados=empleados, usuarios=usuarios)



@app.route('/agregar_AreaAdmin', methods=['POST'])
def agregar_AreaAdmin():
    if request.method == 'POST':
        
        idAreaTrabajo = request.form['idAreaTrabajo']
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO areatrabajo (idAreaTrabajo, nombre) VALUES ( %s, %s)", ( idAreaTrabajo, nombre))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/modificar_AreaAdmin/<int:id>', methods=['GET', 'POST'])
def modificar_AreaAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        id = request.form['idAreaTrabajo']
        nombre = request.form['nombre']
       
        cursor.execute("UPDATE areatrabajo SET  nombre = %s WHERE idAreaTrabajo = %s", ( nombre,id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))
    
@app.route('/eliminar_AreaAdmin/<int:id>')
def eliminar_AreaAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM areatrabajo WHERE idAreaTrabajo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))  






@app.route('/empleado_dashboard')
def empleado_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

   
    
    cursor.close()
    conn.close()
    
    return render_template('Empleado.html')




if __name__ == '_main_':
    app.run(debug=True)


@app.route('/agregar_CargoAdmin', methods=['POST'])
def agregar_CargoAdmin():
    if request.method == 'POST':
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cargos (nombre) VALUES (%s)", (nombre,))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/modificar_CargoAdmin/<int:id>', methods=['GET', 'POST'])
def modificar_CargoAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cursor.execute("UPDATE cargos SET nombre = %s WHERE idCargo = %s", (nombre, id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

@app.route('/eliminar_CargoAdmin/<int:id>')
def eliminar_CargoAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cargos WHERE idCargo = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/agregar_EmpleadoAdmin', methods=['GET', 'POST'])
def agregar_EmpleadoAdmin():
    conn = get_db_connection()
    cursor = conn.cursor()


    if request.method == 'GET':
        cursor.execute("SELECT * FROM Cargos")
        cargos = cursor.fetchall()
        cursor.execute("SELECT * FROM AreaTrabajo")
        area_trabajo = cursor.fetchall()

        cursor.close()

        
        return render_template('agregar_empleado.html', cargos=cargos, area_trabajo=area_trabajo)
        

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        idCargo = request.form['idCargo']  
        idAreaTrabajo = request.form['idAreaTrabajo']  
        salario = request.form['salario']
        idEPS = request.form['idEPS']
        idPension = request.form['idPension']
        fechaIngreso = request.form['fechaIngreso']
        fechaNacimiento = request.form['fechaNacimiento']
        email = request.form['email']
        telefono = request.form['telefono']

        
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO empleados (nombre, apellido, idCargo, idAreaTrabajo, salario, idEPS, idPension, fechaIngreso, fechaNacimiento, email, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido, idCargo, idAreaTrabajo, salario, idEPS, idPension, fechaIngreso, fechaNacimiento, email, telefono))


    
        conn.commit()

        cursor.close()
        conn.close()

        
        return redirect(url_for('admin_dashboard'))



@app.route('/modificar_EmpleadoAdmin/<int:id>', methods=['GET', 'POST'])
def modificar_EmpleadoAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo_id = request.form['cargo_id']
        area_trabajo_id = request.form['area_trabajo_id']
        salario = request.form['salario']

        cursor.execute("""
            UPDATE empleados 
            SET nombre = %s, cargo_id = %s, area_trabajo_id = %s, salario = %s 
            WHERE idEmpleado = %s
        """, (nombre, cargo_id, area_trabajo_id, salario, id))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

@app.route('/eliminar_EmpleadoAdmin/<int:id>')
def eliminar_EmpleadoAdmin(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE idEmpleado = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/agregar_EPS', methods=['POST'])
def agregar_EPS():
    if request.method == 'POST':
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO eps (nombre) VALUES (%s)", (nombre,))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/modificar_EPS/<int:id>', methods=['POST'])
def modificar_EPS(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE eps SET nombre = %s WHERE idEPS = %s", (nombre, id))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_EPS/<int:id>')
def eliminar_EPS(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eps WHERE idEPS = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))



@app.route('/agregar_Nomina', methods=['POST'])
def agregar_Nomina():
    if request.method == 'POST':
        idEmpleado = request.form['idEmpleado']
        mesAnio = request.form['mesAnio']
        salarioBase = request.form['salarioBase']
        bonificacion = request.form['bonificacion']
        apoyoTransporte = request.form['apoyoTransporte']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nomina (idEmpleado, mesAnio, salarioBase, bonificacion, apoyoTransporte)
            VALUES (%s, %s, %s, %s, %s)
        """, (idEmpleado, mesAnio, salarioBase, bonificacion, apoyoTransporte))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/modificar_Nomina/<int:id>', methods=['POST'])
def modificar_Nomina(id):
    if request.method == 'POST':
        mesAnio = request.form['mesAnio']
        salarioBase = request.form['salarioBase']
        bonificacion = request.form['bonificacion']
        apoyoTransporte = request.form['apoyoTransporte']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nomina
            SET mesAnio = %s, salarioBase = %s, bonificacion = %s, apoyoTransporte = %s
            WHERE idNomina = %s
        """, (mesAnio, salarioBase, bonificacion, apoyoTransporte, id))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_Nomina/<int:id>')
def eliminar_Nomina(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nomina WHERE idNomina = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/agregar_Novedad', methods=['POST'])
def agregar_Novedad():
    if request.method == 'POST':
        idEmpleado = request.form['idEmpleado']
        tipoNovedad = request.form['tipoNovedad']
        fechaInicio = request.form['fechaInicio']
        fechaFin = request.form.get('fechaFin', None)  
        detalle = request.form['detalle']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO novedades (idEmpleado, tipoNovedad, fechaInicio, fechaFin, detalle)
            VALUES (%s, %s, %s, %s, %s)
        """, (idEmpleado, tipoNovedad, fechaInicio, fechaFin, detalle))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/modificar_Novedad/<int:id>', methods=['POST'])
def modificar_Novedad(id):
    if request.method == 'POST':
        tipoNovedad = request.form['tipoNovedad']
        fechaInicio = request.form['fechaInicio']
        fechaFin = request.form.get('fechaFin', None)
        detalle = request.form['detalle']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE novedades
            SET tipoNovedad = %s, fechaInicio = %s, fechaFin = %s, detalle = %s
            WHERE idNovedad = %s
        """, (tipoNovedad, fechaInicio, fechaFin, detalle, id))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_Novedad/<int:id>')
def eliminar_Novedad(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM novedades WHERE idNovedad = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))



@app.route('/agregar_Pension', methods=['POST'])
def agregar_Pension():
    if request.method == 'POST':
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pension (nombre) VALUES (%s)", (nombre,))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/modificar_Pension/<int:id>', methods=['POST'])
def modificar_Pension(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE pension SET nombre = %s WHERE idPension = %s", (nombre, id))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_Pension/<int:id>')
def eliminar_Pension(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pension WHERE idPension = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/agregar_Reporte', methods=['POST'])
def agregar_Reporte():
    if request.method == 'POST':
        tipoReporte = request.form['tipoReporte']
        contenido = request.form['contenido'].encode('utf-8') 
        idUsuario = request.form['idUsuario']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reportes (tipoReporte, contenido, idUsuario) VALUES (%s, %s, %s)", 
                       (tipoReporte, contenido, idUsuario))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_Reporte/<int:id>')
def eliminar_Reporte(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reportes WHERE idReporte = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/agregar_SaludPension', methods=['POST'])
def agregar_SaludPension():
    if request.method == 'POST':
        idEmpleado = request.form['idEmpleado']
        idEPS = request.form['idEPS']
        idPension = request.form['idPension']
        fechaRegistro = request.form['fechaRegistro']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO saludpension (idEmpleado, idEPS, idPension, fechaRegistro) VALUES (%s, %s, %s, %s)", 
                       (idEmpleado, idEPS, idPension, fechaRegistro))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/eliminar_SaludPension/<int:id>')
def eliminar_SaludPension(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saludpension WHERE idSaludPension = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/agregar_Usuario', methods=['POST'])
def agregar_Usuario():
    if request.method == 'POST':
        # Recoge datos del formulario
        nombreUsuario = request.form['nombreUsuario']
        email = request.form['email']
        rol = request.form['rol']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']

        # Crear un hash seguro de la contraseña
        contrasenaHash = generar_hash_sha256(contrasena)

        try:
            # Inserta los datos en la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Usuarios (nombreUsuario, contrasenaHash, rol, email, telefono, fechaCreacion) VALUES (%s, %s, %s, %s, %s, NOW())",
                (nombreUsuario, contrasenaHash, rol, email, telefono)
            )
            conn.commit()

        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return "Error al agregar usuario", 500

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('admin_dashboard'))
    

@app.route('/modificar_Usuario/<int:id>', methods=['GET', 'POST'])
def modificar_Usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombreUsuario = request.form['nombreUsuario']
        email = request.form['email']
        rol = request.form['rol']
        contrasena = request.form['contrasena']
        
        if contrasena:  
            contrasenaHash = generate_password_hash(contrasena)
            cursor.execute("UPDATE usuarios SET nombreUsuario = %s, email = %s, rol = %s, contrasenaHash = %s WHERE idUsuario = %s", 
                           (nombreUsuario, email, rol, contrasenaHash, id))
        else:  
            cursor.execute("UPDATE usuarios SET nombreUsuario = %s, email = %s, rol = %s WHERE idUsuario = %s", 
                           (nombreUsuario, email, rol, id))
        
        conn.commit()


    cursor.execute("SELECT * FROM usuarios WHERE idUsuario = %s", (id,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('ModificarUsuario.html', usuario=usuario)

@app.route('/eliminar_Usuario/<int:id>')
def eliminar_Usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE idUsuario = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@app.route('/graficos', methods=['GET'])
def graficos():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos para el gráfico de EPS
    cursor.execute("""
        SELECT eps.nombre, COUNT(empleados.idEmpleado) AS cantidad
        FROM empleados
        JOIN eps ON empleados.idEPS = eps.idEPS
        GROUP BY eps.idEPS
    """)
    eps_data = cursor.fetchall()

    # Obtener datos para el gráfico de Pensión
    cursor.execute("""
        SELECT pension.nombre, COUNT(empleados.idEmpleado) AS cantidad
        FROM empleados
        JOIN pension ON empleados.idPension = pension.idPension
        GROUP BY pension.idPension
    """)
    pension_data = cursor.fetchall()

    # Obtener datos para el gráfico comparativo de EPS por Área de Trabajo
    cursor.execute("""
        SELECT at.nombre AS area, eps.nombre AS eps, COUNT(empleados.idEmpleado) AS cantidad
        FROM empleados
        JOIN eps ON empleados.idEPS = eps.idEPS
        JOIN areatrabajo AS at ON empleados.idAreaTrabajo = at.idAreaTrabajo
        GROUP BY at.idAreaTrabajo, eps.idEPS
        ORDER BY at.nombre, eps.nombre
    """)
    eps_area_data = cursor.fetchall()

    # Obtener datos para el gráfico comparativo de Pensión por Área de Trabajo
    cursor.execute("""
        SELECT at.nombre AS area, pension.nombre AS pension, COUNT(empleados.idEmpleado) AS cantidad
        FROM empleados
        JOIN pension ON empleados.idPension = pension.idPension
        JOIN areatrabajo AS at ON empleados.idAreaTrabajo = at.idAreaTrabajo
        GROUP BY at.idAreaTrabajo, pension.idPension
        ORDER BY at.nombre, pension.nombre
    """)
    pension_area_data = cursor.fetchall()

    cursor.close()
    conn.close()

    # Generación del gráfico de EPS
    eps_names = [row['nombre'] for row in eps_data]
    eps_counts = [row['cantidad'] for row in eps_data]

    plt.figure(figsize=(8, 6))
    plt.bar(eps_names, eps_counts, color='skyblue')
    plt.xlabel('EPS')
    plt.ylabel('Cantidad de Empleados')
    plt.title('Frecuencia de Empleados por EPS')
    plt.xticks(rotation=45, ha="right")

    # Guardar gráfico de EPS en base64
    img_eps = BytesIO()
    plt.tight_layout()
    plt.savefig(img_eps, format='png')
    img_eps.seek(0)
    img_eps_base64 = base64.b64encode(img_eps.getvalue()).decode('utf8')
    plt.close()

    # Generación del gráfico de Pensión
    pension_names = [row['nombre'] for row in pension_data]
    pension_counts = [row['cantidad'] for row in pension_data]

    plt.figure(figsize=(8, 6))
    plt.bar(pension_names, pension_counts, color='salmon')
    plt.xlabel('Pensión')
    plt.ylabel('Cantidad de Empleados')
    plt.title('Frecuencia de Empleados por Pensión')
    plt.xticks(rotation=45, ha="right")

    # Guardar gráfico de Pensión en base64
    img_pension = BytesIO()
    plt.tight_layout()
    plt.savefig(img_pension, format='png')
    img_pension.seek(0)
    img_pension_base64 = base64.b64encode(img_pension.getvalue()).decode('utf8')
    plt.close()

    # Generación de gráfico comparativo para EPS por Área de Trabajo
    areas = sorted(set(row['area'] for row in eps_area_data))
    eps_names = sorted(set(row['eps'] for row in eps_area_data))

    eps_counts_per_area = {area: {eps: 0 for eps in eps_names} for area in areas}
    for row in eps_area_data:
        eps_counts_per_area[row['area']][row['eps']] = row['cantidad']

    plt.figure(figsize=(10, 6))
    for eps in eps_names:
        counts = [eps_counts_per_area[area][eps] for area in areas]
        plt.bar(areas, counts, label=eps)

    plt.xlabel('Área de Trabajo')
    plt.ylabel('Cantidad de Empleados')
    plt.title('Comparativa de Empleados por EPS y Área de Trabajo')
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="EPS")

    # Guardar gráfico comparativo de EPS en base64
    img_eps_area = BytesIO()
    plt.tight_layout()
    plt.savefig(img_eps_area, format='png')
    img_eps_area.seek(0)
    img_eps_area_base64 = base64.b64encode(img_eps_area.getvalue()).decode('utf8')
    plt.close()

    # Generación de gráfico comparativo para Pensión por Área de Trabajo
    pension_names = sorted(set(row['pension'] for row in pension_area_data))

    pension_counts_per_area = {area: {pension: 0 for pension in pension_names} for area in areas}
    for row in pension_area_data:
        pension_counts_per_area[row['area']][row['pension']] = row['cantidad']

    plt.figure(figsize=(10, 6))
    for pension in pension_names:
        counts = [pension_counts_per_area[area][pension] for area in areas]
        plt.bar(areas, counts, label=pension)

    plt.xlabel('Área de Trabajo')
    plt.ylabel('Cantidad de Empleados')
    plt.title('Comparativa de Empleados por Pensión y Área de Trabajo')
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Pensión")

    # Guardar gráfico comparativo de Pensión en base64
    img_pension_area = BytesIO()
    plt.tight_layout()
    plt.savefig(img_pension_area, format='png')
    img_pension_area.seek(0)
    img_pension_area_base64 = base64.b64encode(img_pension_area.getvalue()).decode('utf8')
    plt.close()

    # Pasar todos los gráficos a la plantilla
    return render_template('graficos.html', 
                           img_eps=img_eps_base64, 
                           img_pension=img_pension_base64,
                           img_eps_area=img_eps_area_base64, 
                           img_pension_area=img_pension_area_base64)


    

from datetime import datetime
@app.route('/empleados', methods=['GET'])
def empleados():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recoger parámetros de la URL para ordenar los empleados
    ordenar_por = request.args.get('ordenar_por', 'nombre')  # Por defecto ordenamos por nombre
    direccion = request.args.get('direccion', 'asc')  # Ascendente por defecto

    # Consulta para obtener empleados con el orden dinámico
    query = f"""
        SELECT empleados.idEmpleado, empleados.nombre, empleados.apellido, cargos.nombre AS cargo, 
               areatrabajo.nombre AS area_trabajo, empleados.salario, eps.nombre AS eps, pension.nombre AS pension
        FROM empleados
        JOIN cargos ON empleados.idCargo = cargos.idCargo
        JOIN areatrabajo ON empleados.idAreaTrabajo = areatrabajo.idAreaTrabajo
        JOIN eps ON empleados.idEPS = eps.idEPS
        JOIN pension ON empleados.idPension = pension.idPension
        ORDER BY {ordenar_por} {direccion}
    """

    cursor.execute(query)
    empleados = cursor.fetchall()

    # Cargar datos para el formulario de agregar un empleado
    cursor.execute("SELECT * FROM Cargos")
    cargos = cursor.fetchall()

    cursor.execute("SELECT * FROM AreaTrabajo")
    area_trabajo = cursor.fetchall()

    cursor.close()
    conn.close()

    

    # Pasar datos a la plantilla
    return render_template('empleados.html', 
                           empleados=empleados, 
                           cargos=cargos, 
                           area_trabajo=area_trabajo,
                           ordenar_por=ordenar_por,
                           direccion=direccion)

    
@app.route('/novedades_empleados', methods=['GET'])
def novedades_empleados():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recuperar fechas de inicio y fin de los parámetros de la URL
    fecha_inicio = request.args.get('fecha_inicio', '')  # Fecha de inicio (MM/AAAA)
    fecha_fin = request.args.get('fecha_fin', '')  # Fecha de fin (MM/AAAA)
    
    empleados_con_novedades = []

    if fecha_inicio and fecha_fin:
        try:
            # Convertir las fechas de MM/AAAA a formato YYYY-MM-01
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%m/%Y').date()
            fecha_fin_obj = datetime.strptime(fecha_fin, '%m/%Y').date()

            # Consultar empleados con novedades (fechaIngreso dentro del rango)
            query = """
                SELECT empleados.idEmpleado, empleados.nombre, empleados.apellido, cargos.nombre AS cargo, 
                       areatrabajo.nombre AS area_trabajo, empleados.salario, eps.nombre AS eps, pension.nombre AS pension
                FROM empleados
                JOIN cargos ON empleados.idCargo = cargos.idCargo
                JOIN areatrabajo ON empleados.idAreaTrabajo = areatrabajo.idAreaTrabajo
                JOIN eps ON empleados.idEPS = eps.idEPS
                JOIN pension ON empleados.idPension = pension.idPension
                WHERE empleados.fechaIngreso BETWEEN %s AND %s
            """
            cursor.execute(query, (fecha_inicio_obj, fecha_fin_obj))
            empleados_con_novedades = cursor.fetchall()

        except ValueError:

          
            flash('Formato de fecha incorrecto. Por favor use MM/AAAA.', 'error')

    cursor.close()
    conn.close()

    return render_template('empleados.html', empleados=empleados_con_novedades, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@app.route('/detalle_novedades_empleados', methods=['GET'])
def detalle_novedades_empleados():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recuperar fechas de inicio y fin de los parámetros de la URL
    fecha_inicio = request.args.get('fecha_inicio', '')  # Fecha de inicio (MM/AAAA)
    fecha_fin = request.args.get('fecha_fin', '')  # Fecha de fin (MM/AAAA)
    area_trabajo = request.args.get('area_trabajo', '')  # Área de trabajo filtrada
    cargo = request.args.get('cargo', '')  # Cargo filtrado

    empleados_detalle = []

    if fecha_inicio and fecha_fin:
        try:
            # Convertir las fechas de MM/AAAA a formato YYYY-MM-01
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%m/%Y').date()
            fecha_fin_obj = datetime.strptime(fecha_fin, '%m/%Y').date()

            # Consultar empleados con novedades (fechaIngreso dentro del rango), con filtros de área y cargo
            query = """
                SELECT e.idEmpleado, e.nombre, e.apellido, c.nombre AS cargo, 
                       at.nombre AS area_trabajo, e.salario, e.fechaIngreso, 
                       eps.nombre AS eps, p.nombre AS pension
                FROM empleados e
                JOIN cargos c ON e.idCargo = c.idCargo
                JOIN areatrabajo at ON e.idAreaTrabajo = at.idAreaTrabajo
                JOIN eps ON e.idEPS = eps.idEPS
                JOIN pension p ON e.idPension = p.idPension
                WHERE e.fechaIngreso BETWEEN %s AND %s
            """

          
            if area_trabajo:
                query += " AND at.idAreaTrabajo = %s"
       
            if cargo:
                query += " AND c.idCargo = %s"

   
            if area_trabajo and cargo:
                cursor.execute(query, (fecha_inicio_obj, fecha_fin_obj, area_trabajo, cargo))
            elif area_trabajo:
                cursor.execute(query, (fecha_inicio_obj, fecha_fin_obj, area_trabajo))
            elif cargo:
                cursor.execute(query, (fecha_inicio_obj, fecha_fin_obj, cargo))
            else:
                cursor.execute(query, (fecha_inicio_obj, fecha_fin_obj))

            empleados_detalle = cursor.fetchall()

        except ValueError:
            flash('Formato de fecha incorrecto. Por favor use MM/AAAA.', 'error')

    cursor.close()
    conn.close()

    return render_template('empleados.html', 
                           empleados=empleados_detalle, 
                           fecha_inicio=fecha_inicio, 
                           fecha_fin=fecha_fin,
                           area_trabajo=area_trabajo, 
                           cargo=cargo)


@app.route('/cantidad_incapacidades', methods=['GET'])
def cantidad_incapacidades():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Recuperar fechas de inicio y fin de los parámetros de la URL
    fecha_inicio = request.args.get('fecha_inicio', '')  # Cambié el nombre de 'fechaInicio' a 'fecha_inicio'
    fecha_fin = request.args.get('fecha_fin', '')  # Cambié el nombre de 'fechaFin' a 'fecha_fin'

    cantidad_incapacidades = 0  # Variable para almacenar la cantidad de incapacidades

    if fecha_inicio and fecha_fin:
        try:
            # Convertir las fechas de MM/AAAA a formato YYYY-MM-01
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%m/%Y').replace(day=1)
            fecha_fin_obj = datetime.strptime(fecha_fin, '%m/%Y').replace(day=1)

            # Consultar el conteo de incapacidades dentro del rango de fechas
            query_incapacidades = """
                SELECT COUNT(*) 
                FROM novedades n
                WHERE n.tipoNovedad = 'Incapacidad'
                  AND (
                    (n.fechaInicio BETWEEN %s AND %s) OR
                    (n.fechaFin BETWEEN %s AND %s) OR
                    (n.fechaInicio <= %s AND n.fechaFin >= %s)
                  )
            """
            cursor.execute(query_incapacidades, 
                           (fecha_inicio_obj, fecha_fin_obj, 
                            fecha_inicio_obj, fecha_fin_obj, 
                            fecha_inicio_obj, fecha_fin_obj))

            # Recuperar el resultado de la consulta
            result = cursor.fetchone()

            # Verificar si se obtuvo un resultado válido
            if result and isinstance(result, tuple):
                cantidad_incapacidades = result[0]  # Obtener el primer valor de la primera columna (el conteo)
            else:
                cantidad_incapacidades = 0  # Si no hay resultados, asignar 0

        except ValueError:
            flash('Formato de fecha incorrecto. Por favor use MM/AAAA.', 'error')
        except Exception as e:
            flash(f'Ocurrió un error al procesar la solicitud: {e}', 'error')

    cursor.close()
    conn.close()

    return render_template('empleados.html', 
                           cantidad_incapacidades=cantidad_incapacidades,
                           fecha_inicio=fecha_inicio, 
                           fecha_fin=fecha_fin)




@app.route('/debug_incapacidades', methods=['GET'])
def debug_incapacidades():
    conn = get_db_connection()
    cursor = conn.cursor()

    query_incapacidades = """
        SELECT n.idNovedad, e.nombre, e.apellido, n.fechaInicio, n.fechaFin
        FROM novedades n
        JOIN empleados e ON n.idEmpleado = e.idEmpleado
        WHERE n.tipoNovedad = 'Incapacidad'
        ORDER BY n.fechaInicio DESC
    """
    cursor.execute(query_incapacidades)

    incapacidades = cursor.fetchall()

    cursor.close()
    conn.close()

    # Si no hay datos, retorna un mensaje vacío
    if not incapacidades:
        return jsonify({'message': 'No se encontraron incapacidades registradas.'})

    # Si hay datos, los devuelve en formato JSON
    result = [{
        'idNovedad': incapacidad['idNovedad'],  # Acceder con clave, no con índice
        'nombre': incapacidad['nombre'],
        'apellido': incapacidad['apellido'],
        'fechaInicio': incapacidad['fechaInicio'].strftime('%Y-%m-%d') if incapacidad['fechaInicio'] else None,
        'fechaFin': incapacidad['fechaFin'].strftime('%Y-%m-%d') if incapacidad['fechaFin'] else None
    } for incapacidad in incapacidades]

    return jsonify(result)



@app.route('/reporte_nomina', methods=['GET', 'POST'])
def reporte_nomina():
    # Definir valores por defecto
    order_by = 'e.nombre'  # Valor predeterminado para ordenar por nombre de Empleados
    direction = 'ASC'      # Orden ascendente por defecto

    # Verificar si el usuario ha enviado un formulario con los filtros
    if request.method == 'POST':
        order_by = request.form.get('order_by')
        direction = request.form.get('direction')

    # Validar las opciones para evitar inyección SQL
    valid_columns = ['e.nombre', 'at.nombre', 'c.nombre', 'e.idAreaTrabajo', 'e.idCargo', 'e.salario']
    valid_directions = ['ASC', 'DESC']

    if order_by not in valid_columns:
        order_by = 'e.nombre'  # Por defecto, ordenar por 'nombre'
    if direction not in valid_directions:
        direction = 'ASC'  # Por defecto, ascendente

    # Realizar la consulta a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta de los empleados
    query = f"""
    SELECT e.idEmpleado, e.nombre, e.apellido, e.salario, at.nombre AS areaTrabajo, c.nombre AS cargo
    FROM Empleados e
    JOIN AreaTrabajo at ON e.idAreaTrabajo = at.idAreaTrabajo
    JOIN Cargos c ON e.idCargo = c.idCargo
    ORDER BY {order_by} {direction};
    """
    cursor.execute(query)
    empleados = cursor.fetchall()

    # Consultas para los gráficos de torta
    query_cargos = """
    SELECT c.nombre AS cargo, COUNT(e.idEmpleado) AS cantidad
    FROM Empleados e
    JOIN Cargos c ON e.idCargo = c.idCargo
    GROUP BY c.nombre;
    """
    cursor.execute(query_cargos)
    cargos_data = cursor.fetchall()

    query_areas = """
    SELECT at.nombre AS areaTrabajo, COUNT(e.idEmpleado) AS cantidad
    FROM Empleados e
    JOIN AreaTrabajo at ON e.idAreaTrabajo = at.idAreaTrabajo
    GROUP BY at.nombre;
    """
    cursor.execute(query_areas)
    areas_data = cursor.fetchall()

    # Consulta para el gráfico de barras de salarios promedio por área de trabajo
    query_salarios_area = """
    SELECT at.nombre AS areaTrabajo, AVG(e.salario) AS salario_promedio
    FROM Empleados e
    JOIN AreaTrabajo at ON e.idAreaTrabajo = at.idAreaTrabajo
    GROUP BY at.nombre;
    """
    cursor.execute(query_salarios_area)
    salarios_area_data = cursor.fetchall()

    cursor.close()
    connection.close()

    # Crear gráficos de torta y barras usando Matplotlib

    # Gráfico de torta para cargos
    cargos_df = pd.DataFrame(cargos_data, columns=['cargo', 'cantidad'])
    fig_cargos, ax_cargos = plt.subplots()
    ax_cargos.pie(cargos_df['cantidad'], labels=cargos_df['cargo'], autopct='%1.1f%%', startangle=90)
    ax_cargos.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Gráfico de torta para áreas de trabajo
    areas_df = pd.DataFrame(areas_data, columns=['areaTrabajo', 'cantidad'])
    fig_areas, ax_areas = plt.subplots()
    ax_areas.pie(areas_df['cantidad'], labels=areas_df['areaTrabajo'], autopct='%1.1f%%', startangle=90)
    ax_areas.axis('equal')

    # Gráfico de barras para salarios por área de trabajo
    salarios_area_df = pd.DataFrame(salarios_area_data, columns=['areaTrabajo', 'salario_promedio'])
    fig_salarios_area, ax_salarios_area = plt.subplots()
    ax_salarios_area.bar(salarios_area_df['areaTrabajo'], salarios_area_df['salario_promedio'])
    ax_salarios_area.set_title('Salario Promedio por Área de Trabajo')
    ax_salarios_area.set_xlabel('Área de Trabajo')
    ax_salarios_area.set_ylabel('Salario Promedio')

    # Convertir los gráficos a imágenes en formato PNG
    img_cargos = BytesIO()
    fig_cargos.savefig(img_cargos, format='png')
    img_cargos.seek(0)
    img_areas = BytesIO()
    fig_areas.savefig(img_areas, format='png')
    img_areas.seek(0)
    img_salarios_area = BytesIO()
    fig_salarios_area.savefig(img_salarios_area, format='png')
    img_salarios_area.seek(0)

    # Convertir imágenes a Base64 para incrustarlas en el HTML
    img_cargos_base64 = base64.b64encode(img_cargos.getvalue()).decode('utf-8')
    img_areas_base64 = base64.b64encode(img_areas.getvalue()).decode('utf-8')
    img_salarios_area_base64 = base64.b64encode(img_salarios_area.getvalue()).decode('utf-8')

    # Enviar los gráficos como imágenes en formato Base64 dentro del HTML
    return render_template('reporte_nomina.html', 
                           empleados=empleados, 
                           order_by=order_by, 
                           direction=direction,
                           img_cargos=img_cargos_base64, 
                           img_areas=img_areas_base64,
                           img_salarios_area=img_salarios_area_base64)