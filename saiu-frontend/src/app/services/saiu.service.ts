import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserProfile } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class SaiuService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000'; // URL directa de tu backend en FastAPI

  // Método para obtener el perfil del usuario autenticado
getMyProfile(): Observable<UserProfile> {
    let token = '';
    
    // Verificamos si estamos en el navegador antes de usar localStorage
    if (typeof localStorage !== 'undefined') {
      token = localStorage.getItem('access_token') || '';
    }

    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<UserProfile>(`${this.apiUrl}/auth/me`, { headers });
  }

  // Método para iniciar sesión
  login(credentials: { username: string; password: string }): Observable<any> {
    // FastAPI suele usar OAuth2PasswordRequestForm que requiere x-www-form-urlencoded
    const body = new URLSearchParams();
    body.set('username', credentials.username);
    body.set('password', credentials.password);

    const headers = new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded');

    // CORRECCIÓN: Se cambió /token por /auth/login
    return this.http.post(`${this.apiUrl}/auth/login`, body.toString(), { headers });
  }
}