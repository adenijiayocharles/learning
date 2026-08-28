# Module 11 — Resources & Troubleshooting

## Concepts

Containers have no CPU or memory limits by default. Limits protect the host and
make resource assumptions visible, but values must be tested against the real
application. `docker stats` shows live usage; `docker inspect` shows configured
limits and state.

Use a consistent debugging loop: inspect project status, read logs, inspect the
resolved Compose model, inspect container state and networks, then test from
the narrowest relevant boundary. Avoid deleting resources before collecting
evidence.

## Hands-on

`broken-compose.yaml` contains two faults. Diagnose them in order without
looking at `solution/compose.yaml`.

1. Validate and start the stack:

   ```bash
   cd docker/11-resources-troubleshooting
   docker compose -f broken-compose.yaml config --quiet
   docker compose -f broken-compose.yaml up -d --build
   docker compose -f broken-compose.yaml ps
   ```

2. The host request fails. Gather evidence:

   ```bash
   curl -i http://localhost:5050/
   docker compose -f broken-compose.yaml logs web
   docker compose -f broken-compose.yaml port web 5000
   ```

   Fix the published container port: the app listens on `5000`, not `5001`.

3. The root endpoint now works, but the counter returns `503`:

   ```bash
   curl -i http://localhost:5050/count
   docker compose -f broken-compose.yaml exec web python -c \
     'import socket; print(socket.gethostbyname("missing-cache"))'
   ```

   Fix `REDIS_HOST` to the actual Compose service name, `cache`.

4. Add and inspect resource controls:

   ```yaml
   mem_limit: 128m
   cpus: 0.50
   ```

   ```bash
   docker compose -f broken-compose.yaml up -d
   docker stats --no-stream
   docker inspect $(docker compose -f broken-compose.yaml ps -q web) \
     --format 'memory={{.HostConfig.Memory}} nano_cpus={{.HostConfig.NanoCpus}}'
   ```

5. Compare with the solution, then clean up:

   ```bash
   docker compose -f broken-compose.yaml down
   ```

## Verify

- Explain why a valid Compose file can still describe a broken application.
- Identify which evidence exposed each fault.
- Explain why arbitrary low memory limits are unsafe defaults.

Official references: [Resource constraints](https://docs.docker.com/engine/containers/resource_constraints/), [Compose troubleshooting](https://docs.docker.com/compose/troubleshooting/)

Next: [Module 12 — Capstone, Distribution & Cleanup](../12-capstone-distribution/)
