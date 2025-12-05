-- ============================================
-- FACTORÍA ESTUDIO - Datos Reales de la Web
-- Extraídos de https://factoriaestudio.es
-- ============================================

-- ============================================
-- SEDES
-- ============================================

INSERT INTO sedes (nombre, direccion, telefono, email) VALUES
('Valdemarín (Aravaca)', 'C/ Jimena Menéndez Pidal, nº 11, 28023 Madrid', '+34 659458185', 'factoria@colegio-estudio.es'),
('Conde Orgaz', 'Madrid - Conde Orgaz', '+34 659458185', 'factoria@colegio-estudio.es');

-- ============================================
-- ÁREAS DE ACTIVIDADES
-- ============================================

INSERT INTO areas (nombre, descripcion, icono, num_actividades) VALUES
('Música', 'Clases de instrumento, lenguaje musical, coro y conservatorio', '🎵', 22),
('Danza', 'Danza clásica, contemporánea y baile moderno', '💃', 11),
('Ingeniería y Robótica', 'Programación, robótica, electrónica y tecnología', '🤖', 21),
('Audiovisuales y Cine', 'Producción audiovisual, edición y cinematografía', '🎬', 8),
('Artes Plásticas', 'Dibujo, pintura, escultura y técnicas artísticas', '🎨', 5),
('Confección', 'Costura, diseño de moda y patronaje', '🧵', 3),
('Teatro', 'Interpretación, expresión corporal y teatro musical', '🎭', 4),
('Oratoria', 'Comunicación, debate y hablar en público', '🎤', 2),
('Magia', 'Ilusionismo y prestidigitación', '🪄', 1),
('Fotografía', 'Técnica fotográfica y edición digital', '📷', 2),
('Emprendimiento', 'Miniempresas, negocios y certificado SECOT', '💼', 2);

-- ============================================
-- ACTIVIDADES DE MÚSICA (22)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
-- Instrumentos de cuerda
('Piano', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Clases individuales de piano clásico y moderno'),
('Piano', 1, 'Todos los niveles', 'Individual', 45, 110.00, 'Clases individuales de piano - sesión extendida'),
('Violín', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica violinística desde iniciación'),
('Viola', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Clases de viola para todos los niveles'),
('Violonchelo', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica y repertorio de violonchelo'),
('Contrabajo', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Clases de contrabajo clásico y jazz'),
('Guitarra clásica', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Guitarra española y clásica'),
('Guitarra eléctrica', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Rock, pop, blues y técnicas modernas'),
('Bajo eléctrico', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica de bajo para todos los estilos'),

-- Viento
('Flauta travesera', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica de flauta clásica'),
('Clarinete', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Clases de clarinete'),
('Saxofón', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Saxofón clásico y jazz'),
('Trompeta', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica de trompeta'),

-- Percusión y otros
('Batería', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Batería y percusión moderna'),
('Percusión', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Instrumentos de percusión clásica'),

-- Voz y teoría
('Canto', 1, 'Todos los niveles', 'Individual', 30, 85.00, 'Técnica vocal y repertorio'),
('Canto', 1, 'Todos los niveles', 'Individual', 45, 110.00, 'Técnica vocal - sesión extendida'),
('Lenguaje Musical', 1, 'Iniciación', 'Grupal', 60, 45.00, 'Solfeo, teoría y educación auditiva'),
('Coro', 1, 'Todos los niveles', 'Colectiva', 60, 35.00, 'Coro infantil y juvenil'),
('Combo/Banda', 1, 'Intermedio', 'Grupal', 60, 55.00, 'Práctica de conjunto instrumental'),

-- Conservatorio
('Grado Elemental - Instrumento', 1, 'Elemental', 'Individual', 30, 95.00, 'Preparación para conservatorio'),
('Grado Elemental - Lenguaje Musical', 1, 'Elemental', 'Grupal', 60, 55.00, 'Lenguaje musical nivel conservatorio');

-- ============================================
-- ACTIVIDADES DE DANZA (11)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Danza clásica - Iniciación', 2, 'Iniciación', 'Grupal', 60, 55.00, 'Primeros pasos en ballet clásico'),
('Danza clásica - Elemental', 2, 'Elemental', 'Grupal', 75, 65.00, 'Ballet clásico nivel elemental'),
('Danza clásica - Intermedio', 2, 'Intermedio', 'Grupal', 90, 75.00, 'Ballet clásico nivel intermedio'),
('Danza clásica - Avanzado', 2, 'Avanzado', 'Grupal', 90, 75.00, 'Ballet clásico nivel avanzado'),
('Danza contemporánea', 2, 'Todos los niveles', 'Grupal', 60, 55.00, 'Técnicas de danza contemporánea'),
('Baile moderno - Infantil', 2, 'Iniciación', 'Grupal', 60, 50.00, 'Hip-hop, funky y estilos urbanos para niños'),
('Baile moderno - Juvenil', 2, 'Intermedio', 'Grupal', 60, 55.00, 'Estilos urbanos para adolescentes'),
('Baile moderno - Adultos', 2, 'Todos los niveles', 'Grupal', 60, 55.00, 'Baile moderno para adultos'),
('Flamenco - Iniciación', 2, 'Iniciación', 'Grupal', 60, 55.00, 'Introducción al baile flamenco'),
('Flamenco - Intermedio', 2, 'Intermedio', 'Grupal', 60, 60.00, 'Técnica flamenca nivel medio'),
('Danza española', 2, 'Todos los niveles', 'Grupal', 60, 55.00, 'Escuela bolera y danza española');

-- ============================================
-- ACTIVIDADES DE ROBÓTICA (21)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Robótica - Iniciación (6-8 años)', 3, 'Iniciación', 'Grupal', 60, 65.00, 'Primeros pasos en robótica con LEGO'),
('Robótica - Elemental (9-11 años)', 3, 'Elemental', 'Grupal', 90, 75.00, 'Robótica educativa nivel elemental'),
('Robótica - Avanzado (12+ años)', 3, 'Avanzado', 'Grupal', 90, 85.00, 'Proyectos avanzados de robótica'),
('Programación Scratch', 3, 'Iniciación', 'Grupal', 60, 55.00, 'Introducción a la programación visual'),
('Programación Python', 3, 'Intermedio', 'Grupal', 90, 75.00, 'Programación con Python'),
('Desarrollo de videojuegos', 3, 'Intermedio', 'Grupal', 90, 75.00, 'Creación de videojuegos'),
('Electrónica básica', 3, 'Iniciación', 'Grupal', 60, 60.00, 'Circuitos y componentes electrónicos'),
('Arduino', 3, 'Intermedio', 'Grupal', 90, 75.00, 'Proyectos con Arduino'),
('Raspberry Pi', 3, 'Avanzado', 'Grupal', 90, 80.00, 'Proyectos con Raspberry Pi'),
('Impresión 3D', 3, 'Todos los niveles', 'Grupal', 90, 70.00, 'Diseño e impresión 3D'),
('Diseño CAD', 3, 'Intermedio', 'Grupal', 90, 70.00, 'Diseño asistido por ordenador'),
('Drones', 3, 'Intermedio', 'Grupal', 90, 85.00, 'Pilotaje y programación de drones'),
('Inteligencia Artificial Kids', 3, 'Elemental', 'Grupal', 60, 70.00, 'Introducción a la IA para niños'),
('Minecraft Educativo', 3, 'Iniciación', 'Grupal', 60, 55.00, 'Programación y lógica con Minecraft'),
('Roblox Studio', 3, 'Elemental', 'Grupal', 90, 65.00, 'Desarrollo en Roblox'),
('App Inventor', 3, 'Intermedio', 'Grupal', 90, 70.00, 'Creación de apps móviles'),
('Ciberseguridad Junior', 3, 'Avanzado', 'Grupal', 90, 80.00, 'Introducción a la ciberseguridad'),
('Competición robótica', 3, 'Avanzado', 'Grupal', 120, 95.00, 'Preparación para competiciones'),
('STEAM Lab', 3, 'Todos los niveles', 'Grupal', 90, 70.00, 'Proyectos interdisciplinares STEAM'),
('Tecnología creativa', 3, 'Iniciación', 'Grupal', 60, 55.00, 'Arte y tecnología combinados'),
('Makers', 3, 'Todos los niveles', 'Grupal', 90, 65.00, 'Cultura maker y fabricación digital');

-- ============================================
-- ACTIVIDADES AUDIOVISUALES (8)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Cine - Iniciación', 4, 'Iniciación', 'Grupal', 90, 70.00, 'Introducción al lenguaje cinematográfico'),
('Cine - Producción', 4, 'Intermedio', 'Grupal', 120, 85.00, 'Producción de cortometrajes'),
('Edición de vídeo', 4, 'Todos los niveles', 'Grupal', 90, 70.00, 'Premiere, Final Cut y DaVinci'),
('Animación 2D', 4, 'Intermedio', 'Grupal', 90, 75.00, 'Técnicas de animación tradicional y digital'),
('Animación 3D', 4, 'Avanzado', 'Grupal', 120, 90.00, 'Modelado y animación 3D'),
('YouTube y Streaming', 4, 'Todos los niveles', 'Grupal', 90, 65.00, 'Creación de contenido digital'),
('Podcast', 4, 'Todos los niveles', 'Grupal', 60, 55.00, 'Producción de podcasts'),
('Efectos especiales', 4, 'Avanzado', 'Grupal', 120, 95.00, 'VFX y postproducción');

-- ============================================
-- ARTES PLÁSTICAS (5)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Dibujo', 5, 'Todos los niveles', 'Grupal', 90, 60.00, 'Técnicas de dibujo artístico'),
('Pintura', 5, 'Todos los niveles', 'Grupal', 90, 65.00, 'Óleo, acrílico y acuarela'),
('Escultura', 5, 'Intermedio', 'Grupal', 90, 70.00, 'Modelado y escultura'),
('Ilustración', 5, 'Todos los niveles', 'Grupal', 90, 65.00, 'Ilustración tradicional y digital'),
('Cómic y Manga', 5, 'Todos los niveles', 'Grupal', 90, 65.00, 'Creación de cómic y manga');

-- ============================================
-- CONFECCIÓN (3)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Costura - Iniciación', 6, 'Iniciación', 'Grupal', 90, 70.00, 'Primeros pasos en costura'),
('Costura - Avanzado', 6, 'Avanzado', 'Grupal', 120, 85.00, 'Patronaje y confección avanzada'),
('Diseño de moda', 6, 'Intermedio', 'Grupal', 90, 75.00, 'Diseño y creación de moda');

-- ============================================
-- TEATRO (4)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Teatro - Infantil', 7, 'Iniciación', 'Grupal', 60, 55.00, 'Teatro para niños'),
('Teatro - Juvenil', 7, 'Intermedio', 'Grupal', 90, 65.00, 'Interpretación para adolescentes'),
('Teatro Musical', 7, 'Todos los niveles', 'Grupal', 120, 85.00, 'Canto, baile e interpretación'),
('Expresión corporal', 7, 'Todos los niveles', 'Grupal', 60, 50.00, 'Movimiento y expresión');

-- ============================================
-- ORATORIA (2)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Oratoria y debate', 8, 'Todos los niveles', 'Grupal', 60, 55.00, 'Técnicas de comunicación y debate'),
('Hablar en público', 8, 'Todos los niveles', 'Grupal', 60, 55.00, 'Perder el miedo escénico');

-- ============================================
-- MAGIA (1)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Magia e ilusionismo', 9, 'Todos los niveles', 'Grupal', 60, 60.00, 'Técnicas de magia y prestidigitación');

-- ============================================
-- FOTOGRAFÍA (2)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Fotografía - Iniciación', 10, 'Iniciación', 'Grupal', 90, 65.00, 'Fundamentos de fotografía'),
('Fotografía - Avanzado', 10, 'Avanzado', 'Grupal', 120, 80.00, 'Técnicas avanzadas y edición');

-- ============================================
-- EMPRENDIMIENTO (2)
-- ============================================

INSERT INTO actividades (nombre, area_id, nivel, modalidad, duracion_minutos, precio_mensual, descripcion) VALUES
('Miniempresas', 11, 'Todos los niveles', 'Grupal', 90, 65.00, 'Creación de miniempresas con certificado SECOT'),
('Emprendimiento digital', 11, 'Intermedio', 'Grupal', 90, 70.00, 'Negocios digitales y startups');

-- ============================================
-- PROFESORES (datos de la web)
-- ============================================

INSERT INTO profesores (nombre, especialidad, bio, sede_principal_id, activo) VALUES
-- Música
('Daniel Rabaneda', 'Costura y Diseño', 'Conocido por su participación en Maestros de la Costura. Especialista en patronaje y diseño de moda.', 1, 1),
('María González Pérez', 'Piano', 'Titulada superior en Piano por el Real Conservatorio Superior de Madrid. Más de 15 años de experiencia docente.', 1, 1),
('Carlos Martínez López', 'Violín', 'Violinista de la Orquesta de RTVE. Especialista en pedagogía Suzuki.', 1, 1),
('Ana Sánchez García', 'Canto', 'Soprano lírica con experiencia en ópera y música de cámara. Formación en el Conservatorio de Madrid.', 1, 1),
('Pedro Fernández Ruiz', 'Guitarra', 'Guitarrista flamenco y clásico. Ha colaborado con artistas de renombre internacional.', 1, 1),
('Laura Díaz Moreno', 'Lenguaje Musical', 'Doctora en Musicología. Especialista en educación musical temprana.', 1, 1),
('Javier López Torres', 'Batería y Percusión', 'Percusionista profesional con experiencia en jazz y música latina.', 2, 1),
('Elena Rodríguez Blanco', 'Flauta travesera', 'Primera flauta de la Orquesta Filarmónica. Pedagoga musical.', 2, 1),
('Miguel Ángel García', 'Saxofón', 'Saxofonista de jazz. Director de big band escolar.', 1, 1),
('Carmen Ruiz Vega', 'Violonchelo', 'Chelista con formación en Viena. Especialista en música de cámara.', 1, 1),

-- Danza
('Isabel Navarro', 'Danza Clásica', 'Ex-bailarina del Ballet Nacional de España. Metodología Vaganova.', 1, 1),
('Rocío Morales', 'Flamenco', 'Bailaora profesional con más de 20 años en tablaos de Madrid.', 1, 1),
('David Jiménez', 'Baile Moderno', 'Coreógrafo y bailarín de estilos urbanos. Ha trabajado en videoclips y eventos.', 2, 1),
('Patricia Vázquez', 'Danza Contemporánea', 'Formación en Martha Graham y Limón. Coreógrafa independiente.', 1, 1),

-- Robótica y Tecnología
('Alberto Fernández', 'Robótica', 'Ingeniero informático especializado en robótica educativa. Certificado LEGO Education.', 1, 1),
('Silvia Martín', 'Programación', 'Desarrolladora de software con experiencia en educación tecnológica para niños.', 2, 1),
('Raúl Gómez', 'Electrónica', 'Ingeniero electrónico. Maker y divulgador tecnológico.', 1, 1),
('Cristina López', 'Diseño 3D', 'Diseñadora industrial especializada en impresión 3D y prototipado.', 1, 1),

-- Audiovisuales
('Fernando Herrera', 'Cine y Audiovisuales', 'Director de cine con cortometrajes premiados. Profesor de narrativa visual.', 1, 1),
('Lucía Serrano', 'Edición de Vídeo', 'Editora profesional de cine y televisión. Experta en DaVinci Resolve.', 2, 1),
('Pablo Ruiz', 'Animación', 'Animador 2D y 3D. Ha trabajado para estudios de animación internacionales.', 1, 1),

-- Artes Plásticas
('Rosa Mendoza', 'Pintura', 'Artista plástica con exposiciones en galerías de Madrid y Barcelona.', 1, 1),
('Andrés Molina', 'Dibujo e Ilustración', 'Ilustrador profesional. Colaborador de editoriales infantiles.', 2, 1),
('Marta Sánchez', 'Escultura', 'Escultora con formación en Bellas Artes. Especialista en modelado.', 1, 1),

-- Teatro
('Alejandro Ruiz', 'Teatro', 'Actor profesional con experiencia en teatro, cine y televisión.', 1, 1),
('Sara Gómez', 'Teatro Musical', 'Actriz y cantante. Ha participado en musicales de Madrid.', 1, 1),

-- Otros
('Francisco Lozano', 'Fotografía', 'Fotógrafo profesional especializado en retrato y fotografía artística.', 2, 1),
('Teresa Blanco', 'Oratoria', 'Coach de comunicación. Consultora de empresas y formadora.', 1, 1),
('Guillermo Sanz', 'Magia', 'Mago profesional. Miembro de la Sociedad Española de Ilusionismo.', 1, 1),
('Beatriz Torres', 'Emprendimiento', 'Emprendedora y mentora de startups. Colaboradora de SECOT.', 1, 1);

-- ============================================
-- CONFIGURACIÓN DE PAGO POR DEFECTO
-- (Los 7 tipos de pago)
-- ============================================

-- Tipo 1: Por horas
INSERT INTO proveedores_config (profesor_id, tipo_pago, tarifa_hora) VALUES
(2, 'hora', 25.00),   -- María González (Piano)
(3, 'hora', 25.00),   -- Carlos Martínez (Violín)
(4, 'hora', 25.00);   -- Ana Sánchez (Canto)

-- Tipo 2: Por número de alumnos
INSERT INTO proveedores_config (profesor_id, tipo_pago, tarifa_alumno) VALUES
(11, 'alumno', 8.00), -- Isabel Navarro (Danza Clásica)
(12, 'alumno', 8.50); -- Rocío Morales (Flamenco)

-- Tipo 3: Cantidad fija mensual
INSERT INTO proveedores_config (profesor_id, tipo_pago, cantidad_fija) VALUES
(15, 'fijo', 800.00), -- Alberto Fernández (Robótica)
(16, 'fijo', 750.00); -- Silvia Martín (Programación)

-- Tipo 4: Mixto fijo + alumnos
INSERT INTO proveedores_config (profesor_id, tipo_pago, cantidad_fija, tarifa_alumno) VALUES
(13, 'mixto_alumno', 300.00, 5.00), -- David Jiménez (Baile Moderno)
(14, 'mixto_alumno', 300.00, 5.00); -- Patricia Vázquez (Danza Contemporánea)

-- Tipo 5: Mixto fijo + porcentaje de ingresos
INSERT INTO proveedores_config (profesor_id, tipo_pago, cantidad_fija, porcentaje_ingresos) VALUES
(19, 'mixto_porcentaje', 200.00, 15.00), -- Fernando Herrera (Cine)
(1, 'mixto_porcentaje', 400.00, 20.00);  -- Daniel Rabaneda (Costura)

-- Tipo 6: Mixto hora + alumno
INSERT INTO proveedores_config (profesor_id, tipo_pago, tarifa_hora, tarifa_alumno) VALUES
(25, 'mixto_hora_alumno', 20.00, 3.00), -- Alejandro Ruiz (Teatro)
(26, 'mixto_hora_alumno', 20.00, 3.00); -- Sara Gómez (Teatro Musical)

-- Resto de profesores con tarifa por hora estándar
INSERT INTO proveedores_config (profesor_id, tipo_pago, tarifa_hora) VALUES
(5, 'hora', 25.00),   -- Pedro Fernández (Guitarra)
(6, 'hora', 22.00),   -- Laura Díaz (Lenguaje Musical)
(7, 'hora', 25.00),   -- Javier López (Batería)
(8, 'hora', 25.00),   -- Elena Rodríguez (Flauta)
(9, 'hora', 25.00),   -- Miguel Ángel (Saxofón)
(10, 'hora', 25.00),  -- Carmen Ruiz (Violonchelo)
(17, 'hora', 23.00),  -- Raúl Gómez (Electrónica)
(18, 'hora', 23.00),  -- Cristina López (Diseño 3D)
(20, 'hora', 24.00),  -- Lucía Serrano (Edición)
(21, 'hora', 24.00),  -- Pablo Ruiz (Animación)
(22, 'hora', 22.00),  -- Rosa Mendoza (Pintura)
(23, 'hora', 22.00),  -- Andrés Molina (Ilustración)
(24, 'hora', 22.00),  -- Marta Sánchez (Escultura)
(27, 'hora', 25.00),  -- Francisco Lozano (Fotografía)
(28, 'hora', 30.00),  -- Teresa Blanco (Oratoria)
(29, 'hora', 25.00),  -- Guillermo Sanz (Magia)
(30, 'hora', 28.00);  -- Beatriz Torres (Emprendimiento)
