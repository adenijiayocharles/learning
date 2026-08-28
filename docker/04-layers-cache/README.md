# Module 4 — Layers, Cache & Image History

## Concepts

Images are composed of content-addressed layers. During a rebuild, Docker can
reuse cached results until an instruction or one of its inputs changes. Once a
layer changes, later dependent layers must be rebuilt. Put stable dependency
files before frequently changed application source so ordinary code edits do
not reinstall every dependency.

Tags such as `visit-counter:v1` are mutable names pointing at image content;
they are not immutable copies. Rebuilding with the same tag moves that tag to
the new result.

## Hands-on

Run these commands from `docker/apps/visit-counter`.

1. Build with plain progress so cache decisions are visible:

   ```bash
   docker build --progress=plain -t visit-counter:cache-demo .
   docker build --progress=plain -t visit-counter:cache-demo .
   ```

   The second build should reuse every eligible step.

2. Change only the default message in `app.py`, rebuild, and observe that the
   dependency installation remains cached:

   ```bash
   docker build --progress=plain -t visit-counter:cache-demo .
   ```

3. Inspect the resulting history:

   ```bash
   docker image history visit-counter:cache-demo
   docker image inspect visit-counter:cache-demo --format '{{.Id}}'
   ```

4. Temporarily move `COPY app.py .` before dependency installation and rebuild.
   An app-only edit now invalidates more work. Restore the Dockerfile to the
   ordering in `../../04-layers-cache/solution/Dockerfile` afterward.

5. Force a clean build only to compare behavior:

   ```bash
   docker build --no-cache --progress=plain -t visit-counter:no-cache .
   ```

   `--no-cache` skips reusable build cache, but it does not automatically fetch
   a newer base image; `--pull` is the separate option for that.

## Verify

- Explain which input invalidates the `COPY requirements.txt` layer.
- Explain why instruction ordering changes rebuild time.
- Explain why a tag alone does not guarantee identical image content.

Official references: [Build cache](https://docs.docker.com/build/cache/), [Cache optimization](https://docs.docker.com/build/cache/optimize/)

Next: [Module 5 — Runtime Configuration, Processes & Ports](../05-runtime-configuration/)
