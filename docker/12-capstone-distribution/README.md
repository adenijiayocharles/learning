# Module 12 — Capstone, Distribution & Cleanup

## Concepts

An image name can include a registry host, namespace, repository, tag, or
immutable digest. Registries store and distribute images; containers are
created from pulled image content. Pushing to Docker Hub requires an account
and repository, so that exercise is optional.

`docker image save` and `docker image load` transfer image archives without a
registry. Cleanup should target known course resources. Broad commands such as
`docker system prune` can delete unrelated caches and stopped resources and are
intentionally not part of this course.

A tag is a movable human-friendly reference; a digest identifies exact image
content. Registries distribute layers and repository metadata, while `save`
and `load` package image content for offline transfer. Distribution does not
include runtime volumes, environment values, or other container state.

## Command and flag guide

- `docker compose up --wait` waits until services are running or healthy;
  `--force-recreate` replaces containers even when their configuration and
  image appear unchanged.
- `docker image save IMAGE -o FILE` writes an image archive to a file;
  `docker image load -i FILE` reads an image archive from a file.
- `docker login` authenticates to a registry, `docker tag SOURCE TARGET` adds
  another name to an image, and `docker push IMAGE` uploads it to a registry.
- `docker image rm IMAGE` removes the named image from the local image store.

## Hands-on

1. From `docker/12-capstone-distribution`, review `compose-starter.yaml`. Fill
   in anything you removed while experimenting, then compare it with
   `solution/compose.yaml`.

2. Validate and launch the complete stack:

   ```bash
   docker compose -f solution/compose.yaml config --quiet
   docker compose -f solution/compose.yaml up -d --build --wait
   docker compose -f solution/compose.yaml ps
   curl http://localhost:5050/
   curl -X POST http://localhost:5050/count
   curl http://localhost:5050/healthz
   ```

3. Confirm the final image runs as the unprivileged user and Redis data
   survives service recreation:

   ```bash
   docker compose -f solution/compose.yaml exec web id
   docker compose -f solution/compose.yaml up -d --force-recreate --wait
   curl http://localhost:5050/count
   ```

4. Save and reload the image locally:

   ```bash
   docker image save visit-counter:capstone -o /tmp/visit-counter-capstone.tar
   docker image load -i /tmp/visit-counter-capstone.tar
   ```

5. **Optional Docker Hub exercise.** Replace `YOUR_DOCKER_ID`, sign in using
   an access token when possible, then push and inspect the resulting digest:

   ```bash
   docker login
   docker tag visit-counter:capstone YOUR_DOCKER_ID/visit-counter:v1
   docker push YOUR_DOCKER_ID/visit-counter:v1
   docker image inspect YOUR_DOCKER_ID/visit-counter:v1 \
     --format '{{json .RepoDigests}}'
   ```

   Never commit registry credentials or tokens.

6. Remove only course resources:

   ```bash
   docker compose -f solution/compose.yaml down --volumes
   docker image rm visit-counter:capstone
   ```

## Verify

- Explain the roles of a repository, tag, and digest.
- Explain what survived container recreation and why.
- Walk through `ps` → `logs` → `inspect` → network/config test from memory.

Official references: [Build and push an image](https://docs.docker.com/get-started/introduction/build-and-push-first-image/), [Image save](https://docs.docker.com/reference/cli/docker/image/save/)

You now have practical working knowledge of Docker's core objects, builds,
runtime configuration, storage, networking, Compose, hardening, and debugging.
