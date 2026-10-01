--. PROCEDIMIENTOS ALMACENADOS (STORED PROCEDURES)

DELIMITER //

-- SP 1: Obtener avance detallado del estudiante por carnet
CREATE PROCEDURE sp_obtener_avance_estudiante(IN p_carnet VARCHAR(20))
BEGIN
    SELECT 
        e.carnet,
        CONCAT(u.nombre, ' ', u.apellido) AS estudiante,
        c.nombre AS carrera,
        c.creditos_totales,
        COALESCE(SUM(CASE WHEN h.estado = 'APROBADO' THEN cu.creditos ELSE 0 END), 0) AS creditos_aprobados,
        ROUND(
            (COALESCE(SUM(CASE WHEN h.estado = 'APROBADO' THEN cu.creditos ELSE 0 END), 0) / c.creditos_totales) * 100, 
            2
        ) AS porcentaje_avance
    FROM estudiantes e
    JOIN usuarios u ON e.usuario_id = u.id
    JOIN carreras c ON e.carrera_id = c.id
    LEFT JOIN historial_academico h ON e.id = h.estudiante_id
    LEFT JOIN cursos cu ON h.curso_id = cu.id
    WHERE e.carnet = p_carnet
    GROUP BY e.id, e.carnet, u.nombre, u.apellido, c.nombre, c.creditos_totales;
END//

-- SP 2: Validar si un estudiante cumple con los prerrequisitos para un curso
CREATE PROCEDURE sp_validar_prerrequisitos(
    IN p_estudiante_id INT, 
    IN p_curso_id INT, 
    OUT p_aprobado BOOLEAN
)
BEGIN
    DECLARE v_faltantes INT;
    
    -- Cuenta cuántos requisitos obligatorios el estudiante NO tiene aprobados
    SELECT COUNT(*) INTO v_faltantes
    FROM curso_requisitos cr
    WHERE cr.curso_id = p_curso_id
      AND cr.requisito_curso_id NOT IN (
          SELECT h.curso_id 
          FROM historial_academico h 
          WHERE h.estudiante_id = p_estudiante_id 
            AND h.estado = 'APROBADO'
      );
      
    -- Si no falta ninguno (faltantes = 0), puede asignarse
    IF v_faltantes = 0 THEN
        SET p_aprobado = TRUE;
    ELSE
        SET p_aprobado = FALSE;
    END IF;
END//

DELIMITER ;