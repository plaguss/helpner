"""Module containing functions to highlight a help message.

Visit 
[colors](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors)
to select the colors 
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console(record=True)

default_styles = {
    "CMD": "black on orchid",
    "ARG": "black on deep_sky_blue1",
    "OPT": "black on chartreuse3",
}


def highlight_message(
    msg: str,
    labels: list[tuple[str, int, int]],
    styles: dict[str, str] = default_styles,
    save_svg: bool = False,
    svg_filename: str = "program-help.svg",
) -> None:  # pragma: no cover, tested by rich
    """Highlights a help message with the annotations obtained from the model.

    Args:
        msg (str):
            The help message from the program.
        labels list[tuple[str, int, int]]:
            Annotations obtained from the NER model.
        styles dict[str, str]:
            Styles to be passed to rich, for different types of colors.
        save_svg (bool): Whether to save the console output as svg.
            Visit https://rich.readthedocs.io/en/stable/console.html#exporting-svgs
            for more info. Defaults to False.
        svg_filename (str): Name of the svg file. Defaults to program-help.svg
    """
    text = Text(msg)
    for label, start, end in labels:
        text.stylize(styles[label], start=start, end=end)

    console.print(
        Panel.fit(text, title="[white]Program help[/white]", border_style="red")
    )
    legend = _add_legend(styles)
    console.print(legend)
    if save_svg:
        console.save_svg(svg_filename, title="Helpner")


def _add_legend(
    styles: dict[str, str] = default_styles
) -> Panel:  # pragma: no cover, tested by rich
    """Adds a rich panel with a legend for every color."""
    text = "  ".join([f"- [{v}]{k}[/{v}]" for k, v in styles.items()])
    legend = Panel.fit(text, title="[white]Legend[/white]", border_style="red")
    return legend
