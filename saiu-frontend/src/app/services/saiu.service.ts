import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserProfile } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class SaiuService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000'; 

  // --- AUTENTICACIÓN Y PERFIL ---
  login(credentials: { username: string; password: string }): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', credentials.username);
    body.set('password', credentials.password);

    const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded');
    return this.http.post(`${this.apiUrl}/auth/login`, body.toString(), { headers });
  }

  getMyProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/auth/me`);
  }

  // --- MÓDULO ADMINISTRADOR (Académico y Usuarios) ---
  listarUsuarios(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/usuarios/`);
  }

 crearUsuario(userData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/auth/registro`, userData);
  }
  
  crearCarrera(carreraData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/academico/carreras`, carreraData);
  }

  listarCarreras(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/academico/carreras`);
  }

  crearCurso(cursoData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/academico/cursos`, cursoData);
  }

  listarCursos(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/academico/cursos`);
  }

  crearCiclo(cicloData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/academico/ciclos`, cicloData);
  }

  listarCiclos(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/academico/ciclos`);
  }

  agregarAlPensum(pensumData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/academico/pensum`, pensumData);
  }

  // --- MÓDULO DOCENTE ---
  getMisCursosDocente(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/docente/mis-cursos`);
  }

  calificarEstudiante(data: {
    estudiante_id: number;
    curso_id: number;
    ciclo_id: number;
    nota: number;
    estado: string;
  }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/docente/calificar`, data);
  }

  // --- MÓDULO ESTUDIANTE ---
  getMiAvance(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/estudiantes/mi-avance`);
  }

  getMiHistorial(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/estudiantes/mi-historial`);
  }
}