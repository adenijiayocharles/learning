# Module 6 — Persistent Data & Mounts

## Concepts

Files written only to a container's writable layer disappear when that
container is removed. A **volume** is persistent storage managed by Docker. A
**bind mount** maps a specific host path into a container and is useful for
source or configuration files, but couples the container to the host layout.

Prefer the explicit `--mount` syntax in learning material. Bind mounts are
writable by default, so use `readonly` when the container only needs to read.

## Hands-on

1. Demonstrate ephemeral container data:

   ```bash
   docker run -d --name visit-counter \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl -X POST http://localhost:5050/count
   curl http://localhost:5050/count
   docker rm -f visit-counter
   docker run -d --name visit-counter \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl http://localhost:5050/count
   ```

   The recreated container starts at zero.

2. Recreate it with a named volume:

   ```bash
   docker rm -f visit-counter
   docker volume create visit-data
   docker run -d --name visit-counter \
     --mount type=volume,src=visit-data,dst=/data \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl -X POST http://localhost:5050/count
   docker rm -f visit-counter
   docker run -d --name visit-counter \
     --mount type=volume,src=visit-data,dst=/data \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl http://localhost:5050/count
   ```

3. Inspect the managed volume:

   ```bash
   docker volume inspect visit-data
   ```

4. Bind-mount the example configuration read-only:

   ```bash
   docker run --rm \
     --mount type=bind,src="$PWD/docker/apps/visit-counter/.env.example",dst=/config/app.env,readonly \
     alpine:3.22 cat /config/app.env
   ```

5. Clean up only this lab's resources:

   ```bash
   docker rm -f visit-counter
   docker volume rm visit-data
   ```

## Verify

- Choose a named volume for database data and a bind mount for editable source.
- Explain why read-only bind mounts reduce risk.
- Explain why removing a container does not automatically remove its volume.

Official references: [Docker storage](https://docs.docker.com/engine/storage/), [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

Next: [Module 7 — Container Networking](../07-container-networking/)
