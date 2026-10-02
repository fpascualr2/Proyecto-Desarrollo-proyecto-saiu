import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router'; // <-- 1. Importar Router
import { SaiuService } from '../../services/saiu.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private saiuService = inject(SaiuService);
  private router = inject(Router); // <-- 2. Inyectar Router

  loginForm: FormGroup = this.fb.group({
    username: ['', [Validators.required]],
    password: ['', [Validators.required]]
  });

  errorMessage: string = '';
  isLoading: boolean = false;

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    const { username, password } = this.loginForm.value;

    this.saiuService.login({ username, password }).subscribe({
      next: (response) => {
       this.isLoading = false;
        localStorage.setItem('access_token', response.access_token);
        console.log('¡Inicio de sesión exitoso!', response);
        
        // Damos un micro-respiro para asegurar que el storage sincronice antes de entrar al dashboard
        setTimeout(() => {
          this.router.navigate(['/dashboard']);
        }, 50);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Credenciales incorrectas o error de conexión con el servidor.';
        console.error(err);
      }
    });
  }
}