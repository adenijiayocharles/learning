# Module 6 — ConfigMaps & Secrets

## Concepts

Baking configuration into an image is a bad idea — you'd need a new image
for every environment. **ConfigMaps** and **Secrets** externalize config so
the same image works everywhere.

- **ConfigMap** — arbitrary key-value config data.
- **Secret** — structurally almost identical to a ConfigMap, but intended
  for sensitive data. **Important caveat: Secret values are only
  base64-encoded, not encrypted.** Anyone with API access to read the
  Secret can trivially decode it. Real secret management (encryption at
  rest, access control, rotation) needs more than a vanilla Secret object —
  out of scope for this course, but know the limitation exists.

Both can be consumed by a Pod two ways:

1. **As an environment variable** (`valueFrom.configMapKeyRef` /
   `secretKeyRef`) — injected once, at container **start** time.
2. **As a mounted volume** — each key becomes a *file* under the mount path,
   and (unlike env vars) the kubelet periodically syncs the mounted files
   when the underlying ConfigMap/Secret changes.

That difference in update behavior is the single most important gotcha in
this module, and you'll reproduce it below.

One more detail: when a Secret is mounted as a file, the kubelet
automatically base64-*decodes* it for you — the file contains the raw
value, not the base64 text.

## Hands-on

Run these commands from `kubernetes/06-configmaps-secrets/`. This lesson's
Deployment replaces the earlier `hello-app` Deployment because both use the
same name; `kubectl apply` updates it rather than creating a duplicate.

1. **Fill in and apply the ConfigMap and Secret:**

   ```bash
   # fill in manifests/configmap-starter.yaml and manifests/secret-starter.yaml
   kubectl apply -f manifests/configmap-starter.yaml
   kubectl apply -f manifests/secret-starter.yaml
   ```

2. **See what a Secret actually looks like at rest:**

   ```bash
   kubectl get secret hello-app-secret -o yaml
   ```

   `-o yaml` requests the full stored object rather than the usual summary
   table. Do not copy real credentials into a terminal, lesson file, or
   version-control repository.

   Note the `data` field holds base64 text, even though you wrote
   `stringData` (a convenience field — the API server encodes it for you on
   the way in). Decode it yourself to prove the point:

   ```bash
   kubectl get secret hello-app-secret -o jsonpath='{.data.API_KEY}' | base64 -d
   ```

   `-o jsonpath=...` extracts only `data.API_KEY`; quotes prevent the shell
   from interpreting the braces. `|` passes that encoded text to
   `base64 -d`, which decodes it. Add `; echo` if your prompt appears on the
   same line as the decoded value.

3. **Fill in and apply the Deployment** that wires the ConfigMap in *two
   ways at once* (as the `MESSAGE` env var, and mounted as files at
   `/etc/config`) and the Secret mounted as files at `/etc/secret`:

   ```bash
   kubectl apply -f manifests/deployment-with-config-starter.yaml
   kubectl port-forward deployment/hello-app 5050:5000
   ```

   Forwarding to a Deployment makes kubectl choose one of its Pods. Keep
   this command running and use a second terminal for the following `curl`.

   In another terminal (host port `5050` — see Module 1's note on macOS's
   AirPlay Receiver squatting on port 5000):

   ```bash
   curl -s http://localhost:5050/config | python3 -m json.tool
   ```

   `curl -s` fetches the response without a progress meter. `|` sends the
   JSON to Python's built-in `json.tool`, which indents it for readability.

   You should see `env.MESSAGE`, both files under `config_files` (including
   `GREETING_LANG`, since the whole ConfigMap was mounted, not just one
   key), and `API_KEY` under `secret_files`.

4. **Reproduce the update-propagation gotcha.** Edit the ConfigMap:

   ```bash
   kubectl edit configmap hello-app-config
   ```

   Change `MESSAGE` to something new, save and exit. Then immediately:

   ```bash
   curl -s http://localhost:5050/config | python3 -m json.tool
   ```

   `env.MESSAGE` is unchanged — it was injected once at container start and
   nothing re-injects it. Wait about a minute (kubelet's sync interval) and
   curl again: `config_files.MESSAGE` (the *mounted file*) should now show
   the new value, while `env.MESSAGE` still hasn't changed. The only way to
   pick up the new env var value is to recreate the Pods, e.g.:

   ```bash
   kubectl rollout restart deployment hello-app
   ```

   `rollout restart` deliberately replaces the Deployment's Pods. New
   containers read the current environment-variable value at startup.

## Verify before moving on

- State, without looking back, which of the two consumption methods
  (env var vs. mounted file) picks up ConfigMap edits without a Pod
  restart, and why.
- Explain why `stringData` in a Secret manifest is just a convenience, not
  a different storage mechanism from `data`.

Next: [Module 7 — Volumes & Persistent Storage](../07-volumes-storage/)
