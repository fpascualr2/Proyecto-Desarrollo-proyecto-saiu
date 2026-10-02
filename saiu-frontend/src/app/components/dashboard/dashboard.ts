import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { SaiuService } from '../../services/saiu.service';
import { UserProfile } from '../../models/user.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  private saiuService = inject(SaiuService);
  private router = inject(Router);
  private cdr = inject(ChangeDetectorRef); 

  userProfile: UserProfile | null = null;
  avanceAcademico: any = null;
  cursosDocente: any[] = [];
  historialEstudiante: any[] = [];
  
  isLoadingProfile: boolean = true;
  isLoadingAvance: boolean = true;
  isLoadingCursosDocente: boolean = false;
  errorMessage: string = '';

  // --- Control de Pestañas para el Administrador ---
  adminView: 'overview' | 'usuarios' | 'cursos' | 'historial' = 'overview';

  // --- Propiedades para el módulo de Creación de Usuarios (Admin) ---
  nuevoUsuario = {
    nombre: '',
    apellido: '',
    username: '',
    email: '',
    password: '',
    rol: 'DOCENTE'
  };
  isCreatingUser: boolean = false;
  mensajeAdmin: string = '';
  errorAdmin: string = '';

  ngOnInit() {
    this.loadUserProfile();
  }

  setAdminView(view: 'overview' | 'usuarios' | 'cursos' | 'historial') {
    this.adminView = view;
    this.errorAdmin = '';
    this.mensajeAdmin = '';
    this.cdr.detectChanges();
  }

  loadUserProfile() {
    this.isLoadingProfile = true;

    this.saiuService.getMyProfile().pipe(
      finalize(() => {
        this.isLoadingProfile = false;
        this.cdr.detectChanges(); 
      })
    ).subscribe({
      next: (data: any) => {
        if (data && data.rol) {
          data.rol = data.rol.toUpperCase();
        }
        this.userProfile = data;

        if (this.userProfile?.rol === 'ADMINISTRADOR') {
          this.isLoadingAvance = false;
          this.cdr.detectChanges();
        } 
        else if (this.userProfile?.rol === 'DOCENTE') {
          this.isLoadingAvance = false;
          this.loadCursosDocente();
        } 
        else if (this.userProfile?.rol === 'ESTUDIANTE') {
          this.loadAvanceAcademico();
          this.loadHistorialEstudiante();
        } 
        else {
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
        this.cdr.detectChanges();
      })
    ).subscribe({
      next: (data: any) => {
        this.avanceAcademico = data;
        this.cdr.detectChanges(); 
      },
      error: (err: any) => {
        console.error('Error al cargar avance académico:', err);
      }
    });
  }

  loadHistorialEstudiante() {
    this.saiuService.getMiHistorial().subscribe({
      next: (data: any) => {
        this.historialEstudiante = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error al cargar historial del estudiante:', err);
      }
    });
  }

  loadCursosDocente() {
    this.isLoadingCursosDocente = true;
    this.saiuService.getMisCursosDocente().pipe(
      finalize(() => {
        this.isLoadingCursosDocente = false;
        this.cdr.detectChanges();
      })
    ).subscribe({
      next: (data: any) => {
        this.cursosDocente = data;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        console.error('Error al cargar cursos del docente:', err);
      }
    });
  }

  // --- Método para crear usuario desde el panel de Administrador ---
  crearUsuario() {
    // Cambiado 'correo' por 'email' en la validación
    if (!this.nuevoUsuario.nombre || !this.nuevoUsuario.username || !this.nuevoUsuario.email || !this.nuevoUsuario.password) {
      this.errorAdmin = 'Por favor completa los campos obligatorios (incluyendo el username).';
      return;
    }

    this.isCreatingUser = true;
    this.errorAdmin = '';
    this.mensajeAdmin = '';

    this.saiuService.crearUsuario(this.nuevoUsuario).pipe(
      finalize(() => {
        this.isCreatingUser = false;
        this.cdr.detectChanges();
      })
    ).subscribe({
      next: (res: any) => {
        this.mensajeAdmin = `¡Usuario ${this.nuevoUsuario.rol.toLowerCase()} (${this.nuevoUsuario.username}) creado con éxito!`;
        // Limpiar el formulario usando 'email'
        this.nuevoUsuario = { nombre: '', apellido: '', username: '', email: '', password: '', rol: 'DOCENTE' };
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error al crear usuario:', err);
        this.errorAdmin = err.error?.detail || 'No se pudo crear el usuario. Revisa los datos.';
        this.cdr.detectChanges();
      }
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }
}