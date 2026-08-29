# Module 1 — Containers & Docker Architecture

## Concepts

Docker packages an application and its dependencies as an **image**. A
**container** is a runnable instance of that image. Containers are isolated
processes, not small virtual machines: Linux namespaces isolate resources and
cgroups account for and limit them. On macOS and Windows, Docker-compatible
tools run Linux containers inside a lightweight Linux VM.

Docker uses a client/server design. The `docker` CLI sends API requests to a
Docker daemon, which manages images, containers, networks, and volumes. The
client and daemon may be on different machines, so commands such as bind mounts
refer to paths visible to the daemon.

## Command and flag guide

- `docker version` reports client and daemon versions; `docker info` reports the
  daemon's wider configuration and current resource counts.
- `docker run IMAGE [COMMAND]` creates and starts a new container from an image.
- `--rm` automatically deletes that container when it stops. It does not delete
  the image.
- `docker image ls [IMAGE]` lists local images, optionally filtered by name.
- `docker image inspect IMAGE` prints detailed image metadata as JSON.
- `-i` keeps standard input open and `-t` allocates a terminal. The combined
  `-it` makes an interactive shell behave like a normal terminal.
- In `alpine:3.22`, `alpine` is the image repository and `3.22` is its tag;
  the trailing `sh` replaces the image's default command with a shell.

## Hands-on

1. Confirm both sides are available:

   ```bash
   docker version
   docker info
   ```

   `docker version` should show both Client and Server sections. A client-only
   result means the CLI is installed but cannot reach the daemon.

2. Run a disposable container:

   ```bash
   docker run --rm hello-world
   ```

   If the image is not local, Docker pulls it from its configured registry,
   creates a container, starts its process, and removes the stopped container
   because of `--rm`.

3. Inspect the image that remains:

   ```bash
   docker image ls hello-world
   docker image inspect hello-world
   ```

4. Run a shell in an Alpine container and inspect its environment:

   ```bash
   docker run --rm -it alpine:3.22 sh
   cat /etc/os-release
   hostname
   exit
   ```

   The displayed distribution is the container filesystem, while the kernel is
   supplied by the Linux host or Docker's Linux VM.

## Verify

- Explain the difference between an image and a container.
- Identify which component actually creates containers: the CLI or daemon.
- Explain why a Linux container on macOS still uses a Linux kernel.

Official references: [Docker overview](https://docs.docker.com/get-started/docker-overview/), [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)

Next: [Module 2 — Container Lifecycle & Inspection](../02-container-lifecycle/)
