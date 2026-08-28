# Module 3 — Pods

## Concepts

A **Pod** is the smallest deployable unit in Kubernetes — not a container. A
Pod wraps one or more containers that share networking (same IP, same
`localhost`) and storage. Almost always you'll run exactly one container per
Pod (sidecars are the exception, not covered in this course).

Key fields in a Pod spec:

- `apiVersion: v1`, `kind: Pod` — every manifest starts by declaring which
  API resource it is.
- `metadata.name` / `metadata.labels` — labels are arbitrary key-value tags
  used everywhere in Kubernetes to select groups of objects (you'll rely on
  this heavily from Module 4 onward).
- `spec.containers[].image` — which image to run.
- `spec.containers[].imagePullPolicy: IfNotPresent` — tells the kubelet
  "only pull from a registry if you don't already have this image locally."
  Required here since `hello-app:v1` only exists inside minikube's Docker
  daemon (Module 2), not in any registry.
- `spec.containers[].ports[].containerPort` — documents which port the
  container listens on (like `EXPOSE` in a Dockerfile — informational,
  doesn't publish anything by itself).

**Pods are ephemeral and not self-healing on their own.** If you delete one,
nothing recreates it — that's the job of a *controller* like a Deployment,
which is exactly why Module 4 exists.

## Hands-on

1. **Write `pod.yaml` from scratch** in this directory, using the fields
   described above: name it `hello-app`, label it `app: hello-app`, run
   `hello-app:v1` with `imagePullPolicy: IfNotPresent`, and expose
   `containerPort: 5000`. (Compare against `solution/pod.yaml` once you've
   given it a real attempt.)

   Make sure `minikube docker-env` is active in this shell (Module 2, step
   5) — otherwise the pod won't find the image.

2. **Apply it:**

   ```bash
   kubectl apply -f pod.yaml
   kubectl get pods -w
   ```

   Watch the `STATUS` go `Pending` → `ContainerCreating` → `Running`.
   `Ctrl+C` to stop watching.

3. **Inspect it:**

   ```bash
   kubectl describe pod hello-app
   kubectl logs hello-app
   kubectl exec -it hello-app -- sh
   ```

4. **Reach it from your machine:**

   ```bash
   kubectl port-forward pod/hello-app 5050:5000
   ```

   In another terminal:

   ```bash
   curl http://localhost:5050/
   ```

   (Host port `5050`, not `5000` — see the note in Module 1 about macOS's
   AirPlay Receiver squatting on port 5000.)

   `Ctrl+C` the port-forward when done.

5. **Delete it and watch what (doesn't) happen:**

   ```bash
   kubectl delete pod hello-app
   kubectl get pods
   ```

   No pod. Nothing recreated it. This is the gap Deployments fill.

## Verify before moving on

- You should be able to explain the difference between a Pod and a
  container in one sentence.
- You should understand *why* deleting the Pod didn't bring it back.

Next: [Module 4 — Deployments & ReplicaSets](../04-deployments/)
