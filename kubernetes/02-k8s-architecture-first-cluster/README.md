# Module 2 — Kubernetes Architecture & Your First Cluster

## Concepts

**Why Kubernetes over plain `docker run`?** Docker alone runs containers on
one machine and doesn't know or care if they die, need to scale, or need to
talk to each other across hosts. Kubernetes adds a control system on top:
you declare the state you *want* (e.g. "3 replicas of hello-app, always
running"), and it continuously works to make reality match — restarting
crashed containers, rescheduling them if a node dies, spreading them across
machines, load-balancing traffic between them.

**Cluster architecture**, at a glance:

- **Control plane** (the "brain," runs on control-plane node(s)):
  - `kube-apiserver` — the front door. Every `kubectl` command, and every
    internal component, talks to the cluster *only* through this REST API.
  - `etcd` — the cluster's database. Stores all state (what you asked for,
    what's currently running).
  - `kube-scheduler` — decides which node a new Pod should run on.
  - `kube-controller-manager` — runs the reconciliation loops (e.g. "a
    Deployment wants 3 replicas but only 2 exist — create one").
- **Worker nodes** (where your containers actually run):
  - `kubelet` — the agent on each node that talks to the API server and
    makes sure the containers it's told to run are actually running.
  - `kube-proxy` — programs networking rules so Services (Module 5) work.
  - **Container runtime** — actually pulls images and runs containers
    (containerd, in minikube's case).

`kubectl` is just a client that sends requests to `kube-apiserver`. It has no
special powers beyond what that API allows.

**minikube** runs a whole single-node cluster (control plane + worker,
combined) inside one Docker container (or VM) on your machine — perfect for
learning, not for production.

**A YAML primer**, since every manifest in this course is YAML:

```yaml
key: value          # a scalar field
nested:
  key: value         # indentation (spaces, not tabs) = nesting
list:
  - item1            # a "-" prefix marks a list item
  - item2
```

That's genuinely most of it — Kubernetes manifests are just deeply nested
maps and lists of the above.

## Hands-on

Run these commands from `kubernetes/02-k8s-architecture-first-cluster/`.

1. **Start your cluster:**

   ```bash
   minikube start
   minikube status
   ```

   `start` creates or resumes the local cluster. `status` reports whether
   its host, kubelet, API server, and kubeconfig connection are ready.

2. **Talk to it with kubectl:**

   ```bash
   kubectl cluster-info
   kubectl get nodes -o wide
   ```

   `cluster-info` prints control-plane addresses. `get nodes` lists machines
   in the cluster; `-o wide` adds details such as internal IP and runtime.

   Notice there's only one node — it's playing both control-plane and
   worker roles.

3. **Enable metrics-server now** — you won't need it until Modules 8 and 11,
   but it takes a minute to become ready, so turn it on early:

   ```bash
   minikube addons enable metrics-server
   ```

   An addon is an optional cluster component. This command installs and
   enables metrics-server so later `kubectl top` and autoscaling exercises
   can read CPU and memory usage.

4. *(Optional)* Open the visual dashboard:

   ```bash
   minikube dashboard
   ```

5. **The most important gotcha in this whole course: local images.**
   Minikube runs its own internal Docker daemon, completely separate from
   the one you used in Module 1. If you `docker build` normally, minikube's
   cluster will never see that image, and it'll try (and fail) to pull it
   from a public registry. To avoid needing a registry entirely, point your
   shell's `docker` CLI *at minikube's* daemon instead:

   ```bash
   eval $(minikube docker-env)
   ```

   `minikube docker-env` prints environment-variable assignments. `$(...)`
   captures that text and `eval` applies it to the current shell. Because
   this changes only the current shell, run Docker build commands in this
   same terminal.

   This only affects your **current terminal session** — you'll need to
   re-run it in every new shell you use for this course (or use
   `minikube docker-env` output to check whether it's already set).

6. **Rebuild the image inside minikube:**

   ```bash
   cd ../apps/hello-app
   docker build -t hello-app:v1 .
   docker images | grep hello-app
   ```

   `|` sends the image list into `grep`, which keeps only lines containing
   `hello-app`. No output usually means the image was built in a different
   Docker daemon or under a different name.

   That image now lives inside minikube's cluster, ready for Kubernetes to
   run it — no push, no registry, no `imagePullPolicy` headaches as long as
   you remember to rebuild here (with `docker-env` active) whenever you
   change the app.

## Verify before moving on

- `kubectl get nodes` should show one `Ready` node.
- `docker images` (with `minikube docker-env` active) should list
  `hello-app:v1`.

Next: [Module 3 — Pods](../03-pods/)
