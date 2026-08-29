# Module 1 — Docker Fundamentals

Kubernetes orchestrates containers — it doesn't create them. Before touching
Kubernetes, you need a working mental model of what a container actually is,
and enough Docker literacy to build one.

## Concepts

- **VM vs. container**: a VM virtualizes hardware and runs a full guest OS
  kernel; a container is just an isolated process on the *host's* kernel
  (via Linux namespaces + cgroups). That's why containers start in
  milliseconds and are far lighter than VMs.
- **Image vs. container**: an *image* is a read-only, layered filesystem
  snapshot plus metadata (entrypoint, exposed ports, env). A *container* is a
  running instance of an image with a writable layer on top. One image, many
  containers.
- **Layers & caching**: each `Dockerfile` instruction (`FROM`, `COPY`, `RUN`,
  ...) produces a cached layer. Docker reuses a layer unmodified if nothing
  above it in the file changed *and* its inputs are identical — this is why
  instruction **order** matters (see the exercise below).
- **Dockerfile basics**: `FROM` (base image), `WORKDIR` (default directory
  for subsequent instructions), `COPY` (host → image), `RUN` (executes at
  *build* time), `EXPOSE` (documentation of the listening port — doesn't
  actually publish it), `CMD` (the process that runs at *container start*
  time).
- **Port mapping**: a container's network is isolated from the host by
  default; `docker run -p <host-port>:<container-port>` punches a hole
  through to reach it.

## Hands-on

Start in `kubernetes/01-docker-fundamentals/`. All commands below then run
from the shared `kubernetes/apps/hello-app/` directory.

```bash
cd ../apps/hello-app
```

If your terminal starts at the repository root, this command moves you into
the shared application directory. Use `pwd` to print your current directory
and `ls` to list its files whenever you are unsure where you are.

1. **Complete the Dockerfile.** Open `Dockerfile.starter` and fill in each
   `# TODO`. You have everything you need from the Concepts section above
   and `app.py` (which listens on port 5000). Save your work as `Dockerfile`:

   ```bash
   cp Dockerfile.starter Dockerfile
   # edit Dockerfile to fill in the TODOs
   ```

2. **Build the image:**

   ```bash
   docker build -t hello-app:v1 .
   ```

   `docker build` creates an image from a Dockerfile. `-t hello-app:v1` gives
   it the name `hello-app` and tag `v1`; the final `.` means "send the current
   directory to Docker as the build context."

   If you're stuck, compare against `Dockerfile.solution` — but try first.

3. **Run it and hit it:**

   ```bash
   docker run -d -p 5050:5000 --name hello-app-test hello-app:v1
   curl http://localhost:5050/
   ```

   You should get back JSON with a `hostname`, `app_version`, and `message`.

   Here, `-d` runs in the background, `-p 5050:5000` maps host port 5050 to
   container port 5000, and `--name` assigns a memorable container name.
   `curl` makes an HTTP request and prints the response.

   > **Why port 5050 and not 5000?** On macOS, port 5000 is usually already
   > claimed by the built-in AirPlay Receiver (Control Center) — you can
   > confirm this yourself with `lsof -nP -iTCP:5000 -sTCP:LISTEN`. If you
   > map `-p 5000:5000` there, requests silently go to AirPlay instead of
   > your container (you'll get a `403 Forbidden` with `Server: AirTunes`
   > in the response headers — a real, easy-to-hit gotcha, not a hint at a
   > bug in your Dockerfile). The container's own internal port stays
   > `5000` throughout this course — it's only the host-facing side of any
   > `-p` mapping or `kubectl port-forward` that needs to dodge 5000 on
   > this machine, which is why every later module maps to a different
   > host port.

4. **Poke around the running container:**

   ```bash
   docker ps
   docker logs hello-app-test
   docker exec -it hello-app-test sh   # you're now inside the container
   ```

   Try `ps aux` — it'll fail with `executable file not found`. That's not a
   mistake; `python:3.12-slim` is stripped down enough that it doesn't even
   include basic process tools. Confirm your app is PID 1 a different way:

   ```sh
   cat /proc/1/cmdline | tr '\0' ' '; echo
   exit
   ```

   You should see `python app.py` — proof that inside this container, your
   app's process *is* PID 1, with essentially nothing else running
   alongside it.

   `docker ps` lists running containers, `docker logs` prints application
   output, and `docker exec` starts another command in a running container.
   `-i` keeps input open, `-t` gives you a terminal, and `sh` is the shell
   program started inside the container.

5. **Clean up the container:**

   ```bash
   docker stop hello-app-test && docker rm hello-app-test
   ```

   `stop` asks the process to exit, `rm` removes the stopped container, and
   `&&` runs the second command only if the first succeeds. The image remains.

6. **See layer caching in action.** Edit `app.py` — change the default
   `message` string. Rebuild:

   ```bash
   docker build -t hello-app:v1 .
   ```

   Watch the build output: the `pip install` step should show `CACHED`
   (nothing about `requirements.txt` changed), while the `COPY app.py .`
   step and everything after it re-runs. This is exactly why `requirements.txt`
   is copied and installed *before* the rest of the app code — if you'd
   copied everything in one `COPY . .` step instead, editing any file would
   invalidate the pip-install cache too, and every rebuild would reinstall
   all dependencies from scratch.

## Verify you understand this before moving on

- Could you explain to someone why `docker run hello-app:v1` on your laptop
  and on a teammate's laptop behave identically, but two `python app.py`
  invocations might not?
- Why did editing `app.py` not require re-running `pip install`?

Next: [Module 2 — Kubernetes Architecture & Your First Cluster](../02-k8s-architecture-first-cluster/)
