import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { REPO_URL, TEAM } from './core/team';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="topbar">
      <div class="wrap topbar-inner">
        <a routerLink="/" class="brand">
          <span class="brand-mark">L</span>
          <span>Learn<b>Sphere</b></span>
        </a>
        <nav>
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{ exact: true }">Dashboard</a>
          <a routerLink="/courses" routerLinkActive="active">Modules</a>
          <a routerLink="/team" routerLinkActive="active">Team</a>
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
        <span><b>LearnSphere</b> · Team: {{ teamNames }}</span>
        <span>Angular · Django REST · Redis · MySQL · Docker · GitHub Actions · AWS EC2</span>
        <a [href]="repoUrl" target="_blank" rel="noopener">github.com/Swamini9403/swamini-lms</a>
      </div>
    </footer>
  `,
})
export class App {
  teamNames = TEAM.map((m) => m.name).join(' · ');
  repoUrl = REPO_URL;
}
