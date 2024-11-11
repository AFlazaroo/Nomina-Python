import smtplib
from flask import Flask, request, render_template, redirect, url_for
import pymysql
from flask import session
from email.mime.text import MIMEText

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='NominaEmpleados',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

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
            if usuarios['contrasenaHash'] == contrasena:
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




if __name__ == '__main__':
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
        nombreUsuario = request.form['nombreUsuario']
        email = request.form['email']
        rol = request.form['rol']
        contrasena = request.form['contrasena']
        contrasenaHash = generate_password_hash(contrasena)  

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombreUsuario, email, rol, contrasenaHash) VALUES (%s, %s, %s, %s)", 
                       (nombreUsuario, email, rol, contrasenaHash))
        conn.commit()

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
