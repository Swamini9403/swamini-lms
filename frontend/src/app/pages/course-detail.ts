import { Component, inject, input, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { ApiService, Course } from '../core/api.service';

@Component({
  selector: 'app-course-detail',
  imports: [RouterLink, FormsModule],
  template: `
    <a routerLink="/courses" class="link small">← Back to catalog</a>
    @if (course(); as c) {
      <section class="detail">
        <div>
          <span class="tag">{{ c.category }}</span>
          <h1>{{ c.title }}</h1>
          <p class="lead">{{ c.description }}</p>
          <div class="meta">
            <span>Instructor: {{ c.instructor }}</span><span>{{ c.level }}</span>
            <span>{{ c.duration_hours }} hours</span><span>★ {{ c.rating }}</span><span>{{ c.enrollment_count }} enrolled</span>
          </div>

          <h2>Lessons</h2>
          <ol class="lessons">
            @for (l of c.lessons; track l.id) {
              <li><span>{{ l.title }}</span><span class="muted">{{ l.duration_minutes }} min</span></li>
            }
          </ol>
        </div>

        <aside class="panel">
          <h3>Enroll in this course</h3>
          <form (ngSubmit)="enroll(c.id)">
            <label>Full name<input class="input" name="name" [(ngModel)]="name" required /></label>
            <label>Email<input class="input" name="email" type="email" [(ngModel)]="email" required /></label>
            <button class="btn full" type="submit" [disabled]="busy()">{{ busy() ? 'Enrolling…' : 'Enroll now' }}</button>
          </form>
          @if (message()) {
            <p class="notice" [class.error]="isError()">{{ message() }}</p>
          }
          <p class="small muted">Saved to MySQL; the Redis cache version is bumped so counts refresh instantly.</p>
        </aside>
      </section>
    } @else {
      <p class="muted">Loading course…</p>
    }
  `,
})
export class CourseDetail implements OnInit {
  private api = inject(ApiService);

  id = input.required<string>();
  course = signal<Course | null>(null);
  name = '';
  email = '';
  busy = signal(false);
  message = signal('');
  isError = signal(false);

  ngOnInit() {
    this.load();
  }

  load() {
    this.api.course(Number(this.id())).subscribe((r) => this.course.set(r.data));
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
