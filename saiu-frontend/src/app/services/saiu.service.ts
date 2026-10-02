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

  // 1. Obtener perfil (¡Mira qué limpio quedó sin el código del token!)
  getMyProfile(): Observable<UserProfile> {
    return this.http.get<UserProfile>(`${this.apiUrl}/auth/me`);
  }

  // 2. NUEVO: Obtener el avance académico del estudiante
  getMiAvance(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/estudiantes/mi-avance`);
  }

  // 3. Login
  login(credentials: { username: string; password: string }): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', credentials.username);
    body.set('password', credentials.password);

    const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded');

    return this.http.post(`${this.apiUrl}/auth/login`, body.toString(), { headers });
  }
}