# Learning

Self-paced courses for learning infrastructure and engineering topics —
each one pairs short concept notes with a real, hands-on way to explore
them: labs for some, interactive simulations for others.

## Getting started

Open [`index.html`](./index.html) in a browser for a launcher page listing
every course in this repo. Each course also has its own `index.html` if you
want to jump straight in.

## Courses

| Course | Format | Description |
|--------|--------|-------------|
| [Kubernetes](./kubernetes/) | 12-module hands-on lab | From Docker fundamentals to Helm — build, break, and fix a real local cluster with one running app throughout. |
| [CAP Theorem](./cap-theorem/) | Interactive simulation | Cut off a node, watch the consistency/availability tradeoff play out, then heal it — a low-poly, isometric, accurately-sourced look at what CAP theorem actually says. |

More courses land here as they're built.

## How a course is structured

Every course has a `README.md` and an `index.html` you can open directly in
a browser. Beyond that, the shape depends on the format:

- **Hands-on labs** (e.g. Kubernetes) add numbered module folders, each with
  its own `README.md` (concept + exercise), starter manifests/config with
  `# TODO`s to fill in, and a `solution/` to check your work against; the
  `index.html` is a navigable, progress-tracked version of those READMEs.
- **Interactive simulations** (e.g. CAP Theorem) skip the module/solution
  structure entirely — the `index.html` *is* the course, and the `README.md`
  is the sourced explanation behind what it's simulating.
