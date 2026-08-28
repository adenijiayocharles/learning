# Docker Foundational Learning Curriculum

## Goal

Teach a complete beginner enough Docker to build, run, connect, persist,
inspect, and troubleshoot containerized applications in normal development
work. The course favors runnable evidence over certification terminology and
uses portable Docker CLI behavior rather than product-specific UI features.

## Design

The 12 modules evolve one Flask visit-counter application. It begins with a
file-backed counter in a single container, connects to Redis on a user-defined
network, moves into Compose, then gains readiness, persistent data, resource
controls, and a multi-stage non-root image. This keeps the learner focused on
the Docker concept that changed.

Module READMEs are the source of truth. `index.html` embeds the same Markdown
for a self-contained, progress-tracked browser experience. Starter files mark
learner decisions with TODOs; completed files live under `solution/`.

## Accuracy principles

- Use the current `docker compose` CLI and canonical `compose.yaml` name.
- Separate image metadata (`EXPOSE`) from runtime publication (`-p`).
- Describe containers as isolated processes, including Docker's Linux VM layer
  on macOS and Windows, rather than as miniature VMs.
- Distinguish startup order, health reporting, restart policies, and
  application retry behavior.
- Prefer explicit `--mount` examples and localhost-bound published ports.
- Treat tags as mutable and digest pinning as a reproducibility/update
  tradeoff.
- Keep registry publication optional and never place credentials in files.

The factual baseline is Docker's official documentation for the Engine,
Build, storage, networking, and Compose specifications.

## Verification

- Run every solution command sequence against a working Docker daemon.
- Validate Compose files with `docker compose config --quiet`.
- Build both the basic and optimized images and confirm the optimized process
  uses UID 10001.
- Check file and Redis persistence, container-name DNS, health gating,
  resource configuration, and the two deliberate troubleshooting failures.
- Confirm all cleanup commands target only resources created by the course.
- Compare every embedded Markdown block with its module README and test the
  browser page at desktop and narrow viewport widths.
