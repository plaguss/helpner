"""_summary_

Visit [standard colors](https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors)
to select the colors 
"""

from rich.console import Console
from rich.text import Text

console = Console()

default_styles = {
    "CMD": "black on orchid",
    "ARG": "black on deep_sky_blue1",
    "OPT": "black on chartreuse3",
}


def highlight_message(
    msg: str,
    labels: list[tuple[str, int, int]],
    styles: dict[str, str] = default_styles,
) -> None:
    """Highlights a help message with the annotations obtained from the model.

    Args:
        msg (str): _description_
        annotations (dict): _description_
    """
    text = Text(msg)
    for label, start, end in labels:
        text.stylize(styles[label], start=start, end=end)

    console.print(text)
    # TODO: Add a panel with a legend
