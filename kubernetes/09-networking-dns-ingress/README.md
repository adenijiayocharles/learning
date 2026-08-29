# Module 9 — Networking II: DNS & Ingress

## Concepts

**Cluster DNS in full.** Module 5 mentioned Service DNS names briefly; here's
the full picture. CoreDNS (running inside the cluster) resolves every
Service to `<service-name>.<namespace>.svc.cluster.local`. From the *same*
namespace as the Service, the short name works. From a *different*
namespace, you need at least `<service-name>.<namespace>`, or the fully
qualified name. This is a deliberate isolation boundary — it's why
namespaces (Module 8) aren't just cosmetic.

**Ingress** is an L7 (HTTP-aware) router that sits in front of your
Services, letting you route based on hostname and path instead of exposing
a NodePort per service. An Ingress *resource* is just a routing rule — it
does nothing by itself without an **Ingress controller** actually running
in the cluster to implement it. On minikube, `minikube addons enable
ingress` installs the ingress-nginx controller, which is itself just a
Deployment + Service, no different in kind from anything you've deployed
yourself.

## Hands-on

Run these commands from `kubernetes/09-networking-dns-ingress/`. Confirm the
previous lesson reset your current namespace to `default` with
`kubectl config view --minify | grep namespace`.

### Part 1: cross-namespace DNS

1. Make sure the Module 5 ClusterIP Service (`hello-app`, port 80) still
   exists in the `default` namespace:

   ```bash
   kubectl get svc hello-app -n default
   ```

   `-n default` explicitly looks in the `default` namespace, regardless of
   the default stored in your current kubectl context.

2. From the `training` namespace (created in Module 8), curl it using the
   fully-qualified name:

   ```bash
   kubectl run tmp-curl -n training --rm -it --image=curlimages/curl --restart=Never -- \
     curl -s http://hello-app.default.svc.cluster.local/
   ```

   The trailing `\` continues the same command on the next displayed line.
   Flags before `--` configure the temporary Pod; everything after `--` is
   the `curl` command run inside it. `-n training` creates the Pod in a
   different namespace from the Service.

   Try the short name `hello-app` (without `.default...`) from the same
   namespace-scoped run command and confirm it does **not** resolve — that's
   the isolation boundary in action.

### Part 2: Ingress

3. **Enable the ingress controller** and wait for it to be ready:

   ```bash
   minikube addons enable ingress
   kubectl get pods -n ingress-nginx -w
   ```

   The controller is installed in its own `ingress-nginx` namespace. `-w`
   watches changes; wait until the controller's `READY` column shows all
   containers ready, then press `Ctrl+C`.

   `Ctrl+C` once the controller Pod shows `Running`, `1/1 Ready`.

4. **Fill in and apply the Ingress**, routing host `hello.local` to the
   `hello-app` Service on port 80:

   ```bash
   kubectl apply -f manifests/ingress-starter.yaml
   kubectl get ingress hello-app
   ```

5. **Reach it via port-forward to the ingress controller itself.** (We use
   port-forward rather than curling `$(minikube ip)` directly, because
   whether that IP is reachable from your Mac depends on which Docker
   backend minikube is using — port-forward works the same regardless, the
   same reason Module 5 used `minikube service --url` instead of a raw
   node IP.)

   ```bash
   kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8080:80
   ```

   This listens on your computer's port 8080 and forwards to port 80 of the
   controller Service. Keep it running while using a second terminal.

   In another terminal, set the `Host` header manually to simulate a real
   request to `hello.local` (no need to edit `/etc/hosts`):

   ```bash
   curl -H "Host: hello.local" http://localhost:8080/
   ```

   `-H` adds an HTTP request header. Ingress reads the `Host` header to choose
   a rule; it is independent of the `localhost` address used to connect.

   You should get the same JSON response as always — now routed through
   the Ingress controller instead of a direct Service hit.

6. **Prove hostname-based routing matters** — request a host the Ingress
   doesn't know about:

   ```bash
   curl -H "Host: nope.local" http://localhost:8080/
   ```

   This should fail (typically a 404 from the ingress-nginx default
   backend), since no Ingress rule matches that host.

## Verify before moving on

- Explain why `curl http://hello-app/` worked in Module 5 (same namespace)
  but needs the full DNS name from a different namespace.
- Explain what an Ingress *resource* actually is, and why it does nothing
  on a cluster with no ingress controller installed.

Next: [Module 10 — Health Checks: Probes](../10-health-checks-probes/)
