# Module 10 — Health Checks: Probes

## Concepts

Kubernetes doesn't know your app is unhealthy unless you tell it how to
check. Three probe types, each controlling a different thing:

- **`readinessProbe`** — "is this Pod ready to receive traffic *right now*?"
  A failing readiness probe removes the Pod from every Service's endpoint
  list (Module 5) — traffic stops flowing to it — but the Pod itself is
  **not restarted**. Used for transient conditions (still warming up,
  temporarily overloaded).
- **`livenessProbe`** — "is this Pod's process still functioning, or is it
  stuck/deadlocked?" A failing liveness probe gets the container
  **restarted**. Used for conditions that generally only resolve by
  restarting.
- **`startupProbe`** — (not exercised directly here, but worth knowing)
  useful for slow-starting apps: liveness/readiness checks are suspended
  until the startup probe succeeds once, so a slow boot doesn't get
  liveness-killed before it's even up.

Key tuning fields: `initialDelaySeconds` (grace period before the first
check), `periodSeconds` (how often to check), `failureThreshold`
(consecutive failures needed before Kubernetes acts).

`hello-app` exposes `GET /healthz` (used by both probes here) and
`POST /toggle-health`, which flips a flag file so you can force a failure
on command instead of waiting for a real bug.

## Hands-on

Run these commands from `kubernetes/10-health-checks-probes/`. A result such
as `1/1` in the `READY` column means one of the Pod's one containers is ready
for Service traffic; `Running` alone does not guarantee readiness.

1. **Fill in and apply** the probe fields in
   `manifests/deployment-probes-starter.yaml`:

   ```bash
   kubectl apply -f manifests/deployment-probes-starter.yaml
   kubectl get pods -l app=hello-app
   ```

   `-l app=hello-app` filters to Pods carrying that label. Use the actual
   generated name from this output wherever the lesson shows `<pod-name>`.

   Both Pods should reach `1/1 Ready`.

2. **Force a failure on one Pod.** Pick one Pod name and port-forward
   directly to it (not the Deployment, so you affect only one replica):

   ```bash
   kubectl port-forward pod/<pod-name> 5050:5000
   ```

   In another terminal (host port `5050` — see Module 1's note on macOS's
   AirPlay Receiver squatting on port 5000):

   ```bash
   curl -X POST http://localhost:5050/toggle-health
   curl http://localhost:5050/healthz   # should now return a 500
   ```

   `-X POST` chooses the endpoint's state-changing HTTP method. The `# ...`
   text is a shell comment explaining the expected result; it is not part of
   the URL.

3. **Watch the readiness effect first** (faster — 2 failures × 3s period):

   ```bash
   kubectl get pods -w
   ```

   Within ~6-10 seconds, that Pod's `READY` column should drop to `0/1`
   while `STATUS` stays `Running`. Confirm it was pulled from the Service's
   endpoint list too:

   ```bash
   kubectl get endpoints hello-app
   ```

   An Endpoints object contains the ready Pod IP addresses behind a Service.
   A failing Pod disappearing here is why the Service stops sending it
   traffic. Newer clusters may also expose the same data as EndpointSlices.

   (Only relevant if you still have the Module 5/6 Service around — if not,
   the readiness signal is still visible directly in `kubectl get pods`.)

4. **Watch the liveness effect** (slower — 3 failures × 5s period, plus the
   5s initial delay): keep watching `kubectl get pods -w`. Once the
   threshold is hit, you'll see `RESTARTS` increment for that Pod. Because
   restarting the container also clears its `/tmp/unhealthy` flag file, the
   Pod comes back healthy immediately and stabilizes at `1/1 Ready` again.

5. **Confirm what happened via events:**

   ```bash
   kubectl describe pod <same-pod-name>
   ```

   Look in the `Events` section near the bottom for `Unhealthy` warnings
   from both probes and a `Killing` event from the liveness failure.

## Verify before moving on

- Explain, without looking back, which probe type removes a Pod from
  Service traffic vs. which one restarts the container.
- If you set `initialDelaySeconds: 0` on a liveness probe for an app that
  genuinely takes 30 seconds to boot, what would go wrong, and which probe
  type exists specifically to prevent that?

Next: [Module 11 — Scaling & Rolling Updates](../11-scaling-rolling-updates/)
