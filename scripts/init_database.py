#!/usr/bin/env python3
"""
Inicializador de Base de Datos - Factoría Demo
Crea la BD SQLite y carga los datos reales
"""

import sqlite3
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "factoria_demo.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SEED_PATH = DB_DIR / "seed_real_data.sql"


def init_database():
    """Inicializa la base de datos con schema y datos reales"""

    print("=" * 50)
    print("INICIALIZADOR DE BASE DE DATOS - FACTORÍA DEMO")
    print("=" * 50)

    # Verificar archivos SQL
    if not SCHEMA_PATH.exists():
        print(f"\n❌ Error: No se encuentra {SCHEMA_PATH}")
        return False

    if not SEED_PATH.exists():
        print(f"\n❌ Error: No se encuentra {SEED_PATH}")
        return False

    # Crear directorio si no existe
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Eliminar BD existente
    if DB_PATH.exists():
        print(f"\n⚠️  Eliminando base de datos existente: {DB_PATH}")
        DB_PATH.unlink()

    # Crear conexión
    print(f"\n📁 Creando base de datos: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ejecutar schema
    print("\n📋 Ejecutando schema.sql...")
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    print("   ✓ Tablas creadas correctamente")

    # Ejecutar datos reales
    print("\n📥 Cargando datos reales (seed_real_data.sql)...")
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        seed_sql = f.read()
    cursor.executescript(seed_sql)
    conn.commit()
    print("   ✓ Datos reales cargados")

    # Verificar datos
    print("\n📊 Verificando datos cargados:")

    tables = [
        ('sedes', 'Sedes'),
        ('areas', 'Áreas'),
        ('actividades', 'Actividades'),
        ('profesores', 'Profesores'),
        ('proveedores_config', 'Configuraciones de pago')
    ]

    for table, name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   • {name}: {count}")

    # Mostrar resumen de áreas
    print("\n🎯 Actividades por área:")
    cursor.execute("""
        SELECT ar.nombre, ar.num_actividades, COUNT(a.id) as real_count
        FROM areas ar
        LEFT JOIN actividades a ON a.area_id = ar.id
        GROUP BY ar.id
        ORDER BY real_count DESC
    """)
    for row in cursor.fetchall():
        print(f"   • {row[0]}: {row[2]} actividades")

    # Mostrar tipos de pago configurados
    print("\n💰 Configuraciones de pago por tipo:")
    cursor.execute("""
        SELECT tipo_pago, COUNT(*) as num
        FROM proveedores_config
        GROUP BY tipo_pago
        ORDER BY num DESC
    """)
    for row in cursor.fetchall():
        print(f"   • {row[0]}: {row[1]} profesores")

    conn.close()

    print("\n" + "=" * 50)
    print("✅ BASE DE DATOS INICIALIZADA CORRECTAMENTE")
    print("=" * 50)
    print(f"\n💾 Archivo: {DB_PATH}")
    print("\n📝 Siguiente paso:")
    print("   python scripts/generate_students.py")

    return True


if __name__ == "__main__":
    init_database()
