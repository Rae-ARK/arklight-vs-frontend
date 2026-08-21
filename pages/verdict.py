from __future__ import annotations

from arklight import Details, Heading, Summary, Text

from components.layout import page_shell


def verdict(theme: dict[str, str]):
    return page_shell(
        Heading("The Honest Verdict"),
        Text(
            "ARKlight and React/Vue/Svelte/Angular are not really "
            "competing for the same job. One question below decides "
            "which category actually applies to you.",
        ),
        Details(
            Summary("Do you need client-side interactivity beyond clicks toggling things?"),
            Text(
                "If yes -- forms with live validation, drag-and-drop, "
                "real-time dashboards -- a traditional framework is the "
                "right tool. ARKlight's JS is a closed, named vocabulary "
                "by design, not a smaller version of a full runtime.",
            ),
            class_name="glass",
        ),
        Details(
            Summary("Is your team already fluent in JS/TS and an existing framework?"),
            Text(
                "If yes, switching costs likely outweigh ARKlight's "
                "benefits today -- it's a young, single-maintainer "
                "project without React/Vue/Svelte's ecosystem.",
            ),
            class_name="glass",
        ),
        Details(
            Summary("Do you write Python, need a handful of static pages, and want zero npm toolchain?"),
            Text(
                "This is ARKlight's actual sweet spot: docs stubs, "
                "internal tools, a landing page templated out of a "
                "script, teaching contexts. Genuinely pleasant there.",
            ),
            class_name="glass",
        ),
        title="The Honest Verdict",
        description="Who should actually use ARKlight, and who shouldn't -- a direct recommendation.",
        theme=theme,
    )
