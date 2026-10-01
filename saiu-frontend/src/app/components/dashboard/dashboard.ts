import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
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

  userProfile: UserProfile | null = null;
  isLoading: boolean = true;
  errorMessage: string = '';

  ngOnInit() {
    this.loadUserProfile();
  }

  loadUserProfile() {
    this.saiuService.getMyProfile().subscribe({
      next: (data) => {
        this.userProfile = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'No se pudo cargar la información del perfil. Inicia sesión nuevamente.';
        console.error(err);
      }
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }
}