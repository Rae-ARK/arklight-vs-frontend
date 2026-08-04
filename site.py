"""
Composition root.

This is the only file ARKlight's static discovery
(arklight.parser.discover) actually reads to find `Site()` and
`@<site_var>.page("/route")` decorators -- see pages/__init__.py and
content/routes.py for why that means route registration can't live
inside pages/ itself, no matter how tempting it is to put
`@site.page(...)` next to each page function. Every decorated function
below is a thin, zero-argument shim: discovery only needs to *see* the
decorator here, the real page logic still lives in pages/, built from
content/ + components/ + services/ exactly as the rest of this split
already does.

Kept in the order content.routes.ROUTES lists them, and checked against
that list at import time (see the bottom of this file) -- ROUTES drives
components.layout.nav() independently of the decorators here, and
nothing in ARKlight itself keeps the two in sync automatically (see
content/routes.py's own docstring).
"""

from arklight import Site

import pages.adoption
import pages.architecture
import pages.bundle_size
import pages.changelog
import pages.faq
import pages.getting_started
import pages.home
import pages.methodology
import pages.playground
import pages.verdict
from content.routes import ROUTES
from content.theme import THEME
from services.compatibility import check_arklight_compatibility
from services.styles import register_site_styles

check_arklight_compatibility()

site = Site(bg=THEME["bg"])
register_site_styles(site, THEME)


@site.page("/")
def home():
    return pages.home.home(THEME)


@site.page("/bundle-size")
def bundle_size():
    return pages.bundle_size.bundle_size(THEME)


@site.page("/adoption")
def adoption():
    return pages.adoption.adoption(THEME)


@site.page("/architecture")
def architecture():
    return pages.architecture.architecture(THEME)


@site.page("/methodology")
def methodology():
    return pages.methodology.methodology(THEME)


@site.page("/verdict")
def verdict():
    return pages.verdict.verdict(THEME)


@site.page("/getting-started")
def getting_started():
    return pages.getting_started.getting_started(THEME)


@site.page("/changelog")
def changelog():
    return pages.changelog.changelog(THEME)


@site.page("/faq")
def faq():
    return pages.faq.faq(THEME)


@site.page("/playground")
def playground():
    return pages.playground.playground(THEME)


# --------------------------------------------------------------------
# content/routes.py warns that ROUTES (nav()'s source of truth) and the
# @site.page(...) decorators above (ARKlight's source of truth) have to
# be kept consistent by hand -- nothing here enforces it for you. Catch
# a drift between the two at import time, before a stale nav link or an
# orphaned route ships silently.
_registered_routes = set(site.routes.keys())
_nav_routes = {route for route, _label in ROUTES}
assert _registered_routes == _nav_routes, (
    "content.routes.ROUTES and site.py's @site.page(...) decorators "
    f"disagree: {_registered_routes.symmetric_difference(_nav_routes)}"
)
