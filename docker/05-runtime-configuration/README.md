# Module 5 — Runtime Configuration, Processes & Ports

## Concepts

An image supplies defaults; each container adds runtime configuration.
Environment variables, mounts, published ports, and command overrides let one
image run in different environments. Do not bake credentials into images or
commit them in environment files.

The image's `CMD` starts `python app.py` as PID 1. PID 1 receives container
stop signals and its exit ends the container. Exec-form JSON commands avoid an
extra shell and generally forward signals more predictably than shell-form
commands.

Runtime configuration belongs to a particular container, not to the image it
came from. Publishing a port creates a host-to-container forwarding rule;
setting an environment variable changes process input; overriding the command
changes the process itself. These choices can vary independently while every
container still uses identical image content.

## Command and flag guide

- `-e NAME=VALUE` sets one environment variable in the new container;
  `--env-file PATH` loads multiple variables from a file.
- `docker top CONTAINER` lists processes running inside a container.
- `docker rm -f CONTAINER` force-removes a running container (stopping it
  first); use it deliberately because the process gets less time to shut down.
- `docker port CONTAINER` displays the container-to-host port mappings.
- `{{json ...}}` inside `--format` renders the selected value as JSON; it is part
  of the formatting template, not another command-line flag.

## Hands-on

Run from the repository root after building `visit-counter:v1`.

1. Override the message and bind only to localhost:

   ```bash
   docker run -d --name configured-counter \
     -p 127.0.0.1:5050:5000 \
     -e MESSAGE='Configured at runtime' \
     visit-counter:v1
   curl http://localhost:5050/
   ```

2. Inspect the process and configuration:

   ```bash
   docker top configured-counter
   docker exec configured-counter sh -c "tr '\0' ' ' </proc/1/cmdline"
   docker inspect configured-counter --format '{{json .Config.Env}}'
   ```

   Inspection can reveal environment values; this is one reason environment
   variables are not a complete secret-management solution.

3. Use an environment file:

   ```bash
   docker rm -f configured-counter
   docker run -d --name configured-counter \
     --env-file docker/05-runtime-configuration/solution/runtime.env \
     -p 127.0.0.1:5050:5000 visit-counter:v1
   curl http://localhost:5050/config
   ```

4. Contrast metadata with publication:

   ```bash
   docker inspect visit-counter:v1 --format '{{json .Config.ExposedPorts}}'
   docker port configured-counter
   ```

5. Stop the container and observe graceful termination:

   ```bash
   docker stop configured-counter
   docker rm configured-counter
   ```

## Verify

- Distinguish the host port from the container port in `5050:5000`.
- Explain why `EXPOSE` and `-p` serve different purposes.
- Explain why secrets should not be passed in committed environment files.

Official references: [Publishing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/), [Dockerfile `CMD`](https://docs.docker.com/reference/dockerfile/#cmd)

Next: [Module 6 — Persistent Data & Mounts](../06-persistent-data/)
