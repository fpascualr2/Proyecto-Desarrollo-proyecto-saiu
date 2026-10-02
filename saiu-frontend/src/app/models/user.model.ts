export interface UserProfile {
  id: number;
  nombre: string;
  apellido: string;
  username: string;
  email: string;
  rol: string;
  carnet?: string;
  carrera?: string;
  semestre?: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  nombre: string;
  apellido: string;
  rol: 'ADMINISTRADOR' | 'DOCENTE' | 'ESTUDIANTE';
  activo: boolean;
}