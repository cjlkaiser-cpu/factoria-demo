#!/usr/bin/env python3
"""
Generador de Alumnos Sintéticos para Factoría Demo
Usa Faker con locale español para datos realistas
"""

import sqlite3
import random
from datetime import date, timedelta
from pathlib import Path
from faker import Faker

# Configuración
NUM_ALUMNOS = 50
DB_PATH = Path(__file__).parent.parent / "database" / "factoria_demo.db"

# Faker con locale español
fake = Faker('es_ES')
Faker.seed(42)  # Para reproducibilidad
random.seed(42)


def calculate_age(birth_date: date) -> int:
    """Calcula la edad a partir de la fecha de nacimiento"""
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def generate_student() -> dict:
    """
    Genera un alumno sintético realista

    Distribución de edades:
    - 50% niños (6-12 años)
    - 30% adolescentes (13-17 años)
    - 20% adultos (18-45 años)
    """
    # Determinar grupo de edad
    age_group = random.choices(
        ['nino', 'adolescente', 'adulto'],
        weights=[50, 30, 20]
    )[0]

    if age_group == 'nino':
        edad = random.randint(6, 12)
    elif age_group == 'adolescente':
        edad = random.randint(13, 17)
    else:
        edad = random.randint(18, 45)

    is_minor = edad < 18

    # Generar fecha de nacimiento
    today = date.today()
    birth_year = today.year - edad
    birth_date = fake.date_of_birth(minimum_age=edad, maximum_age=edad)

    # Generar datos del alumno
    student = {
        'nombre': fake.first_name(),
        'apellidos': f"{fake.last_name()} {fake.last_name()}",
        'fecha_nacimiento': birth_date.isoformat(),
        'edad': edad,
        'email': fake.email() if not is_minor else None,
        'telefono': fake.phone_number() if not is_minor else None,
        'direccion': fake.address().replace('\n', ', '),
        'sede_preferida_id': random.choice([1, 2]),
        'fecha_alta': fake.date_between(start_date='-2y', end_date='today').isoformat(),
        'activo': random.random() > 0.05,  # 95% activos
        'notas': random.choice([None, None, None, 'Alumno con beca', 'Horario flexible', 'Requiere atención especial'])
    }

    return student, is_minor


def generate_tutor(alumno_id: int) -> dict:
    """Genera un tutor para alumnos menores"""
    relacion = random.choice(['Padre', 'Madre', 'Madre', 'Padre', 'Tutor legal'])

    # Generar nombre acorde a la relación
    if relacion == 'Madre':
        nombre = fake.first_name_female() + ' ' + fake.last_name()
    elif relacion == 'Padre':
        nombre = fake.first_name_male() + ' ' + fake.last_name()
    else:
        nombre = fake.name()

    return {
        'alumno_id': alumno_id,
        'nombre': nombre,
        'relacion': relacion,
        'email': fake.email(),
        'telefono': fake.phone_number(),
        'es_contacto_principal': True
    }


def generate_inscriptions(conn: sqlite3.Connection, alumno_id: int, sede_id: int, edad: int):
    """
    Genera inscripciones realistas para un alumno

    - Niños: 1-3 actividades (música, robótica, danza)
    - Adolescentes: 1-2 actividades
    - Adultos: 1 actividad generalmente
    """
    cursor = conn.cursor()

    # Determinar número de actividades según edad
    if edad <= 12:
        num_actividades = random.choices([1, 2, 3], weights=[30, 50, 20])[0]
    elif edad <= 17:
        num_actividades = random.choices([1, 2], weights=[60, 40])[0]
    else:
        num_actividades = random.choices([1, 2], weights=[80, 20])[0]

    # Obtener actividades disponibles
    cursor.execute("""
        SELECT a.id, a.nombre, a.area_id, ar.nombre as area_nombre, a.nivel
        FROM actividades a
        JOIN areas ar ON a.area_id = ar.id
        WHERE a.activa = 1
    """)
    actividades = cursor.fetchall()

    # Filtrar actividades apropiadas por edad
    actividades_apropiadas = []
    for act in actividades:
        nivel = act[4] or ''
        # Simplificación: cualquier actividad es apropiada, pero preferimos ciertas áreas por edad
        actividades_apropiadas.append(act)

    if not actividades_apropiadas:
        return

    # Seleccionar actividades al azar sin repetir área
    seleccionadas = random.sample(
        actividades_apropiadas,
        min(num_actividades, len(actividades_apropiadas))
    )

    # Obtener profesores por actividad/área
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    horas = ['16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30']

    for act in seleccionadas:
        act_id = act[0]
        area_id = act[2]

        # Buscar profesor para esta área
        cursor.execute("""
            SELECT id FROM profesores
            WHERE activo = 1
            ORDER BY RANDOM()
            LIMIT 1
        """)
        profesor = cursor.fetchone()
        profesor_id = profesor[0] if profesor else None

        # Generar inscripción
        cursor.execute("""
            INSERT INTO inscripciones (
                alumno_id, actividad_id, profesor_id, sede_id,
                curso_escolar, dia_semana, hora_inicio, estado,
                fecha_inscripcion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alumno_id,
            act_id,
            profesor_id,
            sede_id,
            '2024-2025',
            random.choice(dias_semana),
            random.choice(horas),
            random.choices(['activa', 'activa', 'activa', 'pendiente', 'baja'], weights=[70, 15, 10, 3, 2])[0],
            fake.date_between(start_date='-6m', end_date='today').isoformat()
        ))

    conn.commit()


def generate_absences(conn: sqlite3.Connection, alumno_id: int):
    """
    Genera ausencias realistas para un alumno
    Aproximadamente 0-5 ausencias por alumno
    """
    cursor = conn.cursor()

    # Obtener inscripciones del alumno
    cursor.execute("""
        SELECT id FROM inscripciones
        WHERE alumno_id = ? AND estado = 'activa'
    """, (alumno_id,))
    inscripciones = cursor.fetchall()

    if not inscripciones:
        return

    # Generar 0-5 ausencias
    num_ausencias = random.choices([0, 1, 2, 3, 4, 5], weights=[40, 25, 15, 10, 7, 3])[0]

    motivos = [
        'Enfermedad',
        'Cita médica',
        'Viaje familiar',
        'Actividad escolar',
        'Motivos personales',
        None
    ]

    for _ in range(num_ausencias):
        inscripcion = random.choice(inscripciones)
        cursor.execute("""
            INSERT INTO ausencias (
                alumno_id, inscripcion_id, fecha, motivo, justificada, notificado_profesor
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            alumno_id,
            inscripcion[0],
            fake.date_between(start_date='-3m', end_date='today').isoformat(),
            random.choice(motivos),
            random.random() > 0.3,  # 70% justificadas
            random.random() > 0.1   # 90% notificadas
        ))

    conn.commit()


def main():
    """Función principal de generación de datos"""
    print("=" * 50)
    print("GENERADOR DE DATOS SINTÉTICOS - FACTORÍA DEMO")
    print("=" * 50)

    # Verificar que la BD existe
    if not DB_PATH.exists():
        print(f"\n❌ Error: No se encuentra la base de datos en {DB_PATH}")
        print("   Ejecuta primero: python scripts/init_database.py")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar que hay datos reales
    cursor.execute("SELECT COUNT(*) FROM profesores")
    num_profesores = cursor.fetchone()[0]
    if num_profesores == 0:
        print("\n❌ Error: No hay profesores en la BD")
        print("   Ejecuta primero: python scripts/init_database.py")
        conn.close()
        return

    print(f"\n📊 Base de datos: {DB_PATH}")
    print(f"   Profesores existentes: {num_profesores}")

    # Limpiar datos sintéticos previos
    print("\n🗑️  Limpiando datos sintéticos anteriores...")
    cursor.execute("DELETE FROM ausencias")
    cursor.execute("DELETE FROM inscripciones")
    cursor.execute("DELETE FROM tutores")
    cursor.execute("DELETE FROM alumnos")
    conn.commit()

    # Generar alumnos
    print(f"\n👥 Generando {NUM_ALUMNOS} alumnos sintéticos...")
    alumnos_generados = 0
    tutores_generados = 0

    for i in range(NUM_ALUMNOS):
        student, is_minor = generate_student()

        # Insertar alumno
        cursor.execute("""
            INSERT INTO alumnos (
                nombre, apellidos, fecha_nacimiento, edad, email, telefono,
                direccion, sede_preferida_id, fecha_alta, activo, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student['nombre'],
            student['apellidos'],
            student['fecha_nacimiento'],
            student['edad'],
            student['email'],
            student['telefono'],
            student['direccion'],
            student['sede_preferida_id'],
            student['fecha_alta'],
            student['activo'],
            student['notas']
        ))

        alumno_id = cursor.lastrowid
        alumnos_generados += 1

        # Generar tutor si es menor
        if is_minor:
            tutor = generate_tutor(alumno_id)
            cursor.execute("""
                INSERT INTO tutores (
                    alumno_id, nombre, relacion, email, telefono, es_contacto_principal
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                tutor['alumno_id'],
                tutor['nombre'],
                tutor['relacion'],
                tutor['email'],
                tutor['telefono'],
                tutor['es_contacto_principal']
            ))
            tutores_generados += 1

            # Segundo tutor (50% de probabilidad)
            if random.random() > 0.5:
                tutor2 = generate_tutor(alumno_id)
                tutor2['es_contacto_principal'] = False
                # Cambiar relación para que sea diferente
                if tutor['relacion'] == 'Madre':
                    tutor2['relacion'] = 'Padre'
                    tutor2['nombre'] = fake.first_name_male() + ' ' + fake.last_name()
                elif tutor['relacion'] == 'Padre':
                    tutor2['relacion'] = 'Madre'
                    tutor2['nombre'] = fake.first_name_female() + ' ' + fake.last_name()

                cursor.execute("""
                    INSERT INTO tutores (
                        alumno_id, nombre, relacion, email, telefono, es_contacto_principal
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    tutor2['alumno_id'],
                    tutor2['nombre'],
                    tutor2['relacion'],
                    tutor2['email'],
                    tutor2['telefono'],
                    tutor2['es_contacto_principal']
                ))
                tutores_generados += 1

        conn.commit()

        # Generar inscripciones
        if student['activo']:
            generate_inscriptions(conn, alumno_id, student['sede_preferida_id'], student['edad'])

            # Generar ausencias
            generate_absences(conn, alumno_id)

        # Progreso
        if (i + 1) % 10 == 0:
            print(f"   Progreso: {i + 1}/{NUM_ALUMNOS}")

    # Estadísticas finales
    cursor.execute("SELECT COUNT(*) FROM alumnos")
    total_alumnos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tutores")
    total_tutores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inscripciones")
    total_inscripciones = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ausencias")
    total_ausencias = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE edad < 18")
    menores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE activo = 1")
    activos = cursor.fetchone()[0]

    print("\n" + "=" * 50)
    print("✅ GENERACIÓN COMPLETADA")
    print("=" * 50)
    print(f"\n📈 Estadísticas:")
    print(f"   • Alumnos generados:      {total_alumnos}")
    print(f"   • Alumnos activos:        {activos}")
    print(f"   • Menores de edad:        {menores}")
    print(f"   • Tutores generados:      {total_tutores}")
    print(f"   • Inscripciones creadas:  {total_inscripciones}")
    print(f"   • Ausencias registradas:  {total_ausencias}")

    # Distribución por sede
    cursor.execute("""
        SELECT s.nombre, COUNT(a.id)
        FROM sedes s
        LEFT JOIN alumnos a ON a.sede_preferida_id = s.id
        GROUP BY s.id
    """)
    print(f"\n📍 Distribución por sede:")
    for row in cursor.fetchall():
        print(f"   • {row[0]}: {row[1]} alumnos")

    # Distribución por área
    cursor.execute("""
        SELECT ar.nombre, COUNT(i.id)
        FROM areas ar
        LEFT JOIN actividades a ON a.area_id = ar.id
        LEFT JOIN inscripciones i ON i.actividad_id = a.id AND i.estado = 'activa'
        GROUP BY ar.id
        ORDER BY COUNT(i.id) DESC
        LIMIT 5
    """)
    print(f"\n🎯 Top 5 áreas por inscripciones:")
    for row in cursor.fetchall():
        print(f"   • {row[0]}: {row[1]} inscripciones")

    conn.close()
    print(f"\n💾 Datos guardados en: {DB_PATH}")


if __name__ == "__main__":
    main()
