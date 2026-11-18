import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/dashboard').then((m) => m.Dashboard), title: 'Dashboard · Swamini LMS' },
  { path: 'courses', loadComponent: () => import('./pages/courses').then((m) => m.Courses), title: 'Courses · Swamini LMS' },
  { path: 'courses/:id', loadComponent: () => import('./pages/course-detail').then((m) => m.CourseDetail), title: 'Course · Swamini LMS' },
  { path: 'status', loadComponent: () => import('./pages/status').then((m) => m.Status), title: 'System Status · Swamini LMS' },
  { path: 'about', loadComponent: () => import('./pages/about').then((m) => m.About), title: 'About · Swamini LMS' },
  { path: '**', redirectTo: '' },
];
