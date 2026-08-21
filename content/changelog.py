# --------------------------------------------------------------------
# /changelog -- the milestone table from ARKlight's own
# docs/ARCHITECTURE.md, reproduced as structured data (a real Table on
# this page) instead of just linking off to GitHub. Status values match
# that table exactly, read directly rather than re-derived.
#
# Re-verified against the alpha branch during the re-skin pass:
# ARKlight's own CHANGELOG.md/PROGRESS.md have moved well past v0.043
# (as far as v0.0436 as of this writing -- arklight live-streaming, a
# dev server; arklight.config.py; PWA manifest icons via --icon), but
# this table intentionally still only lists what was directly verified
# against source for *this site's own build* -- the v0.048 row below
# is the one correction made here: docs/EXPERIMENTAL-APIS.md and
# arklight/api.py confirm site.media_query(...) and Site.style(...)'s
# pseudo-class rule keys are both implemented and working today
# (confirmed directly, not assumed from a version number), even though
# ARKlight's own PROGRESS.md snapshot table still marks v0.048 overall
# as "IN PROGRESS" -- the structured <head>/<header> extension half of
# that milestone, not the CSS half, is what's still pending.
CHANGELOG_MILESTONES = [
    # (version, what, status)
    ("v0.001", "Python -> HTML", "DONE"),
    ("v0.002", "CSS (default stylesheet)", "DONE"),
    ("v0.003", "JavaScript helpers, incl. two vocabulary extension addenda", "DONE"),
    ("v0.0035", "Stateful JS -- registry-driven behaviors + actions; State/Bind/Action.*", "DONE"),
    ("v0.004a", "CLI scaffolding (arklight new <name> --template simple|production)", "DONE"),
    ("v0.036", "ARK Bundle spec v1 -- single-file .ark packaging (arklight pack)", "DONE"),
    ("v0.037", "Sealed ARK Bundles -- archive half encrypted by default, arklight unpack", "DONE"),
    ("v0.041", "CLI/pipeline/JS runtime hardening + stateful JS vocabulary addenda I & II", "DONE"),
    ("v0.042", "Extra CSS features -- Site.style(), arklight search, arklight --help", "DONE"),
    ("v0.042+", "arklight search --near/--accept (usage-ranked suggestions) + --serve (stdio JSON server)", "DONE"),
    ("v0.043", "Optional <head> metadata props + Backend.postprocess(...) hook", "DONE"),
    ("experimental", "Gated escape hatches -- Site.style(...) pseudo-class rules (:hover:, :focus:, ...) + site.media_query(...); both flagged at build time, see arklight/experimental.py", "DONE"),
    ("experimental", "arklight pwa --install-button -- native install-prompt injection via beforeinstallprompt", "DONE"),
    ("v0.0438", "Android backend -- arklight android (androidx.webkit.WebViewAssetLoader)", "PLANNED"),
    ("v0.044", "JS backend capability expansion -- reactive core parity with Vue 3", "PLANNED"),
    ("vdom-staging", "Reactive-core vdom staging (Stage 1-2 of 8 done: snabbdom core, reactive class binding)", "IN PROGRESS"),
    ("v0.048", "Structured <head>/<header> extension (the CSS @media half shipped experimentally, above)", "IN PROGRESS"),
    ("v0.010", "User-defined, reusable components", "PLANNED"),
    ("v0.100", "Alternate backends (Vue, Svelte)", "PLANNED"),
    ("v1.0", "Stable compiler", "PLANNED"),
]
