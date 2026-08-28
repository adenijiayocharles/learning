# Docker — Foundational Curriculum

A hands-on, 12-module course for learning Docker from first principles to
solid day-to-day working knowledge. Every module introduces one idea, applies
it to a real local environment, and ends with checks you should be able to
explain rather than merely copy.

Prefer a browser? Open [`index.html`](./index.html) for a navigable version
with progress tracking. [`PLAN.md`](./PLAN.md) records the course design and
verification approach.

## Prerequisites

- A terminal and text editor
- A working Docker-compatible daemon and `docker` CLI
- Docker Compose available as `docker compose`
- `curl` for exercising the demo application

Run `docker version` before starting. Both Client and Server sections must be
present. The labs use portable CLI behavior and work with Docker Desktop,
OrbStack, or Docker Engine running Linux containers.

## How each module works

Each numbered folder contains a `README.md` with concepts, exact commands,
expected observations, and a short verification section. Exercises that need
configuration provide a TODO-marked starter and a completed `solution/`.
Attempt the starter before comparing it with the solution.

All modules evolve one Flask application in [`apps/visit-counter`](./apps/visit-counter/).
It starts as a single file-backed container, then gains Redis, Compose,
health checks, persistent storage, and an optimized non-root image.

## Modules

| # | Module | Concept |
|---|--------|---------|
| 1 | [Containers & Architecture](./01-containers-architecture/) | Images, containers, client, daemon |
| 2 | [Lifecycle & Inspection](./02-container-lifecycle/) | Run, stop, logs, exec, inspect |
| 3 | [Build Your First Image](./03-build-first-image/) | Dockerfiles and build context |
| 4 | [Layers & Cache](./04-layers-cache/) | Cache invalidation and image history |
| 5 | [Runtime Configuration](./05-runtime-configuration/) | Environment, processes, ports |
| 6 | [Persistent Data](./06-persistent-data/) | Volumes and bind mounts |
| 7 | [Container Networking](./07-container-networking/) | Bridge networks and DNS |
| 8 | [Compose Fundamentals](./08-compose-fundamentals/) | Multi-container application model |
| 9 | [Reliable Compose](./09-reliable-compose/) | Health checks and startup ordering |
| 10 | [Efficient & Safer Images](./10-efficient-secure-images/) | Multi-stage builds and non-root users |
| 11 | [Resources & Troubleshooting](./11-resources-troubleshooting/) | Limits and debugging workflow |
| 12 | [Capstone & Distribution](./12-capstone-distribution/) | Complete stack, image transfer, registry |

## Safety and cleanup

Commands use course-specific names and localhost-bound ports. Cleanup steps
remove only those resources. The course deliberately avoids broad pruning
commands because they can remove unrelated Docker data.
