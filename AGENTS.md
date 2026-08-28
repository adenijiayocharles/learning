# Repository Guidelines

## Project Structure & Module Organization

This repository is a static learning hub. The root `index.html` lists courses, while each top-level course directory contains its own `README.md` and `index.html`.

- `docker/`: a 12-module Docker course built around `apps/visit-counter/`, with TODO-marked lab files and completed examples under `solution/`.
- `kubernetes/`: a 12-module hands-on course. Numbered directories contain lesson notes, starter files under `manifests/`, and completed examples under `solution/`.
- `kubernetes/apps/hello-app/`: the shared Flask application and Dockerfiles used throughout the Kubernetes labs.
- `cap-theorem/`: a self-contained interactive simulation with its supporting explanation.

Keep course pages self-contained: CSS and JavaScript live inline in each `index.html`. When changing a Docker or Kubernetes module README, update the matching `text/markdown` block in that course's `index.html`; there is no synchronization script.

## Build, Test, and Development Commands

There is no package manager or build step. Preview the repository from its root:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000/index.html`. Open course pages directly to verify navigation and interactive behavior. For Kubernetes solution manifests, use a client-side validation where practical:

```bash
kubectl apply --dry-run=client -f kubernetes/05-services/solution/
```

The Docker, minikube, kubectl, and Helm commands in lesson files are course exercises, not repository build tooling.

## Coding Style & Naming Conventions

Use two-space indentation in HTML, CSS, JavaScript, and YAML; follow four-space PEP 8 indentation in Python. Preserve the existing CSS custom properties and Archivo/Public Sans/JetBrains Mono typography. Name new lab modules with a zero-padded numeric prefix, such as `13-new-topic/`, and use lowercase kebab-case for files and directories. Starter manifests should end in `-starter.yaml` and mark learner work with `# TODO`.

## Testing Guidelines

No automated test suite or coverage target exists. Manually check changed pages at desktop and narrow viewport sizes, exercise interactive controls, and inspect the browser console. Validate YAML and, for lab changes, confirm commands and expected observations against a local minikube cluster. Keep host port `5000` free; examples intentionally use `5050`, `5001`, or similar mappings to avoid macOS AirPlay conflicts.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries such as `Add root README` and `Add CAP Theorem course; refine hub and sidebar styling`. Follow that style and group related changes. Pull requests should explain the learner-facing impact, list verification performed, link relevant issues, and include screenshots for visible UI changes. Call out any changes that require Docker, minikube, or network access to verify.
