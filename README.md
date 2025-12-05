# Factoría Demo

Sistema de gestión para escuela de artes **Factoría Estudio** - Demo con datos sintéticos.

## Características

- **Dashboard**: Estadísticas generales y resumen
- **Alumnos**: Gestión completa de alumnos y tutores
- **Inscripciones**: Control de matrículas en actividades
- **Horarios**: Vista semanal de clases
- **Ausencias**: Registro y seguimiento
- **Pagos**: Cálculo automático con 7 tipos de pago

## Stack Tecnológico

- **Backend**: Flask (Python)
- **Base de datos**: SQLite
- **Frontend**: Bootstrap 5 + HTML/CSS
- **Datos sintéticos**: Faker (español)

## Instalación

### 1. Clonar/Descargar el proyecto

```bash
cd ~/Desktop/factoria-demo
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
# o en Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Inicializar base de datos

```bash
python scripts/init_database.py
```

Esto creará la BD con:
- 2 sedes (Valdemarín, Conde Orgaz)
- 11 áreas de actividades
- ~80 actividades
- 30 profesores reales (datos de la web)
- Configuración de pagos (7 tipos)

### 5. Generar datos sintéticos

```bash
python scripts/generate_students.py
```

Esto creará:
- 50 alumnos sintéticos
- Tutores para menores
- Inscripciones aleatorias
- Historial de ausencias

### 6. Ejecutar la aplicación

```bash
python app/main.py
```

Abre: **http://localhost:5000**

## Estructura del Proyecto

```
factoria-demo/
├── database/
│   ├── schema.sql              # Modelo de datos
│   ├── seed_real_data.sql      # Datos reales (profesores, actividades)
│   └── factoria_demo.db        # Base de datos SQLite
│
├── scripts/
│   ├── init_database.py        # Inicializador de BD
│   └── generate_students.py    # Generador de alumnos sintéticos
│
├── app/
│   ├── main.py                 # Aplicación Flask
│   ├── templates/              # Plantillas HTML
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── alumnos/
│   │   ├── inscripciones/
│   │   ├── horarios/
│   │   ├── ausencias/
│   │   └── pagos/
│   └── static/
│       └── css/
│
├── requirements.txt
└── README.md
```

## Tipos de Pago Implementados

| Tipo | Descripción |
|------|-------------|
| `hora` | Pago por horas trabajadas |
| `alumno` | Pago por número de alumnos |
| `fijo` | Cantidad fija mensual |
| `mixto_alumno` | Fijo + por alumno |
| `mixto_porcentaje` | Fijo + % de ingresos |
| `mixto_hora_alumno` | Por hora + por alumno |

## Datos de la Demo

### Reales (de factoriaestudio.es)
- Sedes
- Áreas (Música, Danza, Robótica, etc.)
- Actividades (~80)
- Profesores (~30)

### Sintéticos (generados)
- Alumnos (50)
- Tutores
- Inscripciones
- Ausencias
- Pagos calculados

## Próximos Pasos (Producción)

Para pasar a producción:

1. Migrar de SQLite → PostgreSQL (Supabase)
2. Implementar autenticación
3. Desplegar en Vercel/Railway
4. Conectar con datos reales
5. Implementar módulo de facturación completo

## Notas

- Esta es una **DEMO** con datos sintéticos
- Los datos de profesores son públicos (web de Factoría)
- Los alumnos son 100% ficticios (Faker)
- El cálculo de pagos es una estimación

---

**Versión**: 1.0 - Diciembre 2024
**Desarrollado con**: Claude Code
