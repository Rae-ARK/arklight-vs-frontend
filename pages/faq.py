from __future__ import annotations

from arklight import Container, Details, Heading, Summary, Text

from components.layout import page_shell
from content.faq import FAQ


def faq(theme: dict[str, str]):
    entries = [
        Details(Summary(question), Text(answer), class_name="glass")
        for question, answer in FAQ
    ]
    return page_shell(
        Heading("FAQ"),
        Text(
            "Nothing new invented for this page -- every answer below "
            "is repackaged from this project's own README or existing "
            "copy elsewhere on this site, as a zero-JS Details/Summary "
            "accordion.",
        ),
        Container(*entries, class_name="stack"),
        title="FAQ",
        description="Answers to the honest edge cases found while building this site -- no live charts, @media gated as experimental, no PyPI package.",
        theme=theme,
    )
