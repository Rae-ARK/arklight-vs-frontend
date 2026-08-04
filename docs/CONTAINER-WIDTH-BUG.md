# The desktop container-width bug: why it happened, and how to prevent it recurring

Status: **Investigation complete. Fix not yet applied** -- this document
is being committed *before* any CSS change, on purpose, so the root
cause is on record independent of whatever patch follows it. This file
will be updated in place (not superseded by a new file) as the actual
fix lands -- see "Status" at the bottom.

## The symptom

On a wide desktop viewport, every page renders as a narrow, centered
column with large, permanently empty margins on both sides -- roughly
720px of content in the middle of a 1920px window. It's not a broken
render (nothing overlaps, nothing is cut off) -- it's a real,
reproducible layout choice that looks like a bug because it wastes
most of a wide screen's width, on a site whose own copy elsewhere
(`.grid`, `.switcher`, the bento-hero cards) was clearly designed with
a multi-column desktop layout in mind.

## Root cause

`body`'s width is hard-capped by ARKlight's own generated stylesheet,
not by anything this site's `site.py`/`components/`/`services/` code
does:

```css
/* arklight/backend/css/render.py -- BASE_CSS, baked into every site */
:root {
  --ark-max-width: 720px;
}

body {
  max-width: var(--ark-max-width);
  margin-left: auto;
  margin-right: auto;
  ...
}
```

This is a Python string constant inside ARKlight's own CSS backend
(`arklight/backend/css/render.py`), emitted verbatim into every
generated `styles.css`. `720px` is not a default this site opted into
-- it's the *only* value that has ever existed for `--ark-max-width`,
because nothing in ARKlight's public API lets a site override it.
Checked directly against the three places an override could plausibly
live, all three come up empty:

1. **`Page(...)` props don't reach `<body>`.** `arklight/backend/html/
   render.py::_render_page` only ever reads `title`/`description`/
   `favicon`/`og_*` off the root `Page` node -- confirmed by reading
   the function directly, not assumed. There is no `style=`/
   `class_name=` path from a site's `Page(...)` call down to the
   actual `<body>` element ARKlight emits.

2. **`Site.style(name, rules)` only emits class selectors.** Every
   custom style this site registers (`services/styles.py`) compiles to
   `.name { ... }` -- there is no way to target `:root` or `body`
   through this API. It can add a new class; it cannot override an
   element-level rule ARKlight's own base stylesheet already wrote.

3. **The theme wrapper is a *descendant* of `body`, not an ancestor.**
   `components/layout.py::page_shell()` wraps every page's content in
   a `<div style="--ark-accent: ...; background: ...">` -- but that
   div is a *child* of `body`, one level too deep to affect `body`'s
   own `max-width` computation. CSS custom properties only flow
   downward: overriding `--ark-max-width` on that wrapper changes what
   the wrapper's own descendants would read, but `body` already
   resolved its own `max-width: var(--ark-max-width)` from the
   un-overridden `:root` value before the wrapper div even exists in
   the tree. This is the *exact same* category of bug
   `services/theming.py`'s own docstring already diagnoses for
   `--ark-bg` -- and that file's fix (paint a literal `background` on
   the wrapper instead of relying on the custom property) works for
   `background` specifically because a child div can paint its own
   background over its own box. There is no equivalent trick for
   `max-width`: a child element can never make its *parent* (`body`)
   wider than what the parent itself already computed. That's not a
   workaround gap in this site's code -- it's a hard structural limit,
   confirmed by re-reading `theme_wrapper_style()`'s own reasoning
   rather than assumed to generalize.

**In short: this site's `--ark-accent`/`--ark-accent-hover`/
`--ark-border`/`background` re-theme (Phase 2, Stage 6) worked, and
gave false confidence that "override a `--ark-*` variable on the
wrapper" is a general pattern. It isn't -- it only works for
properties `body` doesn't itself read directly. `--ark-max-width` is
exactly the one custom property in ARKlight's base stylesheet that
`body` *does* read directly, which is why it's the one override this
pattern can't reach.**

## Why nobody caught this before now

- **No page on this site visually needed a wide viewport to look
  "checked".** Every page (tables, cards, forms) reads as intentional
  and complete inside a 720px column on a laptop-width preview, which
  is almost certainly how this was checked during Stage 6/7/8 builds
  (`git log`/`PLAN.md` mention rendering pages "to PNG to confirm,"
  not a stated viewport width) -- the failure mode only shows up on a
  genuinely wide monitor, which a quick render-and-diff check doesn't
  surface.
- **ARKlight has no `@media` queries (v0.048, not yet implemented --
  see `content/faq.py`), so the project's own working assumption
  became "responsive issues are handled via the intrinsic-layout
  utility classes (`.switcher`/`.grid`/`.stack`)."** Those classes are
  real and do work -- but they only control how *content reflows
  inside* a container; none of them touch the container's own
  `max-width`. The absence of `@media` correctly ruled out one kind of
  fix, but that got over-generalized into "therefore intrinsic
  patterns solve all our sizing," which isn't true for a value baked
  into an ancestor element this site's own components never touch.

## How to prevent this recurring

1. **Treat "does an override reach `body`, or only a descendant of
   it?" as a required check before trusting any `--ark-*` re-theme.**
   `--ark-accent`/`--ark-accent-hover`/`--ark-border` are safe to
   override on the `page_shell()` wrapper because nothing in
   `BASE_CSS` reads them directly on `body` itself (only on
   descendants -- links, buttons, borders). `--ark-bg` and
   `--ark-max-width` are the two exceptions, because `body`'s own
   rule reads both directly. `--ark-bg` already has a documented
   workaround (paint a literal `background`); `--ark-max-width` did
   not, until this document.

2. **Add this to `content/faq.py`** (mirroring how the `@media`
   limitation and the `on_click` single-action limitation are already
   documented there) so a future contributor hits this file before
   hitting the same false assumption Stage 6 encoded silently:

   > "Can a site override `--ark-max-width` the same way it overrides
   > `--ark-accent`? No -- `body`'s `max-width` rule reads the
   > `:root`-scoped value directly, and nothing in `Page(...)` or
   > `Site.style()` can set a variable at a scope that reaches `body`
   > itself; only a wrapper *inside* `body` is reachable, which is one
   > level too deep. See `docs/CONTAINER-WIDTH-BUG.md`."

3. **Any real fix has to change what `body` resolves `--ark-max-width`
   to, not add another wrapper-level override.** The only way to do
   that without editing ARKlight's own installed package is
   `Backend.postprocess(output_files)` -- an alpha-only hook
   (confirmed in `arklight/backend/base.py` and `arklight/compiler/
   pipeline.py`) that runs after every backend's `render()` and can
   rewrite the *generated* `styles.css` string before it's written to
   disk. It requires calling `arklight.compiler.pipeline.build(...)`
   directly with a custom `backends=[...]` list (a small Python build
   script), since the plain `arklight build` CLI always uses
   `default_backends()` with no flag to inject a custom backend.
   This is the mechanism the next patch will use -- documented here
   first so the *reason* it's necessary (points 1-3 above) isn't lost
   once the fix itself lands and looks, in hindsight, like an obvious
   one-line change.

4. **Longer term, this is worth reporting upstream to ARKlight
   itself** -- either a `Site(max_width=...)` constructor param, or
   generalizing the existing `Page(...)` head-metadata escape hatch to
   include a small set of body-level layout props. A per-site
   `postprocess`-based CSS string-replace is a legitimate workaround
   for `alpha`, not something every ARKlight site should have to
   reach for just to use its own wide viewport.

## Status

- [x] Root cause identified and verified against ARKlight's actual
      source (`arklight/backend/css/render.py`,
      `arklight/backend/html/render.py::_render_page`,
      `arklight/backend/base.py`, `arklight/compiler/pipeline.py`),
      not assumed from the symptom alone.
- [ ] Fix implemented (`Backend.postprocess`-based `styles.css`
      rewrite, using `clamp()`/intrinsic sizing per Intrinsic Web
      Design conventions, no `@media` involved) -- **not in this
      patch**.
- [ ] `content/faq.py` entry added, pointing back to this file.
- [ ] Verified against a real wide-viewport render, not just a clean
      `arklight build`.

This file will be updated in place as each remaining item is checked
off, rather than replaced by a new document.
