import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="topbar">
      <div class="wrap topbar-inner">
        <a routerLink="/" class="brand">
          <span class="brand-mark">S</span>
          <span>Swamini <b>LMS</b></span>
        </a>
        <nav>
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Dashboard</a>
          <a routerLink="/courses" routerLinkActive="active">Courses</a>
          <a routerLink="/status" routerLinkActive="active">System Status</a>
          <a routerLink="/about" routerLinkActive="active">About</a>
        </nav>
      </div>
    </header>

    <main class="wrap">
      <router-outlet />
    </main>

    <footer class="footer">
      <div class="wrap footer-inner">
        <span>Swamini · PRN 202402040005</span>
        <span>Angular · Django REST · Redis · MySQL · Docker · GitHub Actions</span>
        <a href="https://github.com/swamini9403/swamini-lms" target="_blank" rel="noopener">github.com/swamini9403/swamini-lms</a>
      </div>
    </footer>
  `,
})
export class App {}
