# Kubernetes — Foundational Curriculum

A hands-on, 12-module course for learning Kubernetes from zero to solid working
knowledge. Every module teaches one concept and has you apply it against a
real local cluster — no slides, no toy examples that don't run.

See [`PLAN.md`](./PLAN.md) for the original design rationale. Prefer reading
in a browser? Open [`index.html`](./index.html) for a navigable version of
this course with progress tracking.

## Before you start

You do not need prior Kubernetes knowledge. You should be comfortable opening
a terminal, changing folders with `cd`, and editing a text file. The course
explains the Kubernetes and Docker commands it uses.

Install these tools before Module 1, then confirm each command prints a version:

- `docker` — container runtime
- `minikube` — local Kubernetes cluster
- `kubectl` — the Kubernetes CLI

```bash
docker --version
minikube version
kubectl version --client
```

Docker must also be running. On macOS or Windows, open Docker Desktop before
starting. If a command fails, read the error before continuing; later lessons
often depend on the resource created by the current step.

No `kind`, no cloud account, no registry — everything runs locally, and
container images are built straight into minikube's own Docker daemon (see
Module 2).

## How each module works

Every module folder contains:

- **`README.md`** — a short concept explanation, then a numbered hands-on
  procedure with exact commands and what you should observe.
- **`manifests/`** (from Module 5 onward) — starter YAML files with `# TODO`
  comments marking the fields you need to fill in. Modules 3–4 have you write
  the YAML from scratch instead — that repetition is the point early on.
- **`solution/`** — the completed reference manifest. Try the exercise first;
  only diff against this if you're stuck or want to double-check yourself.

Work through the modules in order — later ones assume you've built (and left
running, or know how to rebuild) the resources from earlier ones.

## How to read the exercises

- Run commands from the module directory unless the lesson says otherwise.
  A line beginning with `cd` changes your current directory.
- Do not type placeholders literally. Replace text such as `<pod-name>` with
  a real value from the preceding `kubectl get pods` command, and omit the
  angle brackets.
- Lines beginning with `#` are comments for you, not commands you must run.
- A trailing `\` continues one command onto the next displayed line.
- `Ctrl+C` stops a command that is watching, serving, or forwarding a port;
  it does not undo resources already created in Kubernetes.
- Kubernetes accepts both long and short resource names: `pods`/`pod`/`po`,
  `services`/`service`/`svc`, and `deployments`/`deployment`/`deploy`.

The flags used most often are:

- `-f <file>`: read the desired resource from a YAML file.
- `-n <namespace>`: target a namespace instead of the current default.
- `-l key=value`: select objects by label.
- `-o <format>`: choose an output format; `wide` adds columns and `yaml`
  prints the full object.
- `-w`: keep watching and print changes until you press `Ctrl+C`.
- `-it`: attach an interactive terminal to a container.
- `--`: stop parsing `kubectl` flags; everything after it is the command to
  run inside the container.

## Shared demo app

All 12 modules use one app: [`apps/hello-app`](./apps/hello-app) — a tiny
Flask service with just enough surface area to demonstrate every concept in
the course (env-based config, a togglable health check, a file-backed
counter). You'll build its container image once in Module 1 and reuse it
(and a `v2` variant in Module 11) throughout.

## Modules

| # | Module | Concept |
|---|--------|---------|
| 1 | [Docker Fundamentals](./01-docker-fundamentals/) | Containers, images, Dockerfiles |
| 2 | [K8s Architecture & First Cluster](./02-k8s-architecture-first-cluster/) | Control plane/nodes, minikube, YAML basics |
| 3 | [Pods](./03-pods/) | The smallest deployable unit |
| 4 | [Deployments & ReplicaSets](./04-deployments/) | Declarative, self-healing workloads |
| 5 | [Services](./05-services/) | Stable networking for a set of Pods |
| 6 | [ConfigMaps & Secrets](./06-configmaps-secrets/) | Externalizing configuration |
| 7 | [Volumes & Persistent Storage](./07-volumes-storage/) | Ephemeral vs. persistent data |
| 8 | [Namespaces & Resource Management](./08-namespaces-resources/) | Isolation, requests/limits |
| 9 | [Networking II: DNS & Ingress](./09-networking-dns-ingress/) | Cluster DNS, L7 routing |
| 10 | [Health Checks: Probes](./10-health-checks-probes/) | Liveness, readiness, startup |
| 11 | [Scaling & Rolling Updates](./11-scaling-rolling-updates/) | HPA, zero-downtime deploys |
| 12 | [Troubleshooting & Helm](./12-troubleshooting-observability-helm/) | Debugging loop, packaging with Helm |

## Cleanup

When you're done with the whole course:

```bash
minikube delete
```

This tears down the entire local cluster (VM/container, volumes, everything
built during the course). Nothing here touches anything outside minikube.
