#!/usr/bin/env python3
"""
Factoría Demo - Aplicación Flask
Sistema de Gestión de Escuela de Artes
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# Configuración
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "factoria_demo.db"

app = Flask(__name__)
app.secret_key = 'factoria-demo-secret-key-2024'


def get_db():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def format_currency(value):
    """Formatea un valor como moneda"""
    if value is None:
        return "0,00 €"
    return f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def format_date(value):
    """Formatea una fecha"""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except:
            return value
    return value.strftime("%d/%m/%Y")


# Registrar filtros Jinja2
app.jinja_env.filters['currency'] = format_currency
app.jinja_env.filters['fecha'] = format_date


# ============================================
# RUTAS PRINCIPALES
# ============================================

@app.route('/')
def index():
    """Dashboard principal"""
    conn = get_db()
    cursor = conn.cursor()

    # Estadísticas generales
    stats = {}

    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE activo = 1")
    stats['total_alumnos'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM profesores WHERE activo = 1")
    stats['total_profesores'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inscripciones WHERE estado = 'activa'")
    stats['inscripciones_activas'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ausencias WHERE fecha >= date('now', '-30 days')")
    stats['ausencias_mes'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM actividades WHERE activa = 1")
    stats['total_actividades'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM areas")
    stats['total_areas'] = cursor.fetchone()[0]

    # Ingresos mensuales estimados
    cursor.execute("""
        SELECT COALESCE(SUM(COALESCE(i.precio_especial, a.precio_mensual)), 0)
        FROM inscripciones i
        JOIN actividades a ON i.actividad_id = a.id
        WHERE i.estado = 'activa'
    """)
    stats['ingresos_mensuales'] = cursor.fetchone()[0] or 0

    # Distribución por área
    cursor.execute("""
        SELECT ar.nombre, ar.icono, COUNT(i.id) as num
        FROM areas ar
        LEFT JOIN actividades a ON a.area_id = ar.id
        LEFT JOIN inscripciones i ON i.actividad_id = a.id AND i.estado = 'activa'
        GROUP BY ar.id
        ORDER BY num DESC
    """)
    areas_stats = cursor.fetchall()

    # Distribución por sede
    cursor.execute("""
        SELECT s.nombre, COUNT(a.id) as num
        FROM sedes s
        LEFT JOIN alumnos a ON a.sede_preferida_id = s.id AND a.activo = 1
        GROUP BY s.id
    """)
    sedes_stats = cursor.fetchall()

    # Últimas inscripciones
    cursor.execute("""
        SELECT
            al.nombre || ' ' || al.apellidos as alumno,
            act.nombre as actividad,
            i.fecha_inscripcion
        FROM inscripciones i
        JOIN alumnos al ON i.alumno_id = al.id
        JOIN actividades act ON i.actividad_id = act.id
        ORDER BY i.fecha_inscripcion DESC
        LIMIT 5
    """)
    ultimas_inscripciones = cursor.fetchall()

    # Últimas ausencias
    cursor.execute("""
        SELECT
            al.nombre || ' ' || al.apellidos as alumno,
            aus.fecha,
            aus.motivo
        FROM ausencias aus
        JOIN alumnos al ON aus.alumno_id = al.id
        ORDER BY aus.fecha DESC
        LIMIT 5
    """)
    ultimas_ausencias = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html',
                         stats=stats,
                         areas_stats=areas_stats,
                         sedes_stats=sedes_stats,
                         ultimas_inscripciones=ultimas_inscripciones,
                         ultimas_ausencias=ultimas_ausencias)


# ============================================
# MÓDULO: ALUMNOS
# ============================================

@app.route('/alumnos')
def alumnos_list():
    """Lista de alumnos"""
    conn = get_db()
    cursor = conn.cursor()

    # Filtros
    search = request.args.get('search', '')
    sede_id = request.args.get('sede', '')
    estado = request.args.get('estado', 'activo')

    query = """
        SELECT
            a.id, a.nombre, a.apellidos, a.edad, a.email, a.telefono,
            s.nombre as sede,
            a.activo,
            (SELECT COUNT(*) FROM inscripciones i WHERE i.alumno_id = a.id AND i.estado = 'activa') as num_inscripciones,
            t.nombre as tutor_nombre
        FROM alumnos a
        LEFT JOIN sedes s ON a.sede_preferida_id = s.id
        LEFT JOIN tutores t ON t.alumno_id = a.id AND t.es_contacto_principal = 1
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (a.nombre LIKE ? OR a.apellidos LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])

    if sede_id:
        query += " AND a.sede_preferida_id = ?"
        params.append(sede_id)

    if estado == 'activo':
        query += " AND a.activo = 1"
    elif estado == 'inactivo':
        query += " AND a.activo = 0"

    query += " ORDER BY a.apellidos, a.nombre"

    cursor.execute(query, params)
    alumnos = cursor.fetchall()

    # Obtener sedes para filtro
    cursor.execute("SELECT id, nombre FROM sedes")
    sedes = cursor.fetchall()

    conn.close()

    return render_template('alumnos/list.html',
                         alumnos=alumnos,
                         sedes=sedes,
                         search=search,
                         sede_id=sede_id,
                         estado=estado)


@app.route('/alumnos/<int:id>')
def alumno_detail(id):
    """Detalle de un alumno"""
    conn = get_db()
    cursor = conn.cursor()

    # Datos del alumno
    cursor.execute("""
        SELECT a.*, s.nombre as sede_nombre
        FROM alumnos a
        LEFT JOIN sedes s ON a.sede_preferida_id = s.id
        WHERE a.id = ?
    """, (id,))
    alumno = cursor.fetchone()

    if not alumno:
        flash('Alumno no encontrado', 'error')
        return redirect(url_for('alumnos_list'))

    # Tutores
    cursor.execute("""
        SELECT * FROM tutores WHERE alumno_id = ?
    """, (id,))
    tutores = cursor.fetchall()

    # Inscripciones
    cursor.execute("""
        SELECT
            i.*,
            act.nombre as actividad_nombre,
            ar.nombre as area_nombre,
            ar.icono as area_icono,
            p.nombre as profesor_nombre,
            s.nombre as sede_nombre,
            COALESCE(i.precio_especial, act.precio_mensual) as precio
        FROM inscripciones i
        JOIN actividades act ON i.actividad_id = act.id
        JOIN areas ar ON act.area_id = ar.id
        LEFT JOIN profesores p ON i.profesor_id = p.id
        JOIN sedes s ON i.sede_id = s.id
        WHERE i.alumno_id = ?
        ORDER BY i.estado = 'activa' DESC, i.fecha_inscripcion DESC
    """, (id,))
    inscripciones = cursor.fetchall()

    # Ausencias
    cursor.execute("""
        SELECT aus.*, act.nombre as actividad_nombre
        FROM ausencias aus
        LEFT JOIN inscripciones i ON aus.inscripcion_id = i.id
        LEFT JOIN actividades act ON i.actividad_id = act.id
        WHERE aus.alumno_id = ?
        ORDER BY aus.fecha DESC
        LIMIT 10
    """, (id,))
    ausencias = cursor.fetchall()

    conn.close()

    return render_template('alumnos/detail.html',
                         alumno=alumno,
                         tutores=tutores,
                         inscripciones=inscripciones,
                         ausencias=ausencias)


# ============================================
# MÓDULO: INSCRIPCIONES
# ============================================

@app.route('/inscripciones')
def inscripciones_list():
    """Lista de inscripciones"""
    conn = get_db()
    cursor = conn.cursor()

    # Filtros
    area_id = request.args.get('area', '')
    sede_id = request.args.get('sede', '')
    estado = request.args.get('estado', 'activa')

    query = """
        SELECT
            i.id,
            al.nombre || ' ' || al.apellidos as alumno_nombre,
            al.edad,
            act.nombre as actividad_nombre,
            ar.nombre as area_nombre,
            ar.icono as area_icono,
            p.nombre as profesor_nombre,
            s.nombre as sede_nombre,
            i.dia_semana,
            i.hora_inicio,
            i.estado,
            COALESCE(i.precio_especial, act.precio_mensual) as precio
        FROM inscripciones i
        JOIN alumnos al ON i.alumno_id = al.id
        JOIN actividades act ON i.actividad_id = act.id
        JOIN areas ar ON act.area_id = ar.id
        LEFT JOIN profesores p ON i.profesor_id = p.id
        JOIN sedes s ON i.sede_id = s.id
        WHERE 1=1
    """
    params = []

    if area_id:
        query += " AND ar.id = ?"
        params.append(area_id)

    if sede_id:
        query += " AND i.sede_id = ?"
        params.append(sede_id)

    if estado:
        query += " AND i.estado = ?"
        params.append(estado)

    query += " ORDER BY ar.nombre, act.nombre, al.apellidos"

    cursor.execute(query, params)
    inscripciones = cursor.fetchall()

    # Obtener filtros
    cursor.execute("SELECT id, nombre, icono FROM areas ORDER BY nombre")
    areas = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM sedes")
    sedes = cursor.fetchall()

    conn.close()

    return render_template('inscripciones/list.html',
                         inscripciones=inscripciones,
                         areas=areas,
                         sedes=sedes,
                         area_id=area_id,
                         sede_id=sede_id,
                         estado=estado)


# ============================================
# MÓDULO: HORARIOS
# ============================================

@app.route('/horarios')
def horarios_view():
    """Vista de horarios"""
    conn = get_db()
    cursor = conn.cursor()

    # Filtros
    profesor_id = request.args.get('profesor', '')
    sede_id = request.args.get('sede', '')
    dia = request.args.get('dia', '')

    # Construir horario
    query = """
        SELECT
            i.dia_semana,
            i.hora_inicio,
            act.nombre as actividad,
            ar.icono,
            p.nombre as profesor,
            s.nombre as sede,
            COUNT(i.id) as num_alumnos
        FROM inscripciones i
        JOIN actividades act ON i.actividad_id = act.id
        JOIN areas ar ON act.area_id = ar.id
        LEFT JOIN profesores p ON i.profesor_id = p.id
        JOIN sedes s ON i.sede_id = s.id
        WHERE i.estado = 'activa'
    """
    params = []

    if profesor_id:
        query += " AND i.profesor_id = ?"
        params.append(profesor_id)

    if sede_id:
        query += " AND i.sede_id = ?"
        params.append(sede_id)

    if dia:
        query += " AND i.dia_semana = ?"
        params.append(dia)

    query += """
        GROUP BY i.dia_semana, i.hora_inicio, act.id, p.id, s.id
        ORDER BY
            CASE i.dia_semana
                WHEN 'Lunes' THEN 1
                WHEN 'Martes' THEN 2
                WHEN 'Miércoles' THEN 3
                WHEN 'Jueves' THEN 4
                WHEN 'Viernes' THEN 5
            END,
            i.hora_inicio
    """

    cursor.execute(query, params)
    horarios = cursor.fetchall()

    # Organizar por día
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horarios_por_dia = {dia: [] for dia in dias}
    for h in horarios:
        if h['dia_semana'] in horarios_por_dia:
            horarios_por_dia[h['dia_semana']].append(h)

    # Filtros
    cursor.execute("SELECT id, nombre FROM profesores WHERE activo = 1 ORDER BY nombre")
    profesores = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM sedes")
    sedes = cursor.fetchall()

    conn.close()

    return render_template('horarios/view.html',
                         horarios_por_dia=horarios_por_dia,
                         dias=dias,
                         profesores=profesores,
                         sedes=sedes,
                         profesor_id=profesor_id,
                         sede_id=sede_id,
                         dia_seleccionado=dia)


# ============================================
# MÓDULO: AUSENCIAS
# ============================================

@app.route('/ausencias')
def ausencias_list():
    """Lista de ausencias"""
    conn = get_db()
    cursor = conn.cursor()

    # Filtros
    fecha_desde = request.args.get('desde', '')
    fecha_hasta = request.args.get('hasta', '')
    justificada = request.args.get('justificada', '')

    query = """
        SELECT
            aus.id,
            aus.fecha,
            al.nombre || ' ' || al.apellidos as alumno_nombre,
            act.nombre as actividad_nombre,
            aus.motivo,
            aus.justificada,
            aus.notificado_profesor
        FROM ausencias aus
        JOIN alumnos al ON aus.alumno_id = al.id
        LEFT JOIN inscripciones i ON aus.inscripcion_id = i.id
        LEFT JOIN actividades act ON i.actividad_id = act.id
        WHERE 1=1
    """
    params = []

    if fecha_desde:
        query += " AND aus.fecha >= ?"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND aus.fecha <= ?"
        params.append(fecha_hasta)

    if justificada == '1':
        query += " AND aus.justificada = 1"
    elif justificada == '0':
        query += " AND aus.justificada = 0"

    query += " ORDER BY aus.fecha DESC"

    cursor.execute(query, params)
    ausencias = cursor.fetchall()

    # Estadísticas
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN justificada = 1 THEN 1 ELSE 0 END) as justificadas,
            SUM(CASE WHEN justificada = 0 THEN 1 ELSE 0 END) as no_justificadas
        FROM ausencias
        WHERE fecha >= date('now', '-30 days')
    """)
    stats = cursor.fetchone()

    conn.close()

    return render_template('ausencias/list.html',
                         ausencias=ausencias,
                         stats=stats,
                         fecha_desde=fecha_desde,
                         fecha_hasta=fecha_hasta,
                         justificada=justificada)


# ============================================
# MÓDULO: PAGOS
# ============================================

@app.route('/pagos')
def pagos_list():
    """Vista de pagos y facturación"""
    conn = get_db()
    cursor = conn.cursor()

    mes = request.args.get('mes', datetime.now().month)
    anio = request.args.get('anio', datetime.now().year)

    # Calcular pagos por profesor
    cursor.execute("""
        SELECT
            p.id,
            p.nombre,
            p.especialidad,
            pc.tipo_pago,
            pc.tarifa_hora,
            pc.tarifa_alumno,
            pc.cantidad_fija,
            pc.porcentaje_ingresos,
            COUNT(DISTINCT i.alumno_id) as num_alumnos,
            COUNT(DISTINCT i.id) as num_clases
        FROM profesores p
        LEFT JOIN proveedores_config pc ON pc.profesor_id = p.id
        LEFT JOIN inscripciones i ON i.profesor_id = p.id AND i.estado = 'activa'
        WHERE p.activo = 1
        GROUP BY p.id
        ORDER BY p.nombre
    """)
    profesores_raw = cursor.fetchall()

    # Calcular importes según tipo de pago
    pagos = []
    total_pagos = 0

    for prof in profesores_raw:
        pago = dict(prof)
        tipo = pago['tipo_pago']
        importe = 0

        if tipo == 'hora':
            # Estimación: 4 semanas * clases por semana * tarifa
            horas_mes = pago['num_clases'] * 4  # Simplificación
            importe = (pago['tarifa_hora'] or 0) * horas_mes

        elif tipo == 'alumno':
            importe = (pago['tarifa_alumno'] or 0) * (pago['num_alumnos'] or 0)

        elif tipo == 'fijo':
            importe = pago['cantidad_fija'] or 0

        elif tipo == 'mixto_alumno':
            importe = (pago['cantidad_fija'] or 0) + (pago['tarifa_alumno'] or 0) * (pago['num_alumnos'] or 0)

        elif tipo == 'mixto_porcentaje':
            # Calcular ingresos del profesor
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(i.precio_especial, a.precio_mensual)), 0)
                FROM inscripciones i
                JOIN actividades a ON i.actividad_id = a.id
                WHERE i.profesor_id = ? AND i.estado = 'activa'
            """, (pago['id'],))
            ingresos = cursor.fetchone()[0] or 0
            importe = (pago['cantidad_fija'] or 0) + (ingresos * (pago['porcentaje_ingresos'] or 0) / 100)

        elif tipo == 'mixto_hora_alumno':
            horas_mes = pago['num_clases'] * 4
            importe = (pago['tarifa_hora'] or 0) * horas_mes + (pago['tarifa_alumno'] or 0) * (pago['num_alumnos'] or 0)

        pago['importe_calculado'] = importe
        total_pagos += importe
        pagos.append(pago)

    # Tipos de pago para leyenda
    tipos_pago = {
        'hora': 'Por horas trabajadas',
        'alumno': 'Por número de alumnos',
        'fijo': 'Cantidad fija mensual',
        'mixto_alumno': 'Fijo + por alumno',
        'mixto_porcentaje': 'Fijo + % de ingresos',
        'mixto_hora_alumno': 'Por hora + por alumno'
    }

    conn.close()

    return render_template('pagos/list.html',
                         pagos=pagos,
                         total_pagos=total_pagos,
                         tipos_pago=tipos_pago,
                         mes=int(mes),
                         anio=int(anio))


# ============================================
# API ENDPOINTS (para AJAX)
# ============================================

@app.route('/api/stats')
def api_stats():
    """Estadísticas en JSON"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE activo = 1")
    alumnos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inscripciones WHERE estado = 'activa'")
    inscripciones = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ausencias WHERE fecha >= date('now', '-7 days')")
    ausencias_semana = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        'alumnos_activos': alumnos,
        'inscripciones_activas': inscripciones,
        'ausencias_semana': ausencias_semana
    })


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("FACTORÍA DEMO - Sistema de Gestión")
    print("=" * 50)
    print(f"\n📁 Base de datos: {DB_PATH}")

    if not DB_PATH.exists():
        print("\n❌ Error: Base de datos no encontrada")
        print("   Ejecuta primero:")
        print("   python scripts/init_database.py")
        print("   python scripts/generate_students.py")
    else:
        print("\n🚀 Iniciando servidor...")
        print("   URL: http://127.0.0.1:5000")
        print("\n   Ctrl+C para detener\n")
        app.run(host='127.0.0.1', debug=True, port=5000, use_reloader=False)
