import { Component } from '@angular/core';
import { REPO_URL, TEAM } from '../core/team';

@Component({
  selector: 'app-about',
  template: `
    <section class="page-head">
      <h1>About LearnSphere</h1>
      <p class="muted">Case Study 8 — Online Learning Platform: CI/CD + Docker</p>
    </section>

    <div class="about">
      <div class="panel">
        <h3>Project team</h3>
        <table class="table">
          <thead><tr><th>#</th><th>Name</th><th>Details</th></tr></thead>
          <tbody>
            @for (m of team; track m.name; let i = $index) {
              <tr>
                <td>{{ i + 1 }}</td>
                <td><b>{{ m.name }}</b></td>
                <td class="small">
                  @if (m.prn) { PRN {{ m.prn }} · }
                  @if (m.github) { GitHub {{ m.github }} } @else { Team member }
                </td>
              </tr>
            }
          </tbody>
        </table>
        <p class="small">Repository: <a [href]="repoUrl" target="_blank" rel="noopener">github.com/Swamini9403/swamini-lms</a></p>
      </div>

      <div class="panel">
        <h3>Assignment tasks</h3>
        <ol class="tasks">
          <li><b>Dockerfiles</b> — multi-stage builds for Angular (Node → Nginx) and Django (wheels → slim runtime).</li>
          <li><b>Docker Compose</b> — frontend, backend, Redis and MySQL with healthchecks and private networks.</li>
          <li><b>Persistent volumes</b> — MySQL data on the named volume <code>swamini_mysql_data</code>.</li>
          <li><b>GitHub Actions</b> — test → compose integration test → push images to GHCR → deploy to AWS EC2.</li>
        </ol>
        <h3>Learning content</h3>
        <p class="small">9 modules with 38 video lessons. Each lesson has written notes and an embedded YouTube video from a
          well-known educator (Fireship, TechWorld with Nana, Programming with Mosh, freeCodeCamp and others).</p>
      </div>
    </div>
  `,
})
export class About {
  team = TEAM;
  repoUrl = REPO_URL;
}
