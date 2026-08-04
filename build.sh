#!/usr/bin/env bash
# Build pipeline for the ARKlight vs. Frontend Frameworks comparison site.
#
# Ported unchanged from main's build.sh -- nothing here actually
# depended on main's monolithic site.py/data.py, only on the *names*
# site.py and generate_assets.py existing at the repo root, which the
# SoA (Separation of Areas) branch still has: site.py is now a thin
# composition root that imports components/content/pages/services
# instead of one 654-line file, and generate_assets.py imports its
# two datasets from content/bundle_size.py and content/adoption.py
# instead of the deleted data.py, but both still run the same way.
#
# Always produces a deployable ARK/ folder. Packing that folder into a
# single sealed arklight-vs-frontend.ark bundle is attempted, but is
# NOT required for deployment -- if packing fails for any reason (a
# future ARKlight release changing the sealing format, a permissions
# issue, running against an ARKlight build that lacks `arklight pack`,
# etc.) the script prints a clear warning and continues. ARK/ is what
# Cloudflare Workers actually serves either way -- see wrangler.jsonc.
set -uo pipefail

echo "==> Checking ARKlight installation"
if ! python3 -c "import arklight" 2>/dev/null; then
    echo "ERROR: arklight is not importable in this Python environment."
    echo "This project requires ARKlight's 'alpha' branch:"
    echo "    git clone --branch alpha https://github.com/Rae-ARK/ARKlight.git"
    echo "    cd ARKlight && pip install -e ."
    exit 1
fi

echo "==> Generating chart assets (matplotlib)"
mkdir -p assets
if ! python3 generate_assets.py; then
    echo "ERROR: generate_assets.py failed. Is matplotlib installed?"
    echo "    pip install matplotlib"
    exit 1
fi

echo "==> Building site (site.py -> ARK/)"
rm -rf ARK
# site.py itself raises a clear SystemExit if ARKlight isn't the alpha
# branch (see services/compatibility.py's check_arklight_compatibility,
# called at the top of site.py) -- that message, not this script's, is
# the one you want to read if this fails.
if ! arklight build site.py -o ARK --no-open --verbose; then
    echo "ERROR: arklight build failed -- see message above."
    exit 1
fi

if [ ! -f "ARK/index.html" ]; then
    echo "ERROR: build reported success but ARK/index.html is missing."
    exit 1
fi

echo "==> Build OK -- ARK/ is ready to deploy as-is."

echo "==> Attempting to pack ARK/ into a sealed .ark bundle (optional)"
if arklight pack ARK -o arklight-vs-frontend.ark; then
    echo "==> Packed arklight-vs-frontend.ark successfully."

    # Serve the bundle from the deployed site too (linked from the
    # footer), not just as a local file -- this is what fixes the
    # "no Open with Browser option" problem on Android and similar
    # mobile OSes. A raw .ark file downloaded to a phone has no
    # registered file-type association, so the OS has nothing to hand
    # it to. Serving it over HTTP instead lets us set the Content-Type
    # ourselves (see the _headers rule below): the bundle's front
    # matter is valid, self-contained HTML by design (that's the whole
    # "polyglot" idea -- see ARKlight's README, "ARK Bundle"), so
    # forcing text/html makes any browser render it directly in-tab,
    # no OS file-association step involved at all.
    cp arklight-vs-frontend.ark ARK/arklight-vs-frontend.ark
    cat >> ARK/_headers << 'HEADERS_EOF'
/arklight-vs-frontend.ark
  Content-Type: text/html
  Content-Disposition: inline
HEADERS_EOF
    echo "    -> Also copied into ARK/ and added a _headers rule so it"
    echo "       renders in-browser (not a raw file download) once deployed."
else
    echo "WARNING: 'arklight pack' failed. This does NOT block deployment --"
    echo "         ARK/ (the actual folder of files) is what gets deployed"
    echo "         to Cloudflare, not the .ark bundle. The .ark file is a"
    echo "         convenience artifact for local/offline viewing only."
    echo "         The footer's 'Download offline bundle' link will 404"
    echo "         cleanly (Cloudflare's not_found_handling: 404-page) --"
    echo "         a normal, in-browser 404 page, not a broken file-open"
    echo "         prompt with no app to hand it to."
fi

echo ""
echo "==> Done. Deployable output: ./ARK"
echo "    Deploy with: npx wrangler deploy"
echo "    (wrangler.jsonc already points 'assets.directory' at ./ARK)"
