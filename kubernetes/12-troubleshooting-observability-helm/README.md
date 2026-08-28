# Module 12 — Troubleshooting, Observability & a Taste of Helm

## Concepts

**The debugging loop.** Almost every Kubernetes problem is diagnosable with
the same small toolkit, applied in this order:

1. `kubectl get pods` — what's the `STATUS`? (`Pending`, `ImagePullBackOff`,
   `CrashLoopBackOff`, `Running` are all different problem classes.)
2. `kubectl describe pod <name>` — the `Events` section at the bottom is
   usually where the real story is (scheduling failures, pull failures,
   probe failures — all show up here).
3. `kubectl logs <name>` (add `--previous` if it already crashed) — what did
   the *application* say before it died?
4. `kubectl exec -it <name> -- sh` — if it's running but misbehaving, get
   inside and poke around.
5. `kubectl top pods` / `kubectl top nodes` — is this a resource problem?
6. `kubectl get events --sort-by=.lastTimestamp` — cluster-wide event
   timeline, useful when you're not sure which object is at fault.

Common status signatures worth recognizing on sight: `Pending` +
"Insufficient cpu/memory" in events → scheduling/resource problem;
`ImagePullBackOff`/`ErrImagePull` → wrong image name/tag or registry access;
`CrashLoopBackOff` → the container starts then exits (check logs); a Pod
stuck `Running` but never `Ready` → check probes (Module 10).

**Helm**, briefly: a package manager for Kubernetes manifests. A *chart* is
a templated bundle of manifests plus a `values.yaml` for overrides — instead
of hand-editing YAML for every environment, you parameterize it once and
override values at install time. `helm install`/`upgrade`/`rollback` wrap
the same underlying `kubectl apply` mechanics you've been using all course,
with versioning and templating layered on top.

## Hands-on

### Part 1: diagnose and fix (layered — expect to hit these one at a time)

1. **Apply the broken manifest:**

   ```bash
   kubectl apply -f manifests/broken-deployment.yaml
   kubectl get pods -l app=hello-app-broken
   ```

2. **Bug #1 — it's stuck `Pending`.** Investigate:

   ```bash
   kubectl describe pod -l app=hello-app-broken
   ```

   Find the scheduling failure in `Events`. Fix the offending field in
   `manifests/broken-deployment.yaml` (something reasonable, e.g. `64Mi`),
   then reapply:

   ```bash
   kubectl apply -f manifests/broken-deployment.yaml
   kubectl get pods -l app=hello-app-broken -w
   ```

3. **Bug #2 — now it's `ImagePullBackOff` / `ErrImageNeverPull`.**
   Investigate the same way, find the bad image reference, and fix it to
   `hello-app:v1` (the image you already built into minikube back in
   Module 2). Reapply.

4. **Bug #3 — it's `Running` and `Ready`, but something's still off.**
   Port-forward and check:

   ```bash
   kubectl port-forward deployment/hello-app-broken 5002:5000
   curl -s http://localhost:5002/config
   ```

   `env.MESSAGE` is `null` even though the manifest clearly sets an env
   var — not every bug crashes the Pod. Find the mismatch, fix it, reapply,
   and confirm `env.MESSAGE` now shows the intended text.

5. **Clean up:**

   ```bash
   kubectl delete -f manifests/broken-deployment.yaml
   ```

### Part 2: package hello-app with Helm

6. **Install Helm** if you don't have it:

   ```bash
   brew install helm
   helm version
   ```

7. **Scaffold a chart** from the standard template (don't use a third-party
   chart here — public chart catalogs like Bitnami's have had major
   availability/maintenance changes since 2025, so building your own from
   what you already understand is both more reliable and better practice):

   ```bash
   helm create hello-chart
   ```

   Look at what it generated: `Chart.yaml` (metadata), `values.yaml`
   (overridable config), `templates/` (the actual manifest templates, using
   Go templating to reference `.Values.*`).

8. **Point it at your own app.** Open `hello-chart/values.yaml` and edit the
   `image` section to:

   ```yaml
   image:
     repository: hello-app
     tag: "v1"
     pullPolicy: IfNotPresent
   ```

   and the `service` section's `port` to `5000` (the default scaffold wires
   the container's port to `service.port` under the hood — check
   `templates/deployment.yaml` if you want to see exactly how). This is
   itself a small troubleshooting exercise: if something looks off after
   install, use the Part 1 toolkit on it.

9. **Install the chart:**

   ```bash
   helm install hello-release ./hello-chart
   kubectl get all -l app.kubernetes.io/instance=hello-release
   helm status hello-release
   ```

10. **Upgrade it** to the `v2` image you built in Module 11 (rebuild it here
    if you no longer have it):

    ```bash
    helm upgrade hello-release ./hello-chart --set image.tag=v2
    kubectl rollout status deployment -l app.kubernetes.io/instance=hello-release
    ```

11. **Roll back and clean up:**

    ```bash
    helm history hello-release
    helm rollback hello-release 1
    helm list
    helm uninstall hello-release
    ```

## Verify — and reflect on the whole course

- Walk through Part 1 once more from memory, out loud, without the
  README: `get` → `describe` → `logs` → fix → reapply. This loop is the
  single most reusable skill from this entire course.
- Compare what `helm install` did under the hood to everything you did by
  hand in Modules 3-11 — same primitives, templated and versioned.

You've now covered containers, Pods, Deployments, Services, config/secrets,
storage, namespaces/resources, DNS/Ingress, probes, scaling/rollouts, and
debugging/Helm — a genuinely solid working foundation. From here, the best
next step is applying this to a real (even small) project rather than
more tutorials.
