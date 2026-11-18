import { Component } from '@angular/core';

@Component({
  selector: 'app-about',
  template: `
    <section class="page-head">
      <h1>About this project</h1>
      <p class="muted">Case Study 8 — Online Learning Platform: CI/CD + Docker</p>
    </section>

    <div class="about">
      <div class="panel">
        <h3>Student</h3>
        <dl class="kv">
          <dt>Name</dt><dd>Swamini</dd>
          <dt>PRN</dt><dd>202402040005</dd>
          <dt>GitHub</dt><dd><a href="https://github.com/swamini9403" target="_blank" rel="noopener">swamini9403</a></dd>
          <dt>Repository</dt><dd><a href="https://github.com/swamini9403/swamini-lms" target="_blank" rel="noopener">swamini9403/swamini-lms</a></dd>
        </dl>
      </div>

      <div class="panel">
        <h3>Assignment tasks</h3>
        <ol class="tasks">
          <li><b>Dockerfiles</b> — multi-stage builds for Angular (Node → Nginx) and Django (wheels → slim runtime).</li>
          <li><b>Docker Compose</b> — frontend, backend, Redis and MySQL with healthchecks and a private network.</li>
          <li><b>Persistent volumes</b> — MySQL data on the named volume <code>swamini_mysql_data</code>.</li>
          <li><b>GitHub Actions</b> — test → compose integration test → push images to GHCR → deploy to AWS EC2.</li>
        </ol>
      </div>
    </div>
  `,
})
export class About {}
