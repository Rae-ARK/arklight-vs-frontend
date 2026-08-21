"""
Turns content.theme.THEME (pure data) into the style dict
components.layout.page_shell() actually applies. Kept as a service
rather than inline in the layout component so the *why* -- a fairly
subtle ARKlight rendering detail -- has one place to live, documented
once, instead of being re-derived (or silently dropped) if the layout
component ever gets touched for an unrelated reason.
"""

from __future__ import annotations


def theme_wrapper_style(theme: dict[str, str]) -> dict[str, str]:
    """
    Build the style= dict for page_shell()'s wrapper Container.

    Page(...) itself only ever becomes <body>'s *children* -- style=/
    class_name= on Page has nowhere to attach (confirmed by reading
    ARKlight's own arklight/backend/html/render.py::_render_page,
    which never reads props off the root node besides title/
    description/favicon/og_*). So the re-theme override has to go on a
    real rendered wrapper one level in -- a Container around
    Header+Main+Footer. CSS custom properties inherit to every
    descendant from there, which is everything --ark-accent/
    --ark-accent-hover/--ark-border actually get read by (buttons,
    links, focus rings, .card borders, the "hero" class, ...).

    --ark-bg specifically is consumed by the `body` rule itself, one
    level *above* this wrapper, so overriding the custom property
    alone wouldn't repaint anything -- body already resolved its own
    background from the un-overridden :root value before this div
    exists. Fixed with negative margins matching body's own padding
    (2.5rem 1.5rem 4rem, see arklight/backend/css/render.py) that pull
    the wrapper out to body's edges, then equal padding re-establishes
    the original spacing *inside* a div that paints its own literal
    `background` -- a real repaint, not an inert unread custom
    property.

    That literal `background` is `theme["bg_gradient"]`, not
    `theme["bg"]` -- deliberately. This is inline `style=`, rendered
    straight into the HTML `style` attribute, not routed through a
    `--ark-*` custom property, so it never touches the `<color>`-typed
    `@property` constraint `theme["bg"]` has to respect (see
    content/theme.py). `theme["bg"]` (solid) still goes to
    `Site(bg=...)` in site.py, so `html`/`body` have a sane, correctly-
    typed background the instant the page loads -- before this wrapper
    even exists in the DOM -- and the gradient repaints over it a beat
    later with the richer surface the frosted-glass cards need behind
    them to actually read as translucent.
    """
    return {
        "--ark-accent": theme["accent"],
        "--ark-accent-hover": theme["accent_hover"],
        "--ark-border": theme["border"],
        "background": theme["bg_gradient"],
        "margin": "-2.5rem -1.5rem -4rem",
        "padding": "2.5rem 1.5rem 4rem",
    }
