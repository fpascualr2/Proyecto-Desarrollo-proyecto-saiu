import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  
  // Si estamos en el navegador y hay un token, dejamos pasar
  if (typeof localStorage !== 'undefined' && localStorage.getItem('access_token')) {
    return true;
  }
  
  // Si no hay token, lo mandamos directo al login
  router.navigate(['/login']);
  return false;
};