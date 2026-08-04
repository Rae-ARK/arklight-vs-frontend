# Simple Data Visualization Using ARKlight and Python

A small comparison site -- **"ARKlight vs. Traditional Frontend
Frameworks"** -- built *in* ARKlight, *about* ARKlight, shipped as a
single sealed `.ark` bundle. Six static pages (bundle-size chart,
adoption/sentiment chart, feature-by-feature table, methodology, and
an honest verdict page) built entirely from Python, with no
hand-written HTML/CSS/JS.

It exists as a working example of what ARKlight can and can't do,
not just a write-up describing it -- see [`PLAN.md`](./PLAN.md) for the
full design brief, the frozen dataset, and the source list.

## ⚠️ Built against ARKlight's `alpha` branch, not `main`

This project targets ARKlight's **`alpha` branch**, which is ahead of
`main` and is **not** what you get from a default clone or a
released package. Concretely, at the time this was built:

| | `main` | `alpha` (used here) |
|---|---|---|
| Version | v0.041 | v0.043 |
| `Site.style(name, rules)` (custom CSS classes) | No | Yes |
| `arklight search <name>` / `arklight --help` | No | Yes |
| `Page(...)` head metadata (`description`, `favicon`, `og_*`) | No | Yes |
| `Backend.postprocess(...)` hook | No | Yes |
| Reactive-core vdom staging (Stage 1-2 of 8) | No | Yes |

None of this is a criticism of `main` -- `alpha` is simply where active
development lands first. But it means **this site will not build
against a `main`-branch checkout or an `arklight` install from PyPI**
if one predates these features. If you're cloning ARKlight yourself to
run this project, clone the `alpha` branch specifically:

```bash
git clone --branch alpha https://github.com/Rae-ARK/ARKlight.git
cd ARKlight
pip install -e .
```

Then check `arklight/__init__.py`'s `__version__` (or `pyproject.toml`)
reads `0.043` or later before building this project. If ARKlight has
since merged `alpha` into `main`, or moved further ahead, treat the
table above as a snapshot of what was true when this project was
built, not a live diff.

## What's in this repo

```
data.py               Frozen dataset -- bundle sizes, SO2025 survey
                       numbers, feature comparison table. Single
                       source of truth; site.py and
                       generate_assets.py both import from here.
generate_assets.py    One-off matplotlib script. Not part of
                       ARKlight -- ARKlight never touches matplotlib
                       directly, it only ever sees the finished PNGs
                       this script drops into assets/.
site.py               The actual ARKlight site: six pages, all
                       Python, using Table/Meter/Picture/Details and
                       friends from the ARKlight component vocabulary.
PLAN.md                Design brief written before the build: the
                       constraint that shapes everything (no live
                       charting libraries -- see below), the dataset,
                       page-by-page component mapping, and sources.
arklight-vs-frontend.ark   Final build output -- a sealed ARK Bundle.
                       Double-click/open it directly in a browser; it
                       renders like a normal page even though the
                       rest of the site's files are archived
                       (encrypted) alongside it.
```

## Building it yourself

```bash
./build.sh
```

Runs, in order: chart generation (`generate_assets.py`), `arklight
build site.py -o ARK`, then an *optional* `arklight pack` into
`arklight-vs-frontend.ark`. `site.py` itself checks the installed
ARKlight at import time (see "Compatibility guard" below) and exits
with a clear message rather than a raw traceback if it's not the
`alpha` branch. If you'd rather run the three steps by hand:

```bash
python generate_assets.py                        # needs matplotlib
arklight build site.py -o ARK --verbose           # needs alpha ARKlight
arklight pack ARK -o arklight-vs-frontend.ark     # optional, see below
```

### Compatibility guard (what happens if you `pip install arklight`)

There is **no published `arklight` package on PyPI** as of this
writing -- `pip install arklight` will either fail outright or, if
some other project ever claims that name, install something entirely
unrelated. The only real install path is cloning ARKlight's own repo
(`alpha` or `main`) and running `pip install -e .` inside it.

`site.py` opens with a small compatibility check (`_check_arklight_compatibility()`)
that inspects whatever ARKlight *is* installed and fails fast with an
explicit message if it's missing `Site.style(...)` or the `Page(...)`
head-metadata props this site depends on -- both `alpha`-only, per the
table above. Verified directly, in two clean virtualenvs:

- **`alpha` branch installed** -- `site.py` imports cleanly, no output
  from the guard.
- **`main` branch installed** (`v0.42.0`) -- `site.py` exits immediately
  with: `"This site (site.py) requires ARKlight's 'alpha' branch..."`
  and the exact `pip install -e .` fix, instead of the
  `AttributeError: 'Site' object has no attribute 'style'` you'd
  otherwise get from `site.style("hero", ...)` on line 6.

One more thing found while testing this: **`main`'s own `pip install
-e .` refuses to build at all** until you accept its license terms --
either `pip install -e . --config-settings=yes-i-agree-to-arklight-license=1`
or `ARKLIGHT_ACCEPT_LICENSE=1 pip install -e .` (read `LICENSE` in the
ARKlight repo first). This is a real, reproducible gate in `main`'s
build backend, not something inferred -- confirmed by actually running
the install and reading the message it prints. The `alpha` branch used
here has no such gate. `data.py`'s `PYPI_FINDING` entry records a
related, *unverified* claim (a license-acceptance gate specifically in
a PyPI-distributed wheel) that this session could not confirm one way
or the other, since no such wheel exists to test -- noted here so the
two don't get conflated.

### `.ark` bundle failures -- ARK/ is always the fallback

`arklight pack` is the last, optional step in `build.sh`, and its
failure is **not fatal**. If sealing breaks for any reason -- a future
ARKlight release changing the archive format, a filesystem issue, an
edge case `arklight pack` doesn't handle yet -- `build.sh` prints a
warning and exits `0` anyway, because the actual deployable output is
`ARK/` (real files: `index.html`, `styles.css`, `arklight.js`,
`assets/*.png`), not `arklight-vs-frontend.ark`. The `.ark` file is a
single-file convenience artifact for local/offline viewing; it was
never meant to be what a static host serves. This was tested directly
by forcing a pack failure (making the output path unwritable) and
confirming `ARK/index.html` still built and `build.sh` still exited
cleanly.

## Deploying to Cloudflare Workers

This repo includes `wrangler.jsonc`, already pointed at `./ARK` as
static assets -- no Worker script needed, this is a pure static site.

```bash
# 1. Build first (produces ./ARK)
./build.sh

# 2. Install Wrangler if you don't have it, then deploy
npx wrangler deploy
```

That uploads everything in `ARK/` to Cloudflare's edge and prints a
`*.workers.dev` preview URL. `wrangler.jsonc`:

```jsonc
{
  "name": "arklight-vs-frontend",
  "compatibility_date": "2026-08-04",
  "assets": {
    "directory": "./ARK",
    // ARKlight's Link() already emits real relative "page.html"
    // hrefs at build time. "none" was tried here to serve them at
    // their literal path with zero rewrite/redirect layer -- but
    // "none" also disables Cloudflare's "/" -> "/index.html"
    // mapping entirely, which 404s the site's own root URL. Back to
    // Cloudflare's default, "auto-trailing-slash": internal *.html
    // links still work (one extra 307 redirect to the extensionless
    // URL), and "/" resolves correctly. Confirmed by deploying with
    // "none" first and hitting a live 404 on the root path before
    // switching this back.
    "html_handling": "auto-trailing-slash",
    "not_found_handling": "404-page"
  }
}
```

### Deploying via the Cloudflare dashboard (git-connected, no local Wrangler needed)

An alternative to the CLI/`deploy.yml` paths below: Cloudflare's dashboard
can connect directly to this GitHub repo and rebuild/redeploy on every
push, with no Actions workflow or local `wrangler` install required.

1. Cloudflare dashboard -> **Workers & Pages** -> **Ship something new** ->
   **Continue with GitHub** -> select this repo.
2. **Build command**:
   ```
   git clone --branch alpha https://github.com/Rae-ARK/ARKlight.git /tmp/ARKlight && pip install -e /tmp/ARKlight && pip install matplotlib && bash build.sh
   ```
   (Cloudflare's Workers Builds image preinstalls Python/pip, so this
   runs with no extra setup -- verified directly, see the build log
   excerpt below.)
3. **Deploy command**: `npx wrangler deploy` (default -- matches
   `wrangler.jsonc` above).
4. **Root directory**: leave as the repo root (`wrangler.jsonc` lives
   there).
5. No environment variables/secrets needed for this path -- the
   dashboard's own GitHub connection handles auth, unlike the
   `deploy.yml` path below which needs the two repo secrets.
6. Confirm **Settings -> Builds -> Production branch** matches the
   branch you actually push to (`main`). Every push to that branch
   then auto-rebuilds and redeploys with no further action -- to force
   a rebuild of the current latest commit without a new push, use
   **Deployments -> Retry deployment** (or **Create deployment** to
   pick a specific branch/commit).

Verified end-to-end against this exact repo: build completed in ~30s
(ARKlight `alpha` clone + install, matplotlib install, chart
generation, `arklight build`, optional `arklight pack`), then
`npx wrangler deploy` uploaded 12 files and printed a live
`*.workers.dev` URL. First deploy 404'd on `/` specifically because of
the `html_handling: "none"` issue documented above -- fixed by editing
`wrangler.jsonc` on GitHub directly and letting the push auto-redeploy,
no rebuild trigger needed.

## Automated deploys (`.github/workflows/deploy.yml`)

Pushing to `main` clones ARKlight's `alpha` branch fresh, installs it,
runs `build.sh`, and deploys via `cloudflare/wrangler-action@v3`. Two
repo secrets are required (GitHub -> Settings -> Secrets and variables
-> Actions):

- `CLOUDFLARE_API_TOKEN` -- Cloudflare dashboard -> My Profile -> API
  Tokens -> "Edit Cloudflare Workers" template.
- `CLOUDFLARE_ACCOUNT_ID` -- Cloudflare dashboard sidebar, Workers &
  Pages overview.

The workflow deliberately does **not** try `pip install arklight` --
there's no such package on PyPI (verified directly), so that command
can only ever fail. It clones `alpha` and `pip install -e`'s it
instead, the same as the manual instructions above. Tested end-to-end
in a clean, disposable venv + fresh clone before being committed here
(clone alpha -> install -> install matplotlib -> `bash build.sh`),
not just written and assumed to work.

### A note on an alternative build script

An earlier draft of this pipeline (a `build.py` using
`hasattr(arklight, "backend")`-style introspection to detect `alpha`
vs. stable, plus a Cloudflare Worker script forcing
`Content-Disposition: attachment` on the `.ark` download) was tested
against the real package and reverted. Two concrete problems, checked
directly rather than assumed:

- The introspection returned `False` on *both* branches --
  `hasattr(arklight, "backend")` is `False` even right after `import
  arklight` on a real `alpha` install, since Python doesn't bind a
  submodule onto a package unless something already imported it.
- Forcing `Content-Disposition: attachment` on the bundle download
  reproduces the original Android bug on purpose -- it forces a
  download to a file type the OS still has no app registered for. The
  fix that's actually in this repo does the opposite: `Content-Type:
  text/html` + `Content-Disposition: inline`, so the browser renders
  it instead of downloading it (see "The mobile 'no app to open
  this' problem" above).

Only `ARK/` is deployed -- the sealed `arklight-vs-frontend.ark` bundle
gets included *inside* `ARK/` too (see next section), rather than
uploaded separately, so it's served over real HTTP like everything
else on the site.

### The mobile "no app to open this" problem, and how it's actually fixed

Distributing the raw `.ark` file for someone to download and
double-click relies on their OS recognizing the `.ark` extension and
handing it to a browser -- desktop OSes are often permissive enough
that this works, but on Android there's no registered app for an
unrecognized extension, so the download just sits there with no
"Open with Browser" option. That's a real, reported failure mode, not
a hypothetical one.

The fix isn't a workaround on the phone -- it's not relying on file
association at all. `build.sh` now:

1. Copies the packed bundle into `ARK/arklight-vs-frontend.ark`, so
   it's served over HTTP once deployed, not handed to the OS as a
   downloaded file.
2. Writes `ARK/_headers` (Cloudflare's [custom-headers convention](https://developers.cloudflare.com/workers/static-assets/headers/))
   forcing `Content-Type: text/html` (and `Content-Disposition:
   inline`) specifically on that path:

   ```
   /arklight-vs-frontend.ark
     Content-Type: text/html
     Content-Disposition: inline
   ```

   This works *because* the `.ark` polyglot's front matter is real,
   valid HTML from byte zero, by design (see ARKlight's own README,
   "ARK Bundle"). Wrangler would otherwise guess a generic
   `application/octet-stream` for an unrecognized extension, which is
   exactly what triggers the download-with-no-viewer behavior on
   Android. Forcing `text/html` makes any browser -- desktop or
   mobile -- render it directly in-tab, the moment it's requested over
   HTTP, no OS file-type association involved at all.
3. Links to it from the site's footer ("Download offline bundle
   (.ark)") -- verified in `ARK/index.html`:
   `<a href="arklight-vs-frontend.ark" class="source-note">`.

**Graceful degradation, tested directly:** if `arklight pack` fails
(see the section above), `build.sh` skips steps 1-2 entirely --
`ARK/_headers` and the copied bundle simply aren't written. The
footer's link is still there (it's baked into every page by
`site.py`), but it now resolves through Cloudflare's own
`not_found_handling: 404-page` into a normal, in-browser 404 -- not a
phone-native "no app can open this" dead end. Confirmed by forcing a
real pack failure and inspecting `ARK/`: no `_headers`, no bundle, but
`ARK/index.html` (and the rest of the site) still built and deployed
cleanly.

## The constraint that shapes the whole site

ARKlight has no live charting library and never will -- accepting
arbitrary JS/HTML is a permanent non-goal, not a current gap. So "data
visualization" here comes from exactly two places ARKlight actually
supports: pre-rendered matplotlib PNGs (the bar and pie charts, dropped
into `assets/` and embedded with `Picture`/`Image`), and native
zero-JS widgets ARKlight already has schema support for (`Meter`/
`Progress`, used for the KPI strip). Both are deliberate -- the site
itself demonstrates ARKlight's real ceiling rather than just
describing it. Full reasoning in `PLAN.md` Section 1.

## Notes from building this

Some honest, specific observations from actually building a multi-page
site in ARKlight's `alpha` branch, worth keeping alongside the code
rather than filing away:

**What worked well:**
- Staying in Python the entire time, start to finish -- the data
  (`data.py`), the chart generation (`generate_assets.py`), and the
  page structure (`site.py`) all share the same syntax and mental
  model. No JSX context-switch, no `.vue` file sections, no bundler
  config.
- ARKlight's validation is genuinely useful, not just strict. Nesting
  something invalid inside a text-only component fails the build with
  an exact node path, before any file is written -- rather than a
  broken render that has to be debugged visually after the fact.
- The schema (`arklight/ir/schema.py`) is small enough to read once
  and then *know*, with certainty, every component's required props
  and nesting rules for the rest of the build -- rather than working
  from statistical pattern-matching against a large, only-partly-
  relevant training corpus (the way generating React/Vue/Svelte code
  from memory tends to work).

**What had a real cost:**
- The chart workaround (matplotlib PNGs, generated offline, then
  wired in as static images) is a genuine two-step process, not a
  stylistic choice -- there's no inline, live `<BarChart data={...}>`
  equivalent, and there won't be, per ARKlight's own non-goals.
- Hit one non-obvious bug specific to ARKlight's two-phase execution
  model: `from data import X` inside a page function behaved
  differently than the same import at module level, because the site
  file's top-level code and its page functions run in different
  compiler stages. Nothing about knowing Python in general predicts
  that -- it came from reading the traceback and reasoning about
  ARKlight's loader specifically, not from recalling a known pattern.

Net take: for a task like this one -- static pages, tables, and
pre-computed data, no live interactivity -- ARKlight's closed-
vocabulary ceiling was rarely a real constraint, except at the charts.
A task that needed genuine client-side interactivity would look
different, and would probably lean on `v0.044`'s in-progress reactive-
core work (see the main ARKlight repo's `docs/DESIGN-NOTES.md`) rather
than this project's approach.

## Sources

See [`PLAN.md`](./PLAN.md) Section 2d for the full list -- Stack
Overflow Developer Survey 2025, State of JS 2025, js-framework-
benchmark, and ARKlight's own repo docs. ARKlight's own bundle-size
figures were measured directly during this build, not sourced from an
article; the exact commands are documented on the site's own
Methodology page.
