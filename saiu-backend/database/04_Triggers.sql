DELIMITER //

CREATE TRIGGER trg_historial_after_insert
AFTER INSERT ON historial_academico
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_log (tabla_afectada, accion, usuario_db, detalles)
    VALUES (
        'historial_academico',
        'INSERT',
        USER(),
        CONCAT('Estudiante ID: ', NEW.estudiante_id, ', Curso ID: ', NEW.curso_id, ', Estado: ', NEW.estado)
    );
END//

CREATE TRIGGER trg_historial_after_update
AFTER UPDATE ON historial_academico
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_log (tabla_afectada, accion, usuario_db, detalles)
    VALUES (
        'historial_academico',
        'UPDATE',
        USER(),
        CONCAT('Actualización ID: ', OLD.id, '. Estado: ', OLD.estado, ' -> ', NEW.estado, ', Nota: ', OLD.nota, ' -> ', NEW.nota)
    );
END//

DELIMITER ;
