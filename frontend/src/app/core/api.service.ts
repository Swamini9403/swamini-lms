import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

export interface Cached<T> {
  cache: 'HIT' | 'MISS';
  elapsed_ms: number;
  data: T;
}

export interface Lesson {
  id: number;
  title: string;
  order: number;
  duration_minutes: number;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  category: string;
  instructor: string;
  level: string;
  duration_hours: number;
  rating: string;
  description: string;
  lesson_count: number;
  enrollment_count: number;
  lessons?: Lesson[];
}

export interface Stats {
  courses: number;
  lessons: number;
  enrollments: number;
  categories: number;
}

export interface Enrollment {
  id: number;
  course: number;
  course_title: string;
  student_name: string;
  student_email: string;
  enrolled_at: string;
}

export interface Health {
  status: string;
  service: string;
  version: string;
  container: string;
  checks: {
    database: { status: string; engine?: string; version?: string; error?: string };
    cache: { status: string; backend?: string; error?: string };
  };
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private base = '/api';

  stats() {
    return this.http.get<Cached<Stats>>(`${this.base}/stats/`);
  }

  categories() {
    return this.http.get<Cached<string[]>>(`${this.base}/categories/`);
  }

  courses(search = '', category = '') {
    return this.http.get<Cached<Course[]>>(`${this.base}/courses/`, { params: { search, category } });
  }

  course(id: number) {
    return this.http.get<Cached<Course>>(`${this.base}/courses/${id}/`);
  }

  enrollments() {
    return this.http.get<Enrollment[]>(`${this.base}/enrollments/`);
  }

  enroll(course: number, student_name: string, student_email: string) {
    return this.http.post<Enrollment>(`${this.base}/enrollments/`, { course, student_name, student_email });
  }

  health() {
    return this.http.get<Health>(`${this.base}/health/`);
  }
}
