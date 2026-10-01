

--. VISTAS ANALÍTICAS Y DE REPORTES

-- Vista de Auditoría
CREATE OR REPLACE VIEW vw_reporte_auditoria AS
SELECT 
    id,
    tabla_afectada AS Tabla,
    accion AS Accion,
    usuario_db AS UsuarioDB,
    detalles AS Detalles,
    fecha_hora AS FechaHora
FROM auditoria_log
ORDER BY fecha_hora DESC;

-- Vista de Avance Académico Global
CREATE OR REPLACE VIEW vw_resumen_avance_estudiantes AS
SELECT 
    e.carnet,
    CONCAT(u.nombre, ' ', u.apellido) AS nombre_estudiante,
    c.nombre AS carrera,
    c.creditos_totales AS creditos_plan,
    COALESCE(SUM(CASE WHEN h.estado = 'APROBADO' THEN cu.creditos ELSE 0 END), 0) AS creditos_acumulados,
    ROUND(
        (COALESCE(SUM(CASE WHEN h.estado = 'APROBADO' THEN cu.creditos ELSE 0 END), 0) / c.creditos_totales) * 100, 
        2
    ) AS porcentaje_avance
FROM estudiantes e
JOIN usuarios u ON e.usuario_id = u.id
JOIN carreras c ON e.carrera_id = c.id
LEFT JOIN historial_academico h ON e.id = h.estudiante_id
LEFT JOIN cursos cu ON h.curso_id = cu.id
GROUP BY e.id, e.carnet, u.nombre, u.apellido, c.nombre, c.creditos_totales;

-- Vista de Estado de Trámites de Graduación
CREATE OR REPLACE VIEW vw_estado_tramites AS
SELECT 
    e.carnet,
    CONCAT(u.nombre, ' ', u.apellido) AS estudiante,
    og.nombre AS opcion_graduacion,
    eog.estado_tramite,
    eog.fecha_solicitud,
    eog.observaciones
FROM estudiante_opciones_graduacion eog
JOIN estudiantes e ON eog.estudiante_id = e.id
JOIN usuarios u ON e.usuario_id = u.id
JOIN opciones_graduacion og ON eog.opcion_id = og.id;

