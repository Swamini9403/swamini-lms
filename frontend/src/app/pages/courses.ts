import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService, Course } from '../core/api.service';
import { thumbnailUrl } from '../core/youtube';

@Component({
  selector: 'app-courses',
  imports: [RouterLink, FormsModule],
  template: `
    <section class="page-head">
      <h1>Learning modules</h1>
      <p class="muted">
        {{ courses().length }} modules of curated video lessons. Every request goes Angular → Nginx → Django REST → Redis cache → MySQL.
      </p>
    </section>

    <div class="toolbar">
      <input class="input" placeholder="Search modules or curators…" [(ngModel)]="search" (ngModelChange)="load()" />
      <div class="chips">
        <button class="chip" [class.on]="category === ''" (click)="pick('')">All</button>
        @for (c of categories(); track c) {
          <button class="chip" [class.on]="category === c" (click)="pick(c)">{{ c }}</button>
        }
      </div>
    </div>

    @if (cache()) {
      <p class="small muted">
        Redis cache: <span class="badge" [class.badge-solid]="cache() === 'HIT'">{{ cache() }}</span>
        · API time {{ elapsed() }} ms · {{ courses().length }} module(s)
      </p>
    }

    <div class="grid">
      @for (c of courses(); track c.id) {
        <a class="card card-media" [routerLink]="['/courses', c.id]">
          <div class="thumb">
            <img [src]="thumb(c.cover_video_id)" [alt]="c.title" loading="lazy" />
            <span class="play">▶</span>
            <span class="module-no">Module {{ c.module_no }}</span>
          </div>
          <div class="card-body">
            <span class="tag">{{ c.category }}</span>
            <h3>{{ c.title }}</h3>
            <p class="muted">{{ c.description }}</p>
            <p class="small">Curated by <b>{{ c.instructor }}</b></p>
            <div class="meta">
              <span>{{ c.level }}</span><span>{{ c.lesson_count }} video lessons</span><span>{{ c.duration_hours }} h</span>
              <span>★ {{ c.rating }}</span><span>{{ c.enrollment_count }} enrolled</span>
            </div>
          </div>
        </a>
      } @empty {
        <p class="muted">No modules match your search.</p>
      }
    </div>
  `,
})
export class Courses {
  private api = inject(ApiService);

  search = '';
  category = '';
  courses = signal<Course[]>([]);
  categories = signal<string[]>([]);
  cache = signal('');
  elapsed = signal(0);
  thumb = thumbnailUrl;

  constructor() {
    this.api.categories().subscribe((r) => this.categories.set(r.data));
    this.load();
  }

  pick(category: string) {
    this.category = category;
    this.load();
  }

  load() {
    this.api.courses(this.search, this.category).subscribe((r) => {
      this.courses.set(r.data);
      this.cache.set(r.cache);
      this.elapsed.set(r.elapsed_ms);
    });
  }
}
