from __future__ import annotations

from arklight import Code, Container, Heading, Pre, Text

from components.layout import page_shell
from content.getting_started import CLI_REFERENCE, GETTING_STARTED_STEPS


def getting_started(theme: dict[str, str]):
    steps = [
        Container(
            Heading(step_title, level=3),
            Pre(Code(command)),
            Text(note, class_name="muted"),
            class_name="card",
        )
        for step_title, command, note in GETTING_STARTED_STEPS
    ]
    cli_reference = [
        Container(
            Heading(title, level=3),
            Pre(Code(command)),
            Text(note, class_name="muted"),
            class_name="card",
        )
        for title, command, note in CLI_REFERENCE
    ]
    return page_shell(
        Heading("Getting Started"),
        Text(
            "The exact commands from ARKlight's own README -- nothing "
            "paraphrased. This site itself was built by running these "
            "same five steps against the alpha branch.",
        ),
        Container(*steps, class_name="stack"),
        Heading("CLI reference -- beyond the five steps above", level=2),
        Text(
            "Independent commands a project reaches for as needed, "
            "not a linear sequence -- pulled directly from "
            "`arklight/cli/main.py`'s own --help text. One of these "
            "(the PWA install button) is flagged EXPERIMENTAL; see "
            "the FAQ for what that means and why.",
            class_name="muted",
        ),
        Container(*cli_reference, class_name="stack"),
        Heading("A minimal site.py", level=2),
        Pre(Code(
            "from arklight import *\n\n"
            "site = Site()\n\n"
            "@site.page(\"/\")\n"
            "def home():\n"
            "    return Page(\n"
            "        Heading(\"ARKlight\"),\n"
            "        Text(\"Build websites with Python.\"),\n"
            "        Button(\"Get Started\"),\n"
            "    )"
        )),
        Text(
            "The same shape every page on this site follows -- see the "
            "Methodology page for how this site's own numbers were "
            "measured, or the Changelog for what's shipped so far.",
            class_name="muted",
        ),
        title="Getting Started",
        description="Install ARKlight's alpha branch and build your first site -- the exact commands from ARKlight's own README.",
        theme=theme,
    )
