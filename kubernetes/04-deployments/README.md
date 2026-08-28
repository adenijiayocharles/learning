# Module 4 — Deployments & ReplicaSets

## Concepts

A **Deployment** is a controller that manages Pods for you declaratively.
You describe desired state ("3 replicas of this Pod template"), and the
Deployment's control loop continuously reconciles reality to match.

The ownership chain: **Deployment → ReplicaSet → Pods**.

- You create a Deployment.
- The Deployment creates a **ReplicaSet**, whose only job is "ensure exactly
  N Pods matching this template exist."
- The ReplicaSet creates the actual **Pods**.

(Deployments delegate to ReplicaSets specifically so that rolling updates —
Module 11 — can keep an old ReplicaSet around briefly while a new one spins
up, enabling zero-downtime rollout and rollback.)

The glue holding this chain together is `spec.selector.matchLabels`, which
must match `spec.template.metadata.labels` — this is how the Deployment
knows which Pods belong to it.

## Hands-on

1. **Write `deployment.yaml`** in this directory: a Deployment named
   `hello-app`, `replicas: 3`, selector matching label `app: hello-app`, and
   a Pod template using `hello-app:v1` (same container spec as Module 3, now
   nested under `spec.template.spec`). Add one env var, `APP_VERSION: "v1"`
   — you'll use this later to see version changes reflected in real time.

   (Check `solution/deployment.yaml` once you've tried it yourself.)

2. **Apply it and see the full chain:**

   ```bash
   kubectl apply -f deployment.yaml
   kubectl get deployments,replicasets,pods --show-labels
   ```

   Notice the ReplicaSet's name is `hello-app-<hash>` and each Pod's name is
   `hello-app-<hash>-<random>` — each level's name embeds its parent's.

3. **Kill self-healing in action.** Pick one Pod name from the list above
   and delete it:

   ```bash
   kubectl delete pod <pod-name>
   kubectl get pods -w
   ```

   Unlike Module 3, a replacement Pod appears within seconds — the
   ReplicaSet controller noticed "2 exist, 3 are wanted" and fixed it.

4. **Scale imperatively:**

   ```bash
   kubectl scale deployment hello-app --replicas=5
   kubectl get pods
   ```

5. **Edit live** and watch reconciliation happen in real time:

   ```bash
   kubectl edit deployment hello-app
   ```

   Change `replicas: 5` back to `replicas: 3`, save and exit (this opens
   your `$EDITOR` — usually `vi`; save with `:wq`). Watch
   `kubectl get pods -w` in another terminal terminate the extra two.

## Verify before moving on

- Run `kubectl describe replicaset <name>` — find the line showing which
  Deployment "owns" it.
- Explain why the Deployment creates a ReplicaSet instead of managing Pods
  directly (hint: think ahead to what a rolling update needs to keep around
  temporarily).

Next: [Module 5 — Services](../05-services/)
