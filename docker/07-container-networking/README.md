# Module 7 — Container Networking

## Concepts

Containers have isolated network namespaces. Publishing a port makes a
container service reachable from the host; it is not required for containers
to communicate with each other. A user-defined bridge network provides
isolation plus automatic DNS resolution by container name. Prefer names over
container IP addresses because addresses can change when containers are
recreated.

The visit counter can use Redis when `REDIS_HOST` is set. Redis does not need a
host-published port because only the web container needs to reach it.

## Hands-on

1. Create a network and start Redis:

   ```bash
   docker network create visit-net
   docker run -d --name cache --network visit-net redis:8-alpine
   ```

2. Start the web app on the same network:

   ```bash
   docker run -d --name visit-counter \
     --network visit-net \
     -p 127.0.0.1:5050:5000 \
     -e REDIS_HOST=cache \
     visit-counter:v1
   ```

3. Exercise the Redis-backed counter:

   ```bash
   curl http://localhost:5050/
   curl -X POST http://localhost:5050/count
   curl http://localhost:5050/count
   ```

   The response should report `redis` as its backend.

4. Inspect network membership and name resolution:

   ```bash
   docker network inspect visit-net
   docker exec visit-counter python -c \
     'import socket; print(socket.gethostbyname("cache"))'
   ```

5. Prove the default bridge does not provide access to this isolated network:

   ```bash
   docker run --rm alpine:3.22 nslookup cache
   ```

   This lookup should fail because that container did not join `visit-net`.

6. Clean up in dependency order:

   ```bash
   docker rm -f visit-counter cache
   docker network rm visit-net
   ```

## Verify

- Explain why Redis did not need `-p 6379:6379`.
- Explain why `cache` is safer to depend on than a container IP address.
- Distinguish network isolation from host port publication.

Official reference: [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)

Next: [Module 8 — Compose Fundamentals](../08-compose-fundamentals/)
