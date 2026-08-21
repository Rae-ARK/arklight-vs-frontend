# --------------------------------------------------------------------
# /getting-started -- the exact CLI section from ARKlight's own
# README.md, reproduced as real commands (not paraphrased or
# reformatted), since these are the literal commands a visitor would
# run -- inventing a different-but-equivalent command would be the
# actual inaccuracy here.
GETTING_STARTED_STEPS = [
    (
        "1. Install (alpha branch -- see the compatibility note below)",
        "git clone --branch alpha https://github.com/Rae-ARK/ARKlight.git\n"
        "cd ARKlight\n"
        "pip install -e .",
        "Installs the `arklight` package and the `arklight` CLI command.",
    ),
    (
        "2. Build a site",
        "arklight build site.py -o ARK --no-open --verbose",
        "`site.py` must define `site = Site()` and at least one "
        "`@site.page(\"/route\")`-decorated function. `--verbose` prints "
        "a line as each compiler stage starts.",
    ),
    (
        "3. Pack it into a single file",
        "arklight pack ARK -o mysite.ark",
        "Sealed by default -- opaque to generic archive tools, but "
        "still opens directly in a browser (see this site's own "
        "\"Download offline bundle\" link in the footer).",
    ),
    (
        "4. Unpack it back",
        "arklight unpack mysite.ark -o restored",
        "Auto-detects sealed vs. plain bundles.",
    ),
    (
        "5. Look up a component's schema",
        "arklight search Picture",
        "Prints required props, whether it allows children, and "
        "whether it's a Bind(...)-able target. Typo-tolerant -- "
        "`arklight search pictur` suggests `Picture, PictureSource`.",
    ),
]

# --------------------------------------------------------------------
# CLI surface beyond the five install-to-search steps above -- real
# commands, not paraphrased, pulled directly from `arklight/cli/
# main.py`'s own argparse help text and docs/EXPERIMENTAL-APIS.md.
# Kept as a separate list rather than folded into
# GETTING_STARTED_STEPS since these aren't a linear "do this next"
# sequence -- they're independent commands a project reaches for as
# needed, some of them (--install-button) explicitly gated as
# experimental rather than an ordinary next step.
CLI_REFERENCE = [
    (
        "Scaffold a new project",
        "arklight new myproject --template production --explain-architecture",
        "`--template simple|production` picks the starting layout; "
        "`--explain-architecture` prints guidance on the service-"
        "oriented, separated-by-concern module split this project's "
        "own site.py/pages/content/components/services split follows "
        "-- runnable alone (no project name) to just read the guide.",
    ),
    (
        "Turn a build into an installable PWA",
        "arklight pwa ARK --name \"My Site\" --icon assets/icon-192.png:192x192",
        "Writes a manifest + service worker into the build directory. "
        "--install-button additionally injects a native "
        "browser-install-prompt button into every page -- EXPERIMENTAL "
        "(see the FAQ), gated because it depends entirely on the "
        "non-standardized beforeinstallprompt browser event.",
    ),
    (
        "Override theme values without editing site.py",
        "arklight build site.py --bg \"#0f0f1a\" --max-width 90rem --lang es",
        "--bg/--max-width/--font-family/--button-text/--lang all take "
        "precedence over the matching Site(...) kwarg in the site file "
        "itself, for a one-off build (CI matrix, a themed preview) "
        "without touching source.",
    ),
    (
        "Switch a git-checkout install onto the alpha branch",
        "arklight --upgrade-alpha",
        "Fetches, switches/creates the local `alpha` branch, pulls, "
        "and reinstalls in place (`pip install -e .`) so the CLI "
        "reflects it immediately -- only works against a git-checkout/"
        "editable install, the same kind this site's own README asks "
        "for in step 1 above.",
    ),
]
