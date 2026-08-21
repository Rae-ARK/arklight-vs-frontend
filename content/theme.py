"""
Phase 2, Stage 6 re-theme values (PLAN.md Section 7), extended in the
re-skin pass with a frosted-glass ("Mica"/"Acrylic"-style, Windows
11-adjacent) palette layered on top of the original warm re-theme --
not a replacement of it.

ARKlight's default --ark-accent (#4f46e5) is an indigo -- squarely in
the "blue-dominant default tech palette" current landing-page trend
coverage flags as generic. Picked a warm rust/terracotta instead --
distinct from every framework's own brand color in the adoption pie
chart (React cyan, Vue green, Angular red, Svelte orange-red) so it
doesn't visually blend into "just another framework color", and
distinct from ARKlight's own default indigo so the re-theme is
actually visible.

Glass surfaces need something with visible variation *behind* them to
actually read as translucent -- a flat single-color background makes
`backdrop-filter: blur(...)` indistinguishable from an opaque panel.
`bg_gradient` supplies that (soft warm-toned radial blooms, kept in
the same rust/cream family as the rest of the palette so the glass
tint stays coherent instead of introducing an unrelated hue). `bg`
stays a plain solid color -- it's still what flows through
Site(bg=...) into the `--ark-bg` custom property, which is typed
`<color>` at the CSS `@property` level (see
arklight/backend/css/design_tokens.py's `ROOT_VAR_SYNTAX`) and would
silently reject a gradient value rather than render it. See
services/theming.py for exactly where `bg` vs. `bg_gradient` each
get used and why that split is load-bearing, not cosmetic.

Pure data -- how this gets turned into an actual style dict / CSS
custom properties lives in services/theming.py and services/styles.py,
not here.
"""

THEME = {
    "accent": "#b8480f",       # warm rust/terracotta, not blue/indigo
    "accent_hover": "#8f3709",
    "bg": "#f3ece0",           # solid fallback -- flows into --ark-bg (typed <color>)
    "bg_gradient": (
        "radial-gradient(1100px circle at 12% -10%, #ffe3c2 0%, transparent 55%), "
        "radial-gradient(900px circle at 92% 5%, #ffd9e0 0%, transparent 55%), "
        "radial-gradient(1100px circle at 50% 115%, #dcf1e6 0%, transparent 60%), "
        "linear-gradient(160deg, #faf6f0 0%, #f3ece0 100%)"
    ),
    "border": "rgba(184, 114, 61, 0.22)",   # warm-neutral, now translucent to match glass
    # Frosted-glass ("Mica"/"Acrylic"-style) surface tokens -- read by
    # services/styles.py, not by ARKlight's --ark-* custom properties
    # directly, since backdrop-filter/box-shadow have no dedicated
    # sitewide slot the way accent/border/bg do.
    "glass_bg": "rgba(255, 255, 255, 0.55)",
    "glass_border": "rgba(255, 255, 255, 0.65)",
    "glass_blur": "blur(20px) saturate(180%)",
    "glass_shadow": "0 8px 32px rgba(120, 72, 30, 0.10)",
    "glass_shadow_hover": "0 14px 40px rgba(120, 72, 30, 0.16)",
}
