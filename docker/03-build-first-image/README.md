# Module 3 — Build Your First Image

## Concepts

A `Dockerfile` is an ordered recipe for creating an image. `FROM` selects a
base, `WORKDIR` sets the default directory, `COPY` adds files, `RUN` executes
during the build, and `CMD` supplies the default process at runtime. `EXPOSE`
documents a container port; it does not publish that port to the host.

The final `.` in `docker build ... .` is the **build context**. Only files in
that context can be copied. `.dockerignore` excludes files that should not be
sent to the builder, improving performance and reducing the risk of including
secrets.

Each Dockerfile instruction produces build state that later instructions build
upon. Build-time instructions shape the reusable image; runtime settings choose
what happens when a container starts. A successful build therefore creates an
artifact, not a running application—`docker run` creates the container from it.

## Command and flag guide

- `docker build CONTEXT` builds an image from a Dockerfile and the supplied
  context; `-t NAME:TAG` gives the result a repository name and tag.
- The final `.` means “use the current directory as the build context.”
- This module reuses `docker image ls`, `docker run`, `-d`, `--name`, `-p`,
  `docker image inspect`, `docker stop`, and `docker rm` from Modules 1–2.

## Hands-on

All commands run from the shared application directory:

```bash
cd docker/apps/visit-counter
```

1. Copy `Dockerfile.starter` to `Dockerfile`, then replace every `# TODO`.
   Compare your result with `../../03-build-first-image/solution/Dockerfile`
   only after attempting it yourself.

2. Build and tag the image:

   ```bash
   docker build -t visit-counter:v1 .
   docker image ls visit-counter
   ```

3. Run it and publish its port:

   ```bash
   docker run -d --name visit-counter \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl http://localhost:5050/
   curl http://localhost:5050/config
   ```

   Port `5050` avoids the common macOS AirPlay conflict on host port `5000`.
   The app still listens on port `5000` inside the container.

4. Inspect image metadata and clean up the container:

   ```bash
   docker image inspect visit-counter:v1
   docker stop visit-counter
   docker rm visit-counter
   ```

## Verify

- Explain why `EXPOSE 5000` did not make the app reachable by itself.
- Identify which files `.dockerignore` prevents from entering the context.
- Distinguish a build-time `RUN` instruction from runtime `CMD`.

Official references: [Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/), [Build context](https://docs.docker.com/build/concepts/context/)

Next: [Module 4 — Layers, Cache & Image History](../04-layers-cache/)
