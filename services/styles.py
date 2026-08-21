"""
Registers every custom Site.style(...) class this project defines.
Kept as its own service (not inline literal dicts in site.py) so the
class *definitions* are data-driven from content.theme, and site.py
itself only has to make one call, not carry ~30 lines of style dicts
inline. Has to be a function taking `site` as an argument (not a
module-level side effect) because Site.style() is an instance method
-- the Site() instance only exists once site.py constructs it, in the
composition root.

Re-skin pass: added the frosted-glass ("Mica"/"Acrylic"-style)
surfaces -- `card`, `hero`, `nav`, `glass`, `pill` below. `theme` is
now actually read (previously `del theme`'d -- see the old comment
this replaced) because `background`/`backdrop-filter`/`box-shadow`
have no sitewide `--ark-*` slot the way accent/border/bg do; they're
only reachable through Site.style()'s per-class `{property: value}`
dicts, so the glass tokens in content.theme have to flow through here
by value, not by CSS variable reference. Confirmed directly against
arklight/backend/css/custom_styles.py that a rules dict may mix plain
properties with ":<pseudo>:<property>" keys (":hover:...", etc., one
of `arklight.api.ALLOWED_PSEUDO_CLASSES`) in the same site.style(...)
call -- that's what the hover-lift rules on `card`/`pill` below use,
not a separate call or raw CSS.

Every glass class below only *adds* background/backdrop-filter/
box-shadow/border -- it deliberately leaves border-radius, padding,
and margin undeclared wherever a base ARKlight rule already sets them
(`.card`, `<details>`), since a same-specificity custom class rule
overrides the cascade property-by-property, not block-by-block; only
`hero`, which has no base-stylesheet equivalent at all, needs a
complete rule set of its own.
"""

from __future__ import annotations


def register_site_styles(site, theme: dict[str, str]) -> None:
    # The custom classes below read var(--ark-accent) instead of a
    # hardcoded hex, so they automatically follow whatever
    # --ark-accent is in scope -- including the theme override applied
    # in page_shell() -- rather than needing their own separate
    # re-theme.

    # ---- Frosted-glass surface, shared by every glass-y class below.
    # A single source of truth for the four properties that make a
    # panel read as "glass" (translucent fill, blurred/saturated
    # backdrop, a hairline light border, a soft diffuse shadow instead
    # of a hard drop shadow) -- kept as one dict merged into each
    # class's own rules rather than four repeated site.style(...)
    # calls, so a palette tweak in content.theme only has to flow
    # through one place here.
    glass_surface = {
        "background": theme["glass_bg"],
        "backdrop-filter": theme["glass_blur"],
        "-webkit-backdrop-filter": theme["glass_blur"],  # Safari has no unprefixed support yet
        "border": f"1px solid {theme['glass_border']}",
        "box-shadow": theme["glass_shadow"],
    }

    # `.card` already gets border/border-radius/padding/margin from
    # ARKlight's base stylesheet (arklight/backend/css/
    # base_stylesheet.py) -- this only layers the glass surface plus a
    # gentle hover lift on top, it never redeclares the structural
    # properties base .card already owns.
    site.style("card", {
        **glass_surface,
        "transition": "transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease",
        ":hover:transform": "translateY(-2px)",
        ":hover:box-shadow": theme["glass_shadow_hover"],
        ":hover:background": "rgba(255, 255, 255, 0.68)",
    })

    # `glass` -- same treatment for nodes that aren't `.card` (Details
    # panels on /faq and /verdict, which otherwise only get the base
    # <details> tag rule's plain border). Slightly smaller radius than
    # `.card`'s 12px would look identical, so this stays intentionally
    # close rather than identical.
    site.style("glass", {
        **glass_surface,
        "border-radius": "14px",
    })

    # The nav bar itself, restyled as a frosted bar instead of a flat
    # bottom-border rule -- the one place on every page a Windows
    # 11-style "Mica" surface reads clearly, since it's the one
    # element guaranteed to sit over the busiest part of the page
    # background (services/theming.py's gradient repaint) on every
    # route. Only overrides border-bottom/adds new properties -- the
    # base .nav rule's `display: flex; flex-wrap: wrap; gap: ...` for
    # laying out the links themselves is untouched.
    site.style("nav", {
        "background": theme["glass_bg"],
        "backdrop-filter": theme["glass_blur"],
        "-webkit-backdrop-filter": theme["glass_blur"],
        "border-bottom": "none",
        "border-radius": "16px",
        "padding": "0.85rem 1.25rem",
        "box-shadow": theme["glass_shadow"],
    })

    # Fully rounded "pill" buttons -- opt-in via class_name="pill" (see
    # /playground's Buttons) rather than a sitewide button restyle,
    # since site.style(...) only ever emits `.name { ... }` class
    # rules (confirmed against arklight/backend/css/custom_styles.py),
    # never a bare `button { ... }` tag-selector override -- there is
    # no sitewide way to restyle every <button> short of an ARKlight
    # base-stylesheet change, which is out of scope for a site-level
    # re-skin.
    site.style("pill", {
        "border-radius": "999px",
    })

    site.style("hero", {
        **glass_surface,
        "border-radius": "20px",
        "padding": "2.5rem 2rem",
        "margin-bottom": "1.5rem",
    })
    site.style("kpi-value", {
        "font-size": "2rem",
        "font-weight": "700",
        "color": "var(--ark-accent)",
    })
    site.style("source-note", {
        "font-size": "0.85rem",
        "color": "#666",
    })
    site.style("nav-brand", {
        "font-weight": "700",
        "color": "var(--ark-accent)",
        "letter-spacing": "-0.02em",
    })

    # Bento-grid "hero" card -- a .grid child that spans two tracks
    # instead of one (PLAN.md Section 7/10). Shared by Home,
    # Architecture, and (Stage 8) /playground's card grid.
    site.style("bento-hero", {
        "grid-column": "span 2",
    })

    # /changelog status badges.
    site.style("status-done", {
        "color": "#3f6212",
        "font-weight": "600",
    })
    site.style("status-planned", {
        "color": "var(--ark-muted)",
    })
    site.style("status-in-progress", {
        "color": "var(--ark-accent)",
        "font-weight": "600",
    })

    # Phase 2, Stage 8: /playground's per-card detail panel. No
    # inline <style>/@media/CSS transition escape hatch needed --
    # transition is just another property style={} already passes
    # through untouched, same mechanism as every other inline style on
    # this site, applied here via Site.style() instead since both
    # states (collapsed/expanded) need to share one base rule.
    #
    # Naming note, confirmed by reading arklight/backend/css/render.py
    # (_render_custom_styles): Site.style() classes are emitted
    # `sorted(custom_styles)` by name, NOT registration order -- so
    # with equal selector specificity, whichever name sorts *later*
    # wins the cascade when both classes are applied to the same
    # element at once. "playground-panel" < "playground-panel-open"
    # alphabetically (shorter prefix sorts first), which is exactly
    # the order needed: the base (collapsed) rule first, the
    # bind_class-toggled override second, so the override actually
    # overrides instead of being silently shadowed. Verified directly
    # against the generated ARK/styles.css, not assumed.
    site.style("playground-panel", {
        "max-height": "0",
        "overflow": "hidden",
        "opacity": "0",
        "transition": "max-height 0.25s ease, opacity 0.2s ease",
    })
    site.style("playground-panel-open", {
        "max-height": "400px",
        "opacity": "1",
    })
