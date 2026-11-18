import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService, Course, Enrollment, Stats } from '../core/api.service';
import { TEAM } from '../core/team';
import { thumbnailUrl } from '../core/youtube';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  template: `
    <section class="hero">
      <p class="eyebrow">LearnSphere · Online Learning Platform · Case Study 8</p>
      <h1>Learn. Build. Ship.</h1>
      <p class="lead">
        Video-based modules on Docker, CI/CD, Angular, Django, MySQL, Redis and AWS — served by a containerised
        Angular + Django REST + Redis + MySQL platform that GitHub Actions builds and deploys to AWS EC2.
      </p>
      <p class="small">Built by <b>{{ teamNames }}</b></p>
      <div class="actions">
        <a routerLink="/courses" class="btn">Start learning</a>
        <a routerLink="/team" class="btn btn-ghost">Meet the team</a>
        <a routerLink="/status" class="btn btn-ghost">View system status</a>
      </div>
    </section>

    <section class="tiles">
      @for (tile of tiles; track tile.key) {
        <div class="tile">
          <span class="tile-value">{{ stats()?.[tile.key] ?? '—' }}</span>
          <span class="tile-label">{{ tile.label }}</span>
        </div>
      }
    </section>
    @if (cacheState()) {
      <p class="muted small">Dashboard stats served from Redis cache: <span class="badge">{{ cacheState() }}</span></p>
    }

    <section class="section">
      <div class="section-head">
        <h2>Featured modules</h2>
        <a routerLink="/courses" class="link">See all →</a>
      </div>
      <div class="grid">
        @for (c of featured(); track c.id) {
          <a class="card card-media" [routerLink]="['/courses', c.id]">
            <div class="thumb">
              <img [src]="thumb(c.cover_video_id)" [alt]="c.title" loading="lazy" />
              <span class="play">▶</span>
              <span class="module-no">Module {{ c.module_no }}</span>
            </div>
            <div class="card-body">
              <span class="tag">{{ c.category }}</span>
              <h3>{{ c.title }}</h3>
              <p class="small">Curated by <b>{{ c.instructor }}</b></p>
              <div class="meta">
                <span>{{ c.level }}</span><span>{{ c.lesson_count }} videos</span><span>★ {{ c.rating }}</span>
              </div>
            </div>
          </a>
        }
      </div>
    </section>

    <section class="section">
      <h2>Recent enrollments</h2>
      @if (enrollments().length) {
        <table class="table">
          <thead><tr><th>Student</th><th>Module</th><th>Enrolled</th></tr></thead>
          <tbody>
            @for (e of enrollments(); track e.id) {
              <tr><td>{{ e.student_name }}</td><td>{{ e.course_title }}</td><td>{{ e.enrolled_at.slice(0, 16).replace('T', ' ') }}</td></tr>
            }
          </tbody>
        </table>
      } @else {
        <p class="muted">No enrollments yet. Open a module and enrol to see it here.</p>
      }
    </section>

    <section class="section">
      <h2>Technology stack</h2>
      <div class="stack">
        @for (s of stack; track s.name) {
          <div class="stack-item"><b>{{ s.name }}</b><span class="muted">{{ s.role }}</span></div>
        }
      </div>
    </section>
  `,
})
export class Dashboard {
  private api = inject(ApiService);

  stats = signal<Stats | null>(null);
  cacheState = signal('');
  featured = signal<Course[]>([]);
  enrollments = signal<Enrollment[]>([]);
  teamNames = TEAM.map((m) => m.name).join(', ');
  thumb = thumbnailUrl;

  tiles: { key: keyof Stats; label: string }[] = [
    { key: 'courses', label: 'Modules' },
    { key: 'lessons', label: 'Video lessons' },
    { key: 'enrollments', label: 'Enrollments' },
    { key: 'categories', label: 'Categories' },
  ];

  stack = [
    { name: 'Angular', role: 'Frontend SPA served by Nginx' },
    { name: 'Django REST', role: 'API on Gunicorn' },
    { name: 'Redis', role: 'Response caching' },
    { name: 'MySQL 8.4', role: 'Persistent data (named volume)' },
    { name: 'Docker Compose', role: 'Multi-container orchestration' },
    { name: 'GitHub Actions', role: 'CI/CD to GHCR and AWS EC2' },
  ];

  constructor() {
    this.api.stats().subscribe((r) => {
      this.stats.set(r.data);
      this.cacheState.set(r.cache);
    });
    this.api.courses().subscribe((r) => this.featured.set(r.data.slice(0, 3)));
    this.api.enrollments().subscribe((r) => this.enrollments.set(r.slice(0, 5)));
  }
}
