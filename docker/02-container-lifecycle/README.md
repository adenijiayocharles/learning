# Module 2 — Container Lifecycle & Inspection

## Concepts

`docker run` combines image pull (when needed), container creation, and
container start. A stopped container still exists until removed, including its
writable layer and metadata. `docker ps` lists running containers;
`docker ps -a` includes stopped ones.

The main container process determines its lifecycle. When PID 1 exits, the
container stops. Logs capture the process's standard output and error streams;
`exec` starts an additional process inside an already-running container.

Container identity survives a stop: its name, configuration, exit status, and
writable layer remain available for inspection or restart. Removal is the step
that discards that container state. Treat containers as replaceable in normal
operation, but inspect failures before removing the evidence.

## Command and flag guide

- `-d` runs the container in the background (detached mode), while `--name NAME`
  assigns a memorable name instead of a generated one.
- `-p HOST_IP:HOST_PORT:CONTAINER_PORT` publishes a container port through the
  host. Here, only `127.0.0.1:8080` forwards to port `80` in the container.
- `docker ps` lists running containers; `-a` includes stopped containers and
  `--filter name=VALUE` narrows the results by name.
- `docker logs CONTAINER` shows the main process's output; `docker inspect`
  shows detailed JSON configuration and state.
- `docker exec CONTAINER COMMAND` runs an extra command in a running container.
- `docker stop` requests a graceful stop, `docker start` restarts an existing
  stopped container, and `docker rm` deletes a stopped container.
- `--format TEMPLATE` selects fields from inspect output using a Go template.
- In `sh -c '...'`, `-c` belongs to the shell, not Docker: it tells `sh` to run
  the following string as a command.

## Hands-on

1. Start an Nginx container in the background:

   ```bash
   docker run -d --name lifecycle-web -p 127.0.0.1:8080:80 nginx:1.28-alpine
   curl http://localhost:8080/
   ```

   Binding to `127.0.0.1` keeps the published port reachable only from this
   host. `-d` detaches the terminal.

2. Inspect it from several angles:

   ```bash
   docker ps
   docker logs lifecycle-web
   docker inspect lifecycle-web
   docker exec lifecycle-web cat /etc/nginx/conf.d/default.conf
   ```

3. Stop and restart the same container:

   ```bash
   docker stop lifecycle-web
   docker ps -a --filter name=lifecycle-web
   docker start lifecycle-web
   curl http://localhost:8080/
   ```

4. Remove it. A running container must first be stopped or explicitly forced:

   ```bash
   docker stop lifecycle-web
   docker rm lifecycle-web
   docker ps -a --filter name=lifecycle-web
   ```

5. Observe an exit code:

   ```bash
   docker run --name exit-demo alpine:3.22 sh -c 'echo about-to-exit; exit 7'
   docker inspect exit-demo --format '{{.State.ExitCode}}'
   docker rm exit-demo
   ```

## Verify

- Explain why `docker stop` does not delete a container.
- Describe the difference between `docker exec` and `docker run`.
- Predict what happens when the container's main process exits.

Official reference: [Run containers](https://docs.docker.com/engine/containers/run/)

Next: [Module 3 — Build Your First Image](../03-build-first-image/)
