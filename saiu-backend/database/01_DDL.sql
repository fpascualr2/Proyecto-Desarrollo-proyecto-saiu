DROP DATABASE saiu_db;

CREATE DATABASE IF NOT EXISTS saiu_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE saiu_db;

-- 1. CATÁLOGOS Y USUARIOS

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) DEFAULT 'estudiante',
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE carreras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_carrera VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    creditos_totales INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_curso VARCHAR(15) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    creditos INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE ciclos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL COMMENT 'Ej. 2026-1',
    nombre VARCHAR(100) NOT NULL COMMENT 'Ej. Primer Semestre 2026',
    activo BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;


-- 2. ESTRUCTURA ACADÉMICA Y ESTUDIANTES

CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    carnet VARCHAR(20) UNIQUE NOT NULL COMMENT 'Formato UMG, ej. 0900-26-12345',
    carrera_id INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id)
) ENGINE=InnoDB;

CREATE TABLE pensum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carrera_id INT NOT NULL,
    curso_id INT NOT NULL,
    semestre INT NOT NULL,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Prerrequisitos de cursos
CREATE TABLE curso_requisitos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL COMMENT 'El curso que exige el requisito',
    requisito_curso_id INT NOT NULL COMMENT 'El curso que debe estar aprobado previamente',
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (requisito_curso_id) REFERENCES cursos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE historial_academico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    curso_id INT NOT NULL,
    ciclo_id INT NOT NULL,
    nota DECIMAL(5,2),
    estado ENUM('CURSANDO', 'APROBADO', 'REPROBADO') DEFAULT 'CURSANDO',
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id),
    FOREIGN KEY (ciclo_id) REFERENCES ciclos(id)
) ENGINE=InnoDB;


-- 3. MÓDULO DE GRADUACIÓN

CREATE TABLE opciones_graduacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL COMMENT 'Ej. Tesis, Examen Privado, Cursos de Maestría',
    porcentaje_minimo_avance DECIMAL(5,2) NOT NULL COMMENT 'Ej. 75.00 o 100.00'
) ENGINE=InnoDB;

-- Trámite de graduación por estudiante
CREATE TABLE estudiante_opciones_graduacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    opcion_id INT NOT NULL,
    estado_tramite ENUM('PENDIENTE', 'EN_REVISION', 'APROBADO', 'FINALIZADO') DEFAULT 'PENDIENTE',
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
    FOREIGN KEY (opcion_id) REFERENCES opciones_graduacion(id)
) ENGINE=InnoDB;


-- 4. TABLA Y TRIGGERS DE AUDITORÍA

CREATE TABLE auditoria_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    accion VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    usuario_db VARCHAR(100),
    detalles TEXT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
