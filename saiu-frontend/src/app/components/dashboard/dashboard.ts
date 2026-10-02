import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { SaiuService } from '../../services/saiu.service';
import { UserProfile } from '../../models/user.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  private saiuService = inject(SaiuService);
  private router = inject(Router);
  // Inyectamos el ChangeDetectorRef para forzar el repintado del HTML
  private cdr = inject(ChangeDetectorRef); 

  userProfile: UserProfile | null = null;
  avanceAcademico: any = null;
  
  isLoadingProfile: boolean = true;
  isLoadingAvance: boolean = true;
  errorMessage: string = '';

  ngOnInit() {
    this.loadUserProfile();
  }

  loadUserProfile() {
    this.isLoadingProfile = true;

    this.saiuService.getMyProfile().pipe(
      finalize(() => {
        this.isLoadingProfile = false;
        // Obligamos a Angular a actualizar la pantalla y quitar el "Cargando..."
        this.cdr.detectChanges(); 
      })
    ).subscribe({
      next: (data: any) => {
        console.log('¡Datos de perfil recibidos con éxito del backend!', data);
        
        // Normalizamos el rol a mayúsculas directamente en el objeto 
        // para que tu HTML (=== 'ADMINISTRADOR') no falle nunca.
        if (data && data.rol) {
          data.rol = data.rol.toUpperCase();
        }

        this.userProfile = data;

        if (this.userProfile?.rol !== 'ADMINISTRADOR') {
          this.loadAvanceAcademico();
        } else {
          this.isLoadingAvance = false;
          this.cdr.detectChanges();
        }
      },
      error: (err) => {
        console.error('Error al obtener perfil:', err);
        this.errorMessage = 'No se pudo cargar la información del usuario.';
        this.isLoadingAvance = false;
        this.cdr.detectChanges();
      }
    });
  }

  loadAvanceAcademico() {
    this.isLoadingAvance = true;

    this.saiuService.getMiAvance().pipe(
      finalize(() => {
        this.isLoadingAvance = false;
        this.cdr.detectChanges(); // Repintar tras finalizar
      })
    ).subscribe({
      next: (data: any) => {
        console.log('Avance académico recibido:', data);
        this.avanceAcademico = data;
        // Forzamos a que aparezcan las tarjetas del estudiante
        this.cdr.detectChanges(); 
      },
      error: (err: any) => {
        console.error('Error al cargar avance académico:', err);
      }
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }
}