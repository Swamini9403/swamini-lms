import { Component, inject, signal } from '@angular/core';
import { ApiService, Health } from '../core/api.service';

interface CacheProbe {
  cache: string;
  elapsed_ms: number;
}

@Component({
  selector: 'app-status',
  template: `
    <section class="page-head">
      <h1>System status</h1>
      <p class="muted">Live health of each container in the Docker Compose stack.</p>
    </section>

    <div class="status-grid">
      <div class="status-card">
        <div class="status-top"><b>Frontend</b><span class="dot up"></span></div>
        <p>Angular SPA on Nginx</p>
        <p class="small muted">Container: frontend · port 80</p>
      </div>
      <div class="status-card">
        <div class="status-top"><b>Backend</b><span class="dot" [class.up]="health()?.status === 'healthy'"></span></div>
        <p>Django REST on Gunicorn</p>
        <p class="small muted">Container: {{ health()?.container ?? '…' }} · version {{ health()?.version ?? '…' }}</p>
      </div>
      <div class="status-card">
        <div class="status-top"><b>Database</b><span class="dot" [class.up]="health()?.checks?.database?.status === 'up'"></span></div>
        <p>MySQL {{ health()?.checks?.database?.version ?? '' }}</p>
        <p class="small muted">Data stored on named volume <code>swamini_mysql_data</code></p>
      </div>
      <div class="status-card">
        <div class="status-top"><b>Cache</b><span class="dot" [class.up]="health()?.checks?.cache?.status === 'up'"></span></div>
        <p>Redis 7 ({{ health()?.checks?.cache?.backend ?? '…' }})</p>
        <p class="small muted">Course, category and stats responses cached</p>
      </div>
    </div>

    <p class="small">
      Overall: <span class="badge badge-solid">{{ health()?.status ?? 'checking…' }}</span>
      @if (checkedAt()) { <span class="muted">· checked at {{ checkedAt() }}</span> }
      <button class="btn btn-ghost btn-sm" (click)="refresh()">Re-check</button>
    </p>

    <section class="section">
      <h2>Redis cache test</h2>
      <p class="muted">Calls <code>GET /api/courses/</code> twice. The first call after a change is a MISS (MySQL), the next is a HIT (Redis).</p>
      <button class="btn" (click)="probe()">Run cache test</button>
      @if (probes().length) {
        <table class="table">
          <thead><tr><th>Request</th><th>Cache</th><th>API time</th></tr></thead>
          <tbody>
            @for (p of probes(); track $index) {
              <tr><td>#{{ $index + 1 }}</td><td><span class="badge" [class.badge-solid]="p.cache === 'HIT'">{{ p.cache }}</span></td><td>{{ p.elapsed_ms }} ms</td></tr>
            }
          </tbody>
        </table>
      }
    </section>

    <section class="section">
      <h2>Architecture</h2>
      <div class="arch">
        <div class="arch-node">Browser</div><div class="arch-arrow">→</div>
        <div class="arch-node">frontend<br /><small>Angular + Nginx :80</small></div><div class="arch-arrow">→ /api →</div>
        <div class="arch-node">backend<br /><small>Django REST :8000</small></div><div class="arch-arrow">→</div>
        <div class="arch-col">
          <div class="arch-node">redis<br /><small>cache :6379</small></div>
          <div class="arch-node">mysql<br /><small>DB :3306 + volume</small></div>
        </div>
      </div>
    </section>
  `,
})
export class Status {
  private api = inject(ApiService);

  health = signal<Health | null>(null);
  checkedAt = signal('');
  probes = signal<CacheProbe[]>([]);

  constructor() {
    this.refresh();
  }

  refresh() {
    this.api.health().subscribe({
      next: (h) => this.setHealth(h),
      error: (err) => this.setHealth(err.error),
    });
  }

  probe() {
    this.probes.set([]);
    this.api.courses('', '').subscribe((first) => {
      this.probes.update((p) => [...p, { cache: first.cache, elapsed_ms: first.elapsed_ms }]);
      this.api.courses('', '').subscribe((second) =>
        this.probes.update((p) => [...p, { cache: second.cache, elapsed_ms: second.elapsed_ms }]),
      );
    });
  }

  private setHealth(h: Health) {
    this.health.set(h);
    this.checkedAt.set(new Date().toLocaleTimeString());
  }
}
