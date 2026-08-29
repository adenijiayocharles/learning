# Module 10 — Efficient & Safer Images

## Concepts

Multi-stage builds separate build tools from the final runtime image. The
visit-counter build stage creates Python wheels; the runtime stage installs
only those artifacts. This separation makes the final image easier to reason
about, even when size savings are modest for an interpreted application.

Run application processes as a non-root user unless they genuinely need root.
Keep the build context small, avoid unnecessary packages, rebuild regularly,
and understand that tags are mutable. Pinning a base image digest maximizes
reproducibility, but creates an explicit update responsibility.

## Command and flag guide

- `docker build --check` evaluates the Dockerfile with build checks and reports
  issues without performing a normal image build.
- `-f PATH` selects a Dockerfile whose name or location differs from the default
  `Dockerfile` in the build context.
- The remaining Docker commands and flags in this module were introduced in
  Modules 1–5.

## Hands-on

Run from `docker/apps/visit-counter`.

1. Complete `Dockerfile.optimized-starter`, including ownership of `/data`, using
   `Dockerfile.optimized` only as the reference solution.

2. Ask the builder to check the Dockerfile, then build it:

   ```bash
   docker build --check -f Dockerfile.optimized-starter .
   docker build -f Dockerfile.optimized-starter -t visit-counter:optimized .
   ```

3. Compare image metadata and history:

   ```bash
   docker image ls visit-counter
   docker image history visit-counter:optimized
   docker inspect visit-counter:optimized --format '{{.Config.User}}'
   ```

4. Run the image and prove the process is unprivileged:

   ```bash
   docker run -d --name optimized-counter \
     -p 127.0.0.1:5050:5000 visit-counter:optimized
   docker exec optimized-counter id
   curl http://localhost:5050/healthz
   ```

   The UID should be `10001`, not `0`. Confirm that the unprivileged process
   can still use its intended data path:

   ```bash
   curl -X POST http://localhost:5050/count
   ```

5. Inspect the exact base image reference used by the Dockerfile. A version tag
   such as `python:3.12-slim` can move to newer patched content; a digest-pinned
   reference cannot move until deliberately updated.

6. Clean up:

   ```bash
   docker rm -f optimized-counter
   ```

## Verify

- Explain what is copied between the build and runtime stages.
- Explain why a non-root user limits the impact of an application compromise.
- Describe the maintenance tradeoff introduced by digest pinning.

Official reference: [Building best practices](https://docs.docker.com/build/building/best-practices/)

Next: [Module 11 — Resources & Troubleshooting](../11-resources-troubleshooting/)
