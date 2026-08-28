# Module 8 — Namespaces & Resource Management

## Concepts

**Namespaces** are logical partitions within one cluster — a way to
separate workloads (by team, environment, or in this case, "training
exercises") without needing separate clusters. Most resource types
(Pods, Deployments, Services, ConfigMaps...) are namespace-scoped; a few
(Nodes, PersistentVolumes, Namespaces themselves) are cluster-wide. Every
`kubectl` command implicitly targets a namespace — `default` unless you
say otherwise with `-n <namespace>` or by changing your context's default.

**Resource requests and limits**, set per-container:

- **`requests`** — what the scheduler guarantees is available before it
  will place a Pod on a node. This is also what the HPA (Module 11) uses to
  calculate CPU utilization percentage.
- **`limits`** — the hard ceiling. Behavior differs by resource type:
  - **CPU**: throttled if it exceeds the limit — the container slows down,
    doesn't crash.
  - **Memory**: the container is **OOMKilled** (forcibly terminated) if it
    exceeds the limit — there's no "throttling" equivalent for memory.

This module deliberately sets a memory limit *below* what a Python/Flask
process needs, specifically to trigger and observe an OOMKill.

## Hands-on

1. **Create the `training` namespace:**

   ```bash
   # fill in manifests/namespace-starter.yaml
   kubectl apply -f manifests/namespace-starter.yaml
   kubectl get namespaces
   ```

2. *(Optional but convenient)* switch your shell's default namespace so you
   don't have to type `-n training` on every command:

   ```bash
   kubectl config set-context --current --namespace=training
   ```

   You can always check which namespace you're pointed at with
   `kubectl config view --minify | grep namespace`, and switch back later
   with `kubectl config set-context --current --namespace=default`.

3. **Fill in and apply the intentionally under-provisioned Deployment:**

   ```bash
   kubectl apply -f manifests/deployment-with-limits-starter.yaml
   kubectl get pods -w
   ```

   Watch for `CrashLoopBackOff`.

4. **Confirm it's actually an OOMKill:**

   ```bash
   kubectl describe pod -l app=hello-app
   ```

   Look for `Last State: Terminated`, `Reason: OOMKilled` in the output.

5. **Check live resource usage** (needs the `metrics-server` addon from
   Module 2):

   ```bash
   kubectl top pods
   ```

   If the Pod is crash-looping too fast to catch a metrics sample, that's
   expected — it's dying almost immediately after starting.

6. **Fix it.** Edit `manifests/deployment-with-limits-starter.yaml` (or just
   `kubectl edit deployment hello-app`) and raise both `requests.memory` and
   `limits.memory` to something realistic, e.g. `64Mi`. Reapply if you
   edited the file:

   ```bash
   kubectl apply -f manifests/deployment-with-limits-starter.yaml
   kubectl get pods -w
   ```

   It should now reach and stay in `Running`, `1/1 Ready`.

7. **Reset your namespace context** before moving to Module 9, which needs
   resources in `default`:

   ```bash
   kubectl config set-context --current --namespace=default
   ```

## Verify before moving on

- Explain the difference in what happens when a container exceeds its CPU
  limit vs. its memory limit.
- Explain why `requests` matters even when a node has plenty of free
  capacity right now (hint: what is the scheduler trying to prevent for the
  *future*?).

Next: [Module 9 — Networking II: DNS & Ingress](../09-networking-dns-ingress/)
