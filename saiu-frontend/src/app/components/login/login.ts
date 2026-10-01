import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
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
        // Almacenamos el token JWT recibido del backend de FastAPI
        localStorage.setItem('access_token', response.access_token);
        console.log('¡Inicio de sesión exitoso!', response);
        // Aquí puedes redirigir posteriormente al dashboard o perfil del estudiante
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Credenciales incorrectas o error de conexión con el servidor.';
        console.error(err);
      }
    });
  }
}