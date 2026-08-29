# Module 6 — Persistent Data & Mounts

## Concepts

Files written only to a container's writable layer disappear when that
container is removed. A **volume** is persistent storage managed by Docker. A
**bind mount** maps a specific host path into a container and is useful for
source or configuration files, but couples the container to the host layout.

Prefer the explicit `--mount` syntax in learning material. Bind mounts are
writable by default, so use `readonly` when the container only needs to read.

Storage lifetime is separate from container lifetime. A named volume can be
attached to successive containers and is portable across Compose recreations
on the same Docker host. A bind mount exposes an exact host path instead, giving
direct access but also making permissions and path availability host-dependent.

### Mount types and when to use them

| Type | Data location and lifetime | Use it when | Avoid it when |
| --- | --- | --- | --- |
| Named volume | Docker manages the host location; data survives container removal until the volume is removed | Persisting databases, queues, uploads, or other application data | People or host tools must edit the files directly |
| Anonymous volume | Docker manages the location and generates the name; it can outlive its container unless removed with it | An image needs disposable Docker-managed storage and you do not need to reuse it by name | Data must be easy to identify, reuse, back up, or clean up |
| Bind mount | An exact host file or directory is mounted; its data follows the host path's lifetime | Sharing source code, configuration, certificates, or generated output with the host | The workload must be portable across hosts or isolated from host filesystem changes |
| `tmpfs` mount | Data is kept in host memory and disappears when the container stops or restarts | Temporary caches, scratch data, or sensitive files that should not be written to disk | The data must persist or may grow beyond available memory |

For most persistent application data, start with a **named volume**. Use a
**bind mount** when direct host access is the requirement, and make it read-only
when the container does not need to change it. Use **`tmpfs`** only for
deliberately temporary data. Data left in the container's writable layer is not
a mount type and should not be used for data that must survive container removal.

## Command and flag guide

- `docker volume create NAME` creates Docker-managed persistent storage;
  `docker volume inspect NAME` shows its metadata and host location, and
  `docker volume rm NAME` deletes it when no container uses it.
- `--mount` attaches storage to a container. Its comma-separated fields describe
  the mount: `type=volume` uses a named volume, `type=bind` uses a host path,
  and `type=tmpfs` uses memory-backed temporary storage. `src` is the source
  (and is omitted for `tmpfs`), `dst` is the container path, and `readonly`
  prevents writes through the mount.
- `$PWD` is expanded by the host shell to the current directory before Docker
  receives the bind-mount source path.

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
- Identify when an anonymous volume or `tmpfs` mount is appropriate.
- Explain why read-only bind mounts reduce risk.
- Explain why removing a container does not automatically remove its volume.

Official references: [Docker storage](https://docs.docker.com/engine/storage/), [Volumes](https://docs.docker.com/engine/storage/volumes/), [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [`tmpfs` mounts](https://docs.docker.com/engine/storage/tmpfs/)

Next: [Module 7 — Container Networking](../07-container-networking/)
