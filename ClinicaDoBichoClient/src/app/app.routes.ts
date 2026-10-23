import { Routes } from '@angular/router';
import { AuthGuard } from "./auth/auth.guard";

export const routes: Routes = [
 {
    path: 'home',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./login/login.page').then( m => m.LoginPage)
  },
  {
    path: 'consultas',
    loadComponent: () => import('./consultas/consultas.page').then( m => m.ConsultasPage),
                         canActivate : [AuthGuard]
  },
  {
    path: 'agendar-consulta',
    loadComponent: () => import('./agendar-consulta/agendar-consulta.page').then( m => m.AgendarConsultaPage),
                         canActivate : [AuthGuard]
  },
];
