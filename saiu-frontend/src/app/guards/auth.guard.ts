import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  // Verificamos si estamos corriendo en el navegador (donde sí existe localStorage)
  if (isPlatformBrowser(platformId)) {
    const token = localStorage.getItem('access_token');
    if (token) {
      return true;
    }
  } else {
    // Si está corriendo en SSR (servidor), permitimos pasar temporalmente o validamos de otra forma
    return true;
  }

  // Si no hay token en el navegador, redirige al login
  router.navigate(['/login']);
  return false;
};