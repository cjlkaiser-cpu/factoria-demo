-- ============================================
-- FACTORÍA ESTUDIO - Schema de Base de Datos
-- Demo con datos sintéticos
-- ============================================

-- Eliminar tablas si existen (para reiniciar)
DROP TABLE IF EXISTS pagos_mensuales;
DROP TABLE IF EXISTS facturas;
DROP TABLE IF EXISTS proveedores_config;
DROP TABLE IF EXISTS ausencias;
DROP TABLE IF EXISTS inscripciones;
DROP TABLE IF EXISTS tutores;
DROP TABLE IF EXISTS alumnos;
DROP TABLE IF EXISTS horarios_disponibles;
DROP TABLE IF EXISTS profesores;
DROP TABLE IF EXISTS actividades;
DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS sedes;

-- ============================================
-- ENTIDADES REALES (datos de la web)
-- ============================================

-- Sedes de Factoría Estudio
CREATE TABLE sedes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Áreas de actividades (Música, Danza, etc.)
CREATE TABLE areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    icono TEXT,  -- Para la UI (emoji o clase CSS)
    num_actividades INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Catálogo de actividades
CREATE TABLE actividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    area_id INTEGER REFERENCES areas(id),
    nivel TEXT,                    -- Iniciación, Elemental, Medio, Profesional
    modalidad TEXT,                -- Individual, Grupal, Colectiva
    duracion_minutos INTEGER DEFAULT 60,
    precio_mensual DECIMAL(8,2),
    descripcion TEXT,
    activa BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Profesores (datos reales de la web)
CREATE TABLE profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    especialidad TEXT,
    bio TEXT,
    email TEXT,
    telefono TEXT,
    sede_principal_id INTEGER REFERENCES sedes(id),
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Horarios disponibles por profesor
CREATE TABLE horarios_disponibles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER REFERENCES profesores(id),
    sede_id INTEGER REFERENCES sedes(id),
    dia_semana TEXT NOT NULL,      -- Lunes, Martes, etc.
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ENTIDADES SINTÉTICAS (generadas)
-- ============================================

-- Alumnos (100% sintéticos)
CREATE TABLE alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    fecha_nacimiento DATE,
    edad INTEGER,                  -- Calculado
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    sede_preferida_id INTEGER REFERENCES sedes(id),
    fecha_alta DATE DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT 1,
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tutores (para alumnos menores)
CREATE TABLE tutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE CASCADE,
    nombre TEXT NOT NULL,
    relacion TEXT,                 -- Padre, Madre, Tutor legal
    email TEXT NOT NULL,
    telefono TEXT,
    es_contacto_principal BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inscripciones de alumnos en actividades
CREATE TABLE inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL REFERENCES alumnos(id),
    actividad_id INTEGER NOT NULL REFERENCES actividades(id),
    profesor_id INTEGER REFERENCES profesores(id),
    sede_id INTEGER NOT NULL REFERENCES sedes(id),
    curso_escolar TEXT NOT NULL,   -- "2024-2025"
    dia_semana TEXT,
    hora_inicio TIME,
    estado TEXT DEFAULT 'activa',  -- activa, baja, pendiente, suspendida
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    fecha_baja DATE,
    precio_especial DECIMAL(8,2),  -- NULL = precio estándar
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registro de ausencias
CREATE TABLE ausencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL REFERENCES alumnos(id),
    inscripcion_id INTEGER REFERENCES inscripciones(id),
    fecha DATE NOT NULL,
    motivo TEXT,
    justificada BOOLEAN DEFAULT 0,
    notificado_profesor BOOLEAN DEFAULT 0,
    fecha_notificacion TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- GESTIÓN DE PAGOS Y FACTURACIÓN
-- ============================================

-- Configuración de pago por profesor/proveedor
CREATE TABLE proveedores_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL REFERENCES profesores(id),
    tipo_pago TEXT NOT NULL,       -- hora, alumno, fijo, mixto_alumno, mixto_porcentaje, mixto_hora_alumno
    tarifa_hora DECIMAL(8,2),
    tarifa_alumno DECIMAL(8,2),
    cantidad_fija DECIMAL(8,2),
    porcentaje_ingresos DECIMAL(5,2),
    iban TEXT,
    retencion_irpf DECIMAL(5,2) DEFAULT 15.00,
    notas TEXT,
    vigente_desde DATE DEFAULT CURRENT_DATE,
    vigente_hasta DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pagos mensuales calculados
CREATE TABLE pagos_mensuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL REFERENCES profesores(id),
    sede_id INTEGER REFERENCES sedes(id),
    mes INTEGER NOT NULL,          -- 1-12
    anio INTEGER NOT NULL,

    -- Desglose del cálculo
    horas_trabajadas DECIMAL(6,2),
    num_alumnos INTEGER,
    ingresos_generados DECIMAL(10,2),

    -- Importes
    importe_bruto DECIMAL(10,2),
    descuento_ausencias DECIMAL(10,2) DEFAULT 0,
    ajustes_manuales DECIMAL(10,2) DEFAULT 0,
    importe_neto DECIMAL(10,2),

    -- Estado
    estado TEXT DEFAULT 'calculado',  -- calculado, revisado, facturado, pagado
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,

    UNIQUE(profesor_id, sede_id, mes, anio)
);

-- Facturas recibidas de proveedores
CREATE TABLE facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pago_mensual_id INTEGER REFERENCES pagos_mensuales(id),
    profesor_id INTEGER NOT NULL REFERENCES profesores(id),

    -- Datos de la factura
    numero_factura TEXT NOT NULL,
    fecha_factura DATE NOT NULL,
    fecha_recepcion DATE DEFAULT CURRENT_DATE,

    -- Importes
    importe_base DECIMAL(10,2),
    iva DECIMAL(10,2) DEFAULT 0,
    retencion_irpf DECIMAL(10,2) DEFAULT 0,
    importe_total DECIMAL(10,2),

    -- Validación
    estado TEXT DEFAULT 'pendiente',  -- pendiente, validada, discrepancia, rechazada, pagada
    discrepancia_importe DECIMAL(10,2),
    notas_validacion TEXT,

    -- Archivo
    archivo_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(numero_factura, profesor_id)
);

-- ============================================
-- ÍNDICES PARA RENDIMIENTO
-- ============================================

CREATE INDEX idx_alumnos_sede ON alumnos(sede_preferida_id);
CREATE INDEX idx_alumnos_activo ON alumnos(activo);
CREATE INDEX idx_inscripciones_alumno ON inscripciones(alumno_id);
CREATE INDEX idx_inscripciones_profesor ON inscripciones(profesor_id);
CREATE INDEX idx_inscripciones_estado ON inscripciones(estado);
CREATE INDEX idx_inscripciones_curso ON inscripciones(curso_escolar);
CREATE INDEX idx_ausencias_fecha ON ausencias(fecha);
CREATE INDEX idx_ausencias_alumno ON ausencias(alumno_id);
CREATE INDEX idx_pagos_periodo ON pagos_mensuales(anio, mes);
CREATE INDEX idx_pagos_profesor ON pagos_mensuales(profesor_id);

-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista de alumnos con información completa
CREATE VIEW v_alumnos_completo AS
SELECT
    a.*,
    s.nombre as sede_nombre,
    t.nombre as tutor_nombre,
    t.email as tutor_email,
    t.telefono as tutor_telefono,
    (SELECT COUNT(*) FROM inscripciones i WHERE i.alumno_id = a.id AND i.estado = 'activa') as num_inscripciones
FROM alumnos a
LEFT JOIN sedes s ON a.sede_preferida_id = s.id
LEFT JOIN tutores t ON t.alumno_id = a.id AND t.es_contacto_principal = 1;

-- Vista de inscripciones con detalles
CREATE VIEW v_inscripciones_detalle AS
SELECT
    i.*,
    a.nombre || ' ' || a.apellidos as alumno_nombre,
    a.edad as alumno_edad,
    act.nombre as actividad_nombre,
    ar.nombre as area_nombre,
    p.nombre as profesor_nombre,
    s.nombre as sede_nombre,
    COALESCE(i.precio_especial, act.precio_mensual) as precio_efectivo
FROM inscripciones i
JOIN alumnos a ON i.alumno_id = a.id
JOIN actividades act ON i.actividad_id = act.id
JOIN areas ar ON act.area_id = ar.id
LEFT JOIN profesores p ON i.profesor_id = p.id
JOIN sedes s ON i.sede_id = s.id;

-- Vista de dashboard estadísticas
CREATE VIEW v_dashboard_stats AS
SELECT
    (SELECT COUNT(*) FROM alumnos WHERE activo = 1) as total_alumnos,
    (SELECT COUNT(*) FROM profesores WHERE activo = 1) as total_profesores,
    (SELECT COUNT(*) FROM inscripciones WHERE estado = 'activa') as inscripciones_activas,
    (SELECT COUNT(*) FROM ausencias WHERE fecha >= date('now', '-30 days')) as ausencias_mes,
    (SELECT SUM(precio_efectivo) FROM v_inscripciones_detalle WHERE estado = 'activa') as ingresos_mensuales;
