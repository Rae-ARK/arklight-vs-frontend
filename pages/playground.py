from __future__ import annotations

from arklight import Action, Bind, Button, Container, Heading, State, Text

from components.cards import card_class, card_grid
from components.layout import page_shell
from content.playground import COUNTER_INITIAL, PLAYGROUND_CARDS


def _framework_card(key: str, name: str, summary: str, detail: str, is_hero: bool):
    """
    One independent expand/collapse card's *visual* half. The matching
    State(...) declaration is NOT built here -- see playground() below
    for why every State(...) on this page is hoisted to page_shell's
    state= param instead of living next to the markup that uses it.

    Deliberately not a mutually-exclusive tab switcher (see
    content/faq.py's "Can one on_click fire more than one Action?"
    entry, and PLAN.md Section 9) -- on_click only ever fires a single
    Action, so cross-card coordination ("clicking one collapses the
    others") isn't expressible today. Each card gets its own
    independent State instead, verified against what
    Action.toggle_bool/Bind.when actually do, not simulated.
    """
    state_key = f"show_detail_{key}"
    return Container(
        Heading(name, level=3),
        Text(summary, class_name="muted"),
        Button("Toggle details", on_click=Action.toggle_bool(state_key), class_name="pill"),
        Container(
            Text(detail),
            class_name="playground-panel",
            bind_class=Bind.when(state_key, "playground-panel-open"),
        ),
        class_name=card_class(is_hero=is_hero),
    )


def _counter_demo():
    return Container(
        Heading("Live counter", level=2),
        Text(
            "A minimal example: three buttons mutate one page-scoped "
            "State, and the number below updates live via Bind -- no "
            "page reload, no client-side framework, ~6 KB of shipped "
            "JS total for this whole page (see Bundle Size).",
            class_name="muted",
        ),
        Heading(Bind("count"), level=3, class_name="kpi-value"),
        Container(
            Button("-1", on_click=Action.decrement("count"), class_name="pill"),
            Button("Reset", on_click=Action.reset("count"), class_name="pill"),
            Button("+1", on_click=Action.increment("count"), class_name="pill"),
            class_name="cluster",
        ),
        class_name="card",
    )


def playground(theme: dict[str, str]):
    # Every State(...) on this page, collected in one place and handed
    # to page_shell's state= param -- see components/layout.py's
    # page_shell docstring for why this can't just be built next to
    # the markup that references it (ARKlight requires State(...) to
    # be a literal direct child of Page(...), confirmed directly
    # against arklight/ir/validate.py, not something page_shell's own
    # Main()/Container() wrapping can satisfy).
    page_state = [State(f"show_detail_{key}", False) for key, *_ in PLAYGROUND_CARDS]
    page_state.append(State("count", COUNTER_INITIAL))

    cards = card_grid(*[_framework_card(*card) for card in PLAYGROUND_CARDS])

    return page_shell(
        Heading("Playground"),
        Text(
            "Everything on this page is real, page-compiled State/Bind/"
            "Action interactivity -- not a mockup. Expand a card below "
            "(each one toggles independently), or try the counter.",
        ),
        Heading("Framework cards -- independent expand/collapse", level=2),
        cards,
        _counter_demo(),
        title="Playground",
        description="A live State/Bind/Action demo -- expandable cards and a counter, running entirely on ARKlight's closed-vocabulary JS runtime.",
        theme=theme,
        state=page_state,
    )
