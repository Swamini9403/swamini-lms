import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/dashboard').then((m) => m.Dashboard), title: 'Dashboard · LearnSphere' },
  { path: 'courses', loadComponent: () => import('./pages/courses').then((m) => m.Courses), title: 'Modules · LearnSphere' },
  { path: 'courses/:id', loadComponent: () => import('./pages/course-detail').then((m) => m.CourseDetail), title: 'Module · LearnSphere' },
  { path: 'team', loadComponent: () => import('./pages/team').then((m) => m.Team), title: 'Team · LearnSphere' },
  { path: 'status', loadComponent: () => import('./pages/status').then((m) => m.Status), title: 'System Status · LearnSphere' },
  { path: 'about', loadComponent: () => import('./pages/about').then((m) => m.About), title: 'About · LearnSphere' },
  { path: '**', redirectTo: '' },
];
