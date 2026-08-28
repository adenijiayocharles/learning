# Module 7 — Volumes & Persistent Storage

## Concepts

Containers' own filesystems are ephemeral by default — anything written
inside a container disappears when it's removed. Kubernetes volumes are how
you give Pods disk that outlives (or is at least separate from) the
container's own writable layer.

- **`emptyDir`** — a bare scratch directory created when the Pod starts and
  **deleted when the Pod is deleted**. It survives container *restarts*
  within the same Pod, but not Pod deletion. Good for scratch space or
  sharing files between containers in the same Pod — not for anything you
  actually want to keep.
- **PersistentVolume (PV) / PersistentVolumeClaim (PVC)** — the real
  persistence mechanism. A PVC is a *request* for storage ("I need 1Gi,
  ReadWriteOnce"); Kubernetes binds it to a PV that satisfies it. On
  minikube, a default `StorageClass` (backed by a `storage-provisioner`
  addon, enabled automatically) dynamically creates a PV for you the moment
  you create a PVC — you never have to provision one by hand.
- **Access modes** — `ReadWriteOnce` (one node can mount it read-write at a
  time — the common case for a single-replica workload), `ReadOnlyMany`,
  `ReadWriteMany` (needs a storage backend that supports it; minikube's
  default doesn't).

## Hands-on

### Part 1: emptyDir is genuinely ephemeral

1. **Fill in and apply** `manifests/pod-emptydir-starter.yaml`:

   ```bash
   kubectl apply -f manifests/pod-emptydir-starter.yaml
   kubectl port-forward pod/hello-app-emptydir 5050:5000
   ```

   In another terminal, increment the counter a few times (host port `5050`
   — see Module 1's note on macOS's AirPlay Receiver squatting on port
   5000):

   ```bash
   curl -s -X POST http://localhost:5050/count
   curl -s -X POST http://localhost:5050/count
   curl -s http://localhost:5050/count   # should show {"count": 2}
   ```

2. **Delete and recreate the Pod:**

   ```bash
   kubectl delete pod hello-app-emptydir
   kubectl apply -f manifests/pod-emptydir-starter.yaml
   kubectl port-forward pod/hello-app-emptydir 5050:5000
   ```

   ```bash
   curl -s http://localhost:5050/count   # back to {"count": 0}
   ```

   The data is gone — a fresh `emptyDir` was created along with the fresh
   Pod.

### Part 2: PVC-backed storage survives Pod recreation

3. **Fill in and apply the PVC**, then confirm it bound to a PV:

   ```bash
   kubectl apply -f manifests/pvc-starter.yaml
   kubectl get pvc hello-app-data
   ```

   `STATUS` should become `Bound` within a few seconds.

4. **Fill in and apply the Deployment** that mounts this PVC at `/data`:

   ```bash
   kubectl apply -f manifests/deployment-with-pvc-starter.yaml
   kubectl port-forward deployment/hello-app-pvc 5001:5000
   ```

   ```bash
   curl -s -X POST http://localhost:5001/count
   curl -s -X POST http://localhost:5001/count
   curl -s -X POST http://localhost:5001/count
   curl -s http://localhost:5001/count   # {"count": 3}
   ```

5. **Delete the Pod (not the Deployment, not the PVC)** and let the
   Deployment recreate it:

   ```bash
   kubectl delete pod -l app=hello-app-pvc
   kubectl get pods -l app=hello-app-pvc -w
   ```

   Once the new Pod is `Running`, port-forward again and check the count:

   ```bash
   kubectl port-forward deployment/hello-app-pvc 5001:5000
   curl -s http://localhost:5001/count   # still {"count": 3}
   ```

   The new Pod attached to the *same* underlying PV — the data survived.

## Verify before moving on

- Explain, in your own words, why the Deployment in this module is pinned
  to `replicas: 1` and what would go wrong on minikube if you scaled it up
  with the same PVC.
- Name one thing that would make the emptyDir data survive a Pod restart
  and one thing that would still lose it even with a PVC in place. (Hint
  for the second one: what happens if you `minikube delete`?)

Next: [Module 8 — Namespaces & Resource Management](../08-namespaces-resources/)
