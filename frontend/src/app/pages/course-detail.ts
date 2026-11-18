import { Component, computed, inject, input, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { Router, RouterLink } from '@angular/router';
import { ApiService, Course } from '../core/api.service';
import { embedUrl, isVideoId } from '../core/youtube';

@Component({
  selector: 'app-course-detail',
  imports: [RouterLink, FormsModule],
  template: `
    <a routerLink="/courses" class="link small">← All modules</a>
    @if (course(); as c) {
      <section class="module-head">
        <span class="tag">Module {{ c.module_no }} · {{ c.category }}</span>
        <h1>{{ c.title }}</h1>
        <p class="lead">{{ c.description }}</p>
        <div class="meta">
          <span>Curated by {{ c.instructor }}</span><span>{{ c.level }}</span><span>{{ c.lessons?.length }} video lessons</span>
          <span>{{ c.duration_hours }} hours</span><span>★ {{ c.rating }}</span><span>{{ c.enrollment_count }} enrolled</span>
        </div>
      </section>

      <section class="learn">
        <div>
          @if (current(); as l) {
            <div class="player">
              @if (videoSrc(); as src) {
                <iframe [src]="src" [title]="l.video_title" frameborder="0" allowfullscreen
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>
              }
            </div>
            <div class="lesson-info">
              <p class="eyebrow">Lesson {{ l.order }} of {{ c.lessons?.length }}</p>
              <h2>{{ l.title }}</h2>
              <p class="small muted">Video: “{{ l.video_title }}” — {{ l.channel }}</p>
              <h3>Lesson notes</h3>
              <p>{{ l.summary }}</p>
              <div class="lesson-nav">
                <button class="btn btn-ghost" [disabled]="index() === 0" (click)="select(index() - 1)">← Previous</button>
                <button class="btn" [disabled]="index() === (c.lessons?.length ?? 1) - 1" (click)="select(index() + 1)">Next lesson →</button>
              </div>
            </div>
          }
        </div>

        <aside class="side">
          <div class="panel playlist">
            <h3>Module playlist</h3>
            <ol>
              @for (l of c.lessons; track l.id; let i = $index) {
                <li [class.on]="i === index()" (click)="select(i)">
                  <span class="pl-no">{{ l.order }}</span>
                  <span><b>{{ l.title }}</b><br /><small class="muted">{{ l.channel }}</small></span>
                </li>
              }
            </ol>
          </div>

          <div class="panel">
            <h3>Enroll in this module</h3>
            <form (ngSubmit)="enroll(c.id)">
              <label>Full name<input class="input" name="name" [(ngModel)]="name" required /></label>
              <label>Email<input class="input" name="email" type="email" [(ngModel)]="email" required /></label>
              <button class="btn full" type="submit" [disabled]="busy()">{{ busy() ? 'Enrolling…' : 'Enroll now' }}</button>
            </form>
            @if (message()) {
              <p class="notice" [class.error]="isError()">{{ message() }}</p>
            }
            <p class="small muted">Saved to MySQL; the Redis cache version is bumped so counts refresh instantly.</p>
          </div>
        </aside>
      </section>
    } @else {
      <p class="muted">Loading module…</p>
    }
  `,
})
export class CourseDetail implements OnInit {
  private api = inject(ApiService);
  private router = inject(Router);
  private sanitizer = inject(DomSanitizer);

  id = input.required<string>();
  lesson = input<string>();
  course = signal<Course | null>(null);
  index = signal(0);
  current = computed(() => this.course()?.lessons?.[this.index()] ?? null);
  videoSrc = computed<SafeResourceUrl | null>(() => {
    const id = this.current()?.video_id;
    return isVideoId(id) ? this.sanitizer.bypassSecurityTrustResourceUrl(embedUrl(id)) : null;
  });

  name = '';
  email = '';
  busy = signal(false);
  message = signal('');
  isError = signal(false);

  ngOnInit() {
    this.load(true);
  }

  load(initial = false) {
    this.api.course(Number(this.id())).subscribe((r) => {
      this.course.set(r.data);
      if (initial) {
        const requested = Number(this.lesson() ?? 1) - 1;
        this.index.set(Math.min(Math.max(requested, 0), (r.data.lessons?.length ?? 1) - 1));
      }
    });
  }

  select(i: number) {
    this.index.set(i);
    this.router.navigate([], { queryParams: { lesson: i + 1 }, replaceUrl: true });
  }

  enroll(courseId: number) {
    if (!this.name.trim() || !this.email.trim()) {
      this.isError.set(true);
      this.message.set('Please enter your name and email.');
      return;
    }
    this.busy.set(true);
    this.api.enroll(courseId, this.name.trim(), this.email.trim()).subscribe({
      next: (e) => {
        this.isError.set(false);
        this.message.set(`Enrolled ${e.student_name} in “${e.course_title}”.`);
        this.busy.set(false);
        this.load();
      },
      error: (err) => {
        this.isError.set(true);
        this.message.set(err.error?.detail ?? 'Enrollment failed. Check the details and try again.');
        this.busy.set(false);
      },
    });
  }
}
