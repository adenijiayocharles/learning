# Learning

Self-paced, hands-on courses for learning infrastructure and engineering
topics — each one pairs short concept notes with real exercises you run
yourself, not slides.

## Getting started

Open [`index.html`](./index.html) in a browser for a launcher page listing
every course in this repo. Each course also has its own `index.html` if you
want to jump straight in.

## Courses

| Course | Modules | Description |
|--------|---------|-------------|
| [Kubernetes](./kubernetes/) | 12 | From Docker fundamentals to Helm — build, break, and fix a real local cluster with one running app throughout. |

More courses land here as they're built.

## How a course is structured

Every course follows the same shape:

- **`README.md`** — course index and prerequisites.
- **`index.html`** — a browsable version of the course with navigation and
  progress tracking, generated from the same content as the READMEs.
- Numbered module folders, each with a `README.md` (concept + hands-on
  exercise), starter manifests/config with `# TODO`s to fill in, and a
  `solution/` to check your work against.
