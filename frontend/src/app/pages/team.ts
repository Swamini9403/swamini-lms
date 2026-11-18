import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ApiService, Course } from '../core/api.service';
import { TEAM } from '../core/team';

@Component({
  selector: 'app-team',
  imports: [RouterLink],
  template: `
    <section class="page-head">
      <h1>Our team</h1>
      <p class="muted">LearnSphere was designed, built and deployed by a team of three for Case Study 8 — CI/CD + Docker.</p>
    </section>

    <div class="team">
      @for (m of team; track m.name) {
        <div class="member">
          <div class="avatar">{{ m.initials }}</div>
          <h2>{{ m.name }}</h2>
          @if (m.prn) { <p class="small muted">PRN {{ m.prn }}</p> }
          @if (m.github) {
            <p class="small"><a [href]="'https://github.com/' + m.github" target="_blank" rel="noopener">github.com/{{ m.github }}</a></p>
          }
          <h3>Modules curated</h3>
          <ul class="curated">
            @for (c of modulesBy(m.name); track c.id) {
              <li><a [routerLink]="['/courses', c.id]">Module {{ c.module_no }} · {{ c.title }}</a> <span class="muted small">({{ c.lesson_count }} videos)</span></li>
            }
          </ul>
        </div>
      }
    </div>
  `,
})
export class Team {
  private api = inject(ApiService);
  team = TEAM;
  courses = signal<Course[]>([]);

  constructor() {
    this.api.courses().subscribe((r) => this.courses.set(r.data));
  }

  modulesBy(name: string) {
    return this.courses().filter((c) => c.instructor === name);
  }
}
