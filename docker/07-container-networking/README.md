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

Every container attached to a network receives an interface and an address on
that network. Docker's embedded DNS maps container or service names to those
changing addresses. Network attachment controls container-to-container
reachability; port publishing separately controls traffic entering from the host.

### Network types and when to use them

Docker networks use a **driver**, which determines how container traffic is
connected and isolated.

| Driver or network | Use it when | Important trade-off |
| --- | --- | --- |
| User-defined `bridge` | Containers on one Docker host need private communication and name-based DNS; this is the normal choice for local applications | It does not span multiple Docker hosts; publish only the ports clients outside the network need |
| Default `bridge` | Running a quick standalone container with no special networking needs | It lacks the convenient isolation and automatic name-based discovery of a user-defined bridge, so avoid it for multi-container applications |
| `host` | A trusted workload needs the host's network directly, commonly for performance or software that must observe host networking | It removes network isolation, can cause host-port conflicts, and has platform limitations |
| `none` | A container must have no external or container-to-container network access | The container has only its loopback interface, so it cannot call network services |
| `overlay` | Swarm services or containers on different Docker hosts must communicate | It requires multi-host orchestration and is unnecessary for a single-host application |
| `macvlan` | A legacy or specialized workload must appear as a separate physical device with its own MAC address on the local network | It requires careful physical-network configuration and is not the usual application default |
| `ipvlan` | Containers need direct underlay/VLAN integration but the network should see fewer MAC addresses than with `macvlan` | It is an advanced choice that requires control of addressing and network infrastructure |

Start with a **user-defined bridge** for a multi-container application on one
host. Move to another driver only when the deployment topology or network
integration creates a specific requirement. A network driver controls how a
container connects; `-p` or `--publish` separately controls which container
ports are exposed through the Docker host.

## Command and flag guide

- `docker network create NAME` creates a user-defined bridge network by default;
  add `--driver DRIVER` only when another network type is required.
  `docker network inspect NAME` shows its configuration and attached containers,
  and `docker network rm NAME` deletes an unused network.
- `--network NAME` connects the new container to that network, where containers
  can resolve one another by name.
- `docker exec` is reused here to run a DNS check inside the web container.

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
- Choose a user-defined bridge, `host`, `none`, or `overlay` network for a given
  scenario and explain the trade-off.

Official references: [Docker network drivers](https://docs.docker.com/engine/network/drivers/), [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)

Next: [Module 8 — Compose Fundamentals](../08-compose-fundamentals/)
