# Module 9 — Reliable Compose Applications

## Concepts

Starting a dependency before an application does not mean the dependency is
ready to accept connections. A health check gives Docker an application-level
signal. Long-form `depends_on` with `condition: service_healthy` makes Compose
wait for that signal before creating the dependent service.

A health check reports health; it does not restart an unhealthy container.
Restart policies respond when a container exits or the daemon restarts, with
different behavior for manual stops. Application retries are still important
because dependencies can fail after startup.

## Command and flag guide

- `config --quiet` validates the Compose model without printing it.
- `docker compose ps -q SERVICE` prints only that service container's ID. The
  host shell's `$(...)` substitutes that ID into the surrounding `docker inspect`
  command.
- `docker compose stop SERVICE` stops a service container without removing it;
  `start SERVICE` starts that same container again.

## Hands-on

Run from `docker/09-reliable-compose`.

1. Complete the TODOs in `compose-starter.yaml` so Redis runs
   `redis-cli ping` and the web service waits for `service_healthy`.

2. Validate and start it:

   ```bash
   docker compose -f compose-starter.yaml config --quiet
   docker compose -f compose-starter.yaml up -d --build
   docker compose -f compose-starter.yaml ps
   ```

   Redis should become `healthy` before the web service starts.

3. Inspect the raw health state:

   ```bash
   docker inspect $(docker compose -f compose-starter.yaml ps -q cache) \
     --format '{{json .State.Health}}'
   curl http://localhost:5050/healthz
   ```

4. Stop Redis and observe dependency failure after startup:

   ```bash
   docker compose -f compose-starter.yaml stop cache
   curl -i http://localhost:5050/healthz
   docker compose -f compose-starter.yaml start cache
   ```

   `depends_on` controls startup ordering; it does not continuously repair the
   web service's dependency.

5. Inspect the restart policy and clean up:

   ```bash
   docker inspect $(docker compose -f compose-starter.yaml ps -q web) \
     --format '{{.HostConfig.RestartPolicy.Name}}'
   docker compose -f compose-starter.yaml down --volumes
   ```

## Verify

- Distinguish “running” from “healthy.”
- Explain what `service_healthy` guarantees and what it does not.
- Explain why health checks and application retry logic are complementary.

Official references: [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/), [Restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/)

Next: [Module 10 — Efficient & Safer Images](../10-efficient-secure-images/)
