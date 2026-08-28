# Module 8 — Compose Fundamentals

## Concepts

Docker Compose describes a multi-container application in YAML. The preferred
filename is `compose.yaml`, and the current CLI form is `docker compose`.
Services define containers; top-level volumes and networks define shared
resources. Compose creates a project-scoped default network, and each service
is discoverable by its service name.

A Dockerfile defines how to build an image. A Compose file defines how one or
more containers run. These files complement rather than replace each other.

## Hands-on

Run from `docker/08-compose-fundamentals`.

1. Complete `compose-starter.yaml`: mount `redis-data` at `/data` in the cache
   service and declare the volume at the top level.

2. Render the fully resolved model before starting anything:

   ```bash
   docker compose -f compose-starter.yaml config
   ```

   Compare with `solution/compose.yaml` if validation fails.

3. Build and start the project:

   ```bash
   docker compose -f compose-starter.yaml up -d --build
   docker compose -f compose-starter.yaml ps
   docker compose -f compose-starter.yaml logs
   ```

4. Exercise the application and inspect Compose-created resources:

   ```bash
   curl -X POST http://localhost:5050/count
   docker compose -f compose-starter.yaml exec web python -c \
     'import socket; print(socket.gethostbyname("cache"))'
   docker network ls
   docker volume ls
   ```

5. Recreate the services and confirm the named volume keeps the count:

   ```bash
   docker compose -f compose-starter.yaml down
   docker compose -f compose-starter.yaml up -d
   curl http://localhost:5050/count
   ```

6. Remove services and the project volume:

   ```bash
   docker compose -f compose-starter.yaml down --volumes
   ```

   Omitting `--volumes` deliberately preserves named volumes.

## Verify

- Identify the service name used as Redis's DNS name.
- Explain what `docker compose config` checks and expands.
- Explain the difference between `down` and `down --volumes`.

Official references: [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/), [Compose CLI](https://docs.docker.com/compose/reference/)

Next: [Module 9 — Reliable Compose Applications](../09-reliable-compose/)
