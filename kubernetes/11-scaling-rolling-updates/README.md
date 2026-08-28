# Module 11 — Scaling & Rolling Updates

## Concepts

**HorizontalPodAutoscaler (HPA)** watches a metric (CPU utilization here)
and adjusts `replicas` on a target Deployment automatically, between a
floor and ceiling you define. It needs two things to function:

1. `metrics-server` installed (Module 2) — it's the source of the actual
   utilization numbers.
2. `resources.requests.cpu` set on the target container — utilization is
   calculated as *actual usage ÷ requested amount*, so without a request,
   there's no denominator to compute a percentage from.

**Rolling updates.** By default, a Deployment update uses the
`RollingUpdate` strategy: it creates new-version Pods and terminates
old-version ones gradually (governed by `maxSurge`/`maxUnavailable`,
defaulting to 25% each), rather than replacing everything at once. Combined
with readiness probes (Module 10), traffic only shifts to new Pods once
they report ready — this is what makes zero-downtime deploys possible.
`kubectl rollout` gives you visibility and control over this process:
`status` (watch it happen), `history` (past revisions), `undo` (roll back).

## Hands-on

### Part 1: HPA and load-based autoscaling

1. **Make sure `hello-app` is running in the `default` namespace** with a
   CPU request set (needed for HPA math). If you still have the Module 4/10
   Deployment around, just add resource settings to it:

   ```bash
   kubectl config set-context --current --namespace=default
   kubectl set resources deployment hello-app --requests=cpu=50m --limits=cpu=200m
   ```

   If no `hello-app` Deployment exists in `default`, reapply
   `../04-deployments/solution/deployment.yaml` first, then run the command
   above.

2. **Fill in and apply the HPA:**

   ```bash
   kubectl apply -f manifests/hpa-starter.yaml
   kubectl get hpa hello-app -w
   ```

   Leave this running in its own terminal — you'll watch `REPLICAS` and
   `TARGETS` (current vs. target CPU%) change live.

3. **Generate load**, in another terminal, against the ClusterIP Service
   from Module 5 (`hello-app`, port 80):

   ```bash
   kubectl run load-generator --image=busybox:1.36 --restart=Never -it --rm -- \
     /bin/sh -c "while true; do wget -q -O- http://hello-app.default.svc.cluster.local/; done"
   ```

   Watch the HPA terminal — within a minute or two, `TARGETS` should climb
   and `REPLICAS` should scale up toward `maxReplicas`.

4. **Stop the load** (`Ctrl+C` the load-generator command — `--rm` cleans it
   up) and keep watching the HPA. Scale-down is deliberately conservative
   (a stabilization window, several minutes by default) to avoid
   flapping — be patient.

### Part 2: rolling update and rollback

5. **Ship a v2.** Bump `APP_VERSION`'s default in
   `../apps/hello-app/app.py`, e.g. from `"v1"` to `"v2"`. Rebuild (make
   sure `minikube docker-env` is still active in this shell — Module 2):

   ```bash
   cd ../apps/hello-app
   docker build -t hello-app:v2 .
   cd ../../11-scaling-rolling-updates
   ```

6. **Trigger the rollout:**

   ```bash
   kubectl set image deployment/hello-app hello-app=hello-app:v2
   kubectl rollout status deployment/hello-app
   ```

7. **Watch old and new versions briefly coexist**, in another terminal,
   while the rollout is in progress:

   ```bash
   for i in $(seq 1 20); do
     kubectl run tmp-curl-$i --rm -i --image=curlimages/curl --restart=Never -- \
       curl -s http://hello-app.default.svc.cluster.local/ 2>/dev/null | grep app_version
   done
   ```

   With only a couple of replicas this window may be short — if you missed
   it, `kubectl rollout history deployment/hello-app` still proves it
   happened.

8. **Roll back:**

   ```bash
   kubectl rollout undo deployment/hello-app
   kubectl rollout status deployment/hello-app
   kubectl port-forward deployment/hello-app 5050:5000 &
   curl -s http://localhost:5050/   # app_version should be back to v1
   kill %1                          # stop the background port-forward
   ```

## Verify before moving on

- Explain why the HPA couldn't compute anything before you set a CPU
  `request` on the Deployment.
- Explain why scale-up and scale-down aren't symmetric in responsiveness,
  and why that asymmetry is a reasonable default.

Next: [Module 12 — Troubleshooting, Observability & Helm](../12-troubleshooting-observability-helm/)
