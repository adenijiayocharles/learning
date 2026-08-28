# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A static, no-build multi-course "Learning Hub" — self-paced courses on
infrastructure/engineering topics, each pairing short written notes with a
hands-on way to explore them (a lab or an interactive simulation). Root
`index.html` is a launcher listing every course as a card; each course
lives in its own top-level folder with its own `README.md` and `index.html`.

There is no build system, package manager, linter, or test suite in this
repo — every page is a single, self-contained HTML file (inline
`<style>`/`<script>`), opened directly via `file://` or a static file
server.

## Commands

Preview any page locally:

```bash
python3 -m http.server 8000   # from the repo root
```

Then open `http://localhost:8000/index.html` (hub),
`http://localhost:8000/kubernetes/index.html`, or
`http://localhost:8000/cap-theorem/index.html`. There's no lint/test/build
command — changes are verified by opening the page in a browser and
checking the console.

The Kubernetes course's own content teaches `docker`, `minikube`,
`kubectl`, and `helm` commands as its subject matter (see
`kubernetes/README.md` and its numbered modules) — those aren't repo
tooling, they're what the course's exercises run against a local cluster.

## Architecture

**Two established course formats** (see root `README.md` for the
user-facing description). New courses should pick one of these rather than
inventing a third:

- **Hands-on lab** (`kubernetes/`): numbered module folders (`01-...`
  through `12-...`), each with a `README.md` (concept + exercise), starter
  YAML/config with `# TODO` placeholders under `manifests/`, and a matching
  `solution/`. `apps/hello-app/` is the *one* shared Flask demo app reused
  across every module (`Dockerfile.starter` has TODOs; `Dockerfile.solution`
  and the checked-in `Dockerfile` are the working reference). `PLAN.md`
  documents the original design rationale for the curriculum.
- **Interactive simulation** (`cap-theorem/`): no modules — `index.html`
  *is* the course (a Three.js scene), and `README.md` is the sourced
  written explanation of what it simulates, not a lab guide.

Adding a course means creating its folder, then adding a card to root
`index.html` (`.course-card` markup) and a row to the table in root
`README.md`.

**Each course's `index.html` is a single self-contained file** — no
bundler, no separate JS/CSS files. All three (`index.html`,
`kubernetes/index.html`, `cap-theorem/index.html`) share one design-token
system, copy-pasted intentionally rather than factored into a shared
stylesheet (there's no build step to assemble one):

- CSS custom properties for color (`--bg`, `--surface`, `--surface-2`,
  `--ink`, `--muted`, `--accent`, `--line`, `--good`, `--shadow`, plus a
  couple of course-specific extras like `--warn`/`--stale`/`--info` in CAP
  Theorem), themed via `prefers-color-scheme: dark` guarded with
  `:root:not([data-theme="light"])`, plus a `:root[data-theme="dark"]`
  override. No page currently wires up a UI control for `data-theme` — it's
  a hook for a future toggle, kept consistent across all three files.
- Fonts: Archivo (headings), Public Sans (body), JetBrains Mono (code/labels),
  all via one Google Fonts `<link>`.
- Any external JS is loaded via a classic `<script src>` tag from
  `cdnjs.cloudflare.com`, pinned to an exact version with a real
  `integrity`/`crossorigin` SRI hash — compute it by downloading the file
  and running `openssl dgst -sha384 -binary <file> | openssl base64 -A`,
  don't hand-write or guess one. Currently pinned: `marked@4.3.0` +
  `highlight.js@11.9.0` (kubernetes), `three.js@0.160.0` (cap-theorem).

**The three.js version is pinned for a specific, load-bearing reason**:
cdnjs stopped shipping a classic global/UMD `three.min.js` build after
r160 — r161+ is ES-modules-only, which won't work as a plain `<script src>`
opened via `file://`. Before bumping that version, re-check cdnjs's file
listing for the target version rather than assuming a newer build still
has a global script.

**Kubernetes course content is authored once and rendered twice**: the
numbered module `README.md` files are the source of truth;
`kubernetes/index.html` embeds that same markdown text verbatim inside
`<script type="text/markdown" id="md-NN">` blocks (not JS string literals —
this sidesteps escaping problems since the content contains triple-backtick
code fences and inline code), then renders it client-side via
`marked.parse()` + `highlight.js`. Editing a module's `README.md` requires
the matching edit in `kubernetes/index.html`'s corresponding
`<script type="text/markdown">` block to keep the two in sync — nothing
does this automatically.

**Known environment gotcha baked into the Kubernetes course content**:
macOS's built-in AirPlay Receiver listens on port 5000 by default,
colliding with the demo app's port. Course instructions deliberately map
host-side ports to `5050`/`5001`/etc. instead of `5000` for every
`docker run -p` / `kubectl port-forward` step — keep that offset if adding
new port-forwarding instructions.
