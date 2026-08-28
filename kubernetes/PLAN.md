# Kubernetes Foundational Learning Curriculum

## Context

The user wants to learn Kubernetes from scratch (complete beginner — no prior Docker/K8s/YAML experience) with the goal of general day-to-day working knowledge, not certification prep. They created an empty `kubernetes/` directory for this. They asked for a hands-on-labs format: structured notes paired with runnable exercises against a real local cluster, not pure theory and not unguided exercises.

The machine already has `kubectl`, `minikube`, and `docker` installed (no `kind`), so `minikube` is the local cluster used throughout. This plan builds a 12-module curriculum, each module teaching one concept and having the learner apply it against a running cluster.

## Design

One shared demo app (`apps/hello-app/`) is used across the entire course instead of a different toy example per module, so each module's diff stays focused on the Kubernetes concept rather than on new application code. It's a small Flask app exposing:
- `GET /` — returns hostname + env vars `APP_VERSION`/`MESSAGE` (proves which replica/pod answered)
- `GET /healthz` + `POST /toggle-health` — flips a health flag on command, for probe demos
- `GET /config` — dumps env vars and file contents from `/etc/config` and `/etc/secret` if mounted
- `GET /count`, `POST /count` — persists a counter to `/data/count.txt`, for volume-persistence demos

Each module folder contains:
- `README.md` — short concept explanation, then a numbered hands-on procedure with exact commands and what to observe/verify
- `manifests/` — starter YAML with `# TODO` comments for the new field(s) being taught (used from Module 5 onward, where YAML syntax itself is the new/finicky part)
- `solution/` — completed reference manifest to diff against after attempting

Modules 3 and 4 (first Pod, first Deployment) have the learner write YAML from scratch guided by the README, with only a solution file for reference — the repetition of writing it themselves is the point early on.

## Directory structure to create

```
kubernetes/
├── README.md                                   # course index, prerequisites, how each module works
├── apps/hello-app/
│   ├── app.py                                  # Flask app, all endpoints above
│   ├── requirements.txt                        # Flask only
│   ├── Dockerfile.starter                      # TODO-commented skeleton (Module 1 exercise)
│   └── Dockerfile.solution                     # completed reference
├── 01-docker-fundamentals/README.md
├── 02-k8s-architecture-first-cluster/README.md
├── 03-pods/{README.md, solution/pod.yaml}
├── 04-deployments/{README.md, solution/deployment.yaml}
├── 05-services/{README.md, manifests/service-clusterip-starter.yaml, manifests/service-nodeport-starter.yaml, solution/*.yaml}
├── 06-configmaps-secrets/{README.md, manifests/{configmap,secret,deployment-with-config}-starter.yaml, solution/*.yaml}
├── 07-volumes-storage/{README.md, manifests/{pod-emptydir,pvc,deployment-with-pvc}-starter.yaml, solution/*.yaml}
├── 08-namespaces-resources/{README.md, manifests/{namespace,deployment-with-limits}-starter.yaml, solution/*.yaml}
├── 09-networking-dns-ingress/{README.md, manifests/ingress-starter.yaml, solution/ingress.yaml}
├── 10-health-checks-probes/{README.md, manifests/deployment-probes-starter.yaml, solution/deployment-probes.yaml}
├── 11-scaling-rolling-updates/{README.md, manifests/hpa-starter.yaml, solution/hpa.yaml}
└── 12-troubleshooting-observability-helm/{README.md, manifests/broken-deployment.yaml}   # no solution — the fix is the exercise
```

## Module sequence

1. **Docker Fundamentals** — containers vs VMs, images/layers, Dockerfile. Learner completes `Dockerfile.starter`, builds/runs it, inspects with `docker ps/logs/exec`, observes layer-cache behavior on rebuild.
2. **K8s Architecture & First Cluster** — control plane/node overview, why K8s over plain Docker, YAML primer. `minikube start`, `kubectl cluster-info/get nodes`, `minikube addons enable metrics-server`, and the key local-image workflow: `eval $(minikube docker-env)` + rebuild `hello-app:v1` so no registry is needed all course.
3. **Pods** — Pod anatomy, `imagePullPolicy: IfNotPresent`, ephemeral nature. Learner writes `pod.yaml` from scratch, applies, inspects (`describe`, `logs`, `exec`, `port-forward`), deletes it and observes it does not come back.
4. **Deployments & ReplicaSets** — ownership chain, desired vs actual state, self-healing. Learner writes `deployment.yaml` (3 replicas), deletes one pod to watch it get recreated, scales, edits live.
5. **Services** — ClusterIP vs NodePort, label selectors, Service DNS. Apply both starter Services against the Module 4 Deployment, curl via DNS name from a throwaway pod to see load-balancing, and via `minikube service --url` for NodePort.
6. **ConfigMaps & Secrets** — externalizing config, env-var vs volume-mount injection, Secrets are base64 not encrypted (explicit caveat — kubelet auto-decodes on mount, so the file content is plaintext). Wire the ConfigMap in **two ways at once** (as an env var AND mounted as a file at `/etc/config`) and the Secret mounted as a file at `/etc/secret`; demonstrate the gotcha that after editing the ConfigMap, the env var in already-running pods does NOT update, while the mounted file does (after kubelet's periodic sync, ~1 min).
7. **Volumes & Persistent Storage** — `emptyDir` vs PVC/PV/StorageClass. Show emptyDir data lost on pod delete, then PVC-backed `/data` surviving pod recreation via the `/count` endpoint.
8. **Namespaces & Resource Management** — namespaces as logical partitions, requests/limits, OOMKill vs throttling. Create a `training` namespace, redeploy into it, apply a deliberately tiny memory limit (below the Flask process's baseline footprint, e.g. 10-16Mi) so the container reliably OOMKills on startup — observed via `kubectl describe pod` showing `OOMKilled` / `CrashLoopBackOff` (the app has no memory-scaling behavior, so this is done via the limit itself, not by generating load).
9. **Networking II: DNS & Ingress** — CoreDNS naming (`svc.ns.svc.cluster.local`), cross-namespace calls, Ingress as L7 routing. Cross-namespace curl test, then `minikube addons enable ingress` + apply Ingress + reach it via `kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80` and `curl -H "Host: hello.local" http://localhost:8080/` (port-forward is used instead of hitting `$(minikube ip)` directly, since on macOS the node IP isn't reliably routable from the host depending on the Docker backend in use — port-forward works identically regardless of driver, consistent with why Module 5 already uses `minikube service --url` rather than a raw IP for NodePort access).
10. **Health Checks: Probes** — liveness vs readiness vs startup, what each actually controls. Wire both probes to `/healthz`, use `/toggle-health` to force failures, watch readiness removal vs liveness restart in `kubectl get pods -w` / `describe`.
11. **Scaling & Rolling Updates** — HPA mechanics, rolling update strategy, rollout commands. Apply HPA, generate load to trigger scale-up/down; separately bump `APP_VERSION`, build `hello-app:v2`, `kubectl set image`, watch rollout, then `rollout undo`.
12. **Troubleshooting, Observability & Helm taste** — the describe/logs/events/exec/top debug loop; Helm as templated manifests. Learner diagnoses and fixes a deliberately broken `broken-deployment.yaml` (bad image tag + missing required env var + oversized resource request) using only kubectl introspection; then `helm create hello-chart` to templatize the hello-app Deployment/Service the learner already built, and runs `helm install`/`upgrade --set`/`rollback`/`uninstall` against it. (Using a self-authored chart instead of a third-party one like `bitnami/nginx` avoids depending on Bitnami's public chart images, which Bitnami migrated to an unmaintained "legacy" repo in August 2025 that isn't guaranteed to keep working — confirmed via web search since this course needs to hold up over time.)

## Verification

- After scaffolding, spot-check a few modules end-to-end on the actual machine: run Module 1's Docker build/run, Module 2's `minikube start` + docker-env rebuild, and Module 3's Pod apply/curl, to confirm the exercises work as written before considering the course "done."
- Confirm `kubectl apply --dry-run=client -f` succeeds on every solution manifest (catches YAML/schema mistakes without needing a live cluster for all of them).
- Read back each README to make sure command sequences are copy-pasteable in order (no missing prior steps like namespace context or docker-env re-eval in new shells).
