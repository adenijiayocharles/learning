# Module 5 — Services

## Concepts

Pods are disposable — they get new IPs every time they're recreated (you saw
this in Module 4). You can't hardcode a Pod IP anywhere. A **Service** gives
a *stable* network identity to a *set* of Pods, selected by label — exactly
the same label-matching mechanism a Deployment uses.

Two Service types you'll use constantly:

- **ClusterIP** (the default) — a stable virtual IP reachable only from
  *inside* the cluster. This is how Pods talk to each other.
- **NodePort** — everything ClusterIP does, plus it opens a port
  (30000-32767 by default) on every node, reachable from outside the
  cluster. Useful for local dev; production clusters usually prefer
  Ingress (Module 9) or a cloud LoadBalancer instead.

Under the hood, `kube-proxy` (Module 2) programs networking rules on every
node so traffic to a Service's IP gets load-balanced across all matching
Pods.

Every Service also gets a **DNS name**, automatically, in the form
`<service-name>.<namespace>.svc.cluster.local` — cluster DNS (CoreDNS)
resolves it to the Service's ClusterIP. From within the same namespace you
can just use `<service-name>`.

## Hands-on

Make sure the Module 4 Deployment is still running (`kubectl get deployment
hello-app`); if not, reapply `../04-deployments/deployment.yaml`.

1. **Fill in and apply the ClusterIP Service:**

   ```bash
   # fill in the TODOs in manifests/service-clusterip-starter.yaml first
   kubectl apply -f manifests/service-clusterip-starter.yaml
   kubectl get svc hello-app
   ```

2. **Prove load-balancing and DNS work**, from inside the cluster. Launch a
   throwaway Pod with a shell:

   ```bash
   kubectl run tmp-curl --rm -it --image=curlimages/curl --restart=Never -- sh
   ```

   From inside that shell:

   ```sh
   for i in 1 2 3 4 5; do curl -s http://hello-app.default.svc.cluster.local/; echo; done
   ```

   Look at the `hostname` field in each response — it should rotate across
   your 3 replicas' Pod names, proving the Service is spreading traffic.
   Also try the short name (works because you're in the same namespace):

   ```sh
   curl -s http://hello-app/
   ```

   `exit` when done — `--rm` cleans the Pod up automatically.

3. **Fill in and apply the NodePort Service:**

   ```bash
   kubectl apply -f manifests/service-nodeport-starter.yaml
   kubectl get svc hello-app-nodeport
   ```

4. **Reach it from your host machine.** Don't try to curl the node IP
   directly — depending on your Docker backend, minikube's internal node IP
   may not be routable from your Mac. Instead, let minikube handle it:

   ```bash
   minikube service hello-app-nodeport --url
   ```

   Copy the URL it prints and `curl` it.

## Verify before moving on

- Delete and recreate one of the backing Pods (`kubectl delete pod
  <one-of-the-hello-app-pods>`) — the Service should keep working
  immediately with zero reconfiguration on your part. Confirm with
  `kubectl get endpoints hello-app` before and after.
- Explain, in one sentence, why `minikube service --url` is used instead of
  `curl $(minikube ip):<nodePort>` directly.

Next: [Module 6 — ConfigMaps & Secrets](../06-configmaps-secrets/)
