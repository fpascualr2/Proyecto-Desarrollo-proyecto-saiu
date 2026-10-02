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