"""Command Line Interface for helpner. """

import typer

from .highlight import default_styles, highlight_message
from .utils import Opt, StdInArg, parse_message

app = typer.Typer()


@app.command()
def parse(msg: str = StdInArg):
    """Program to parse a CLI help message and determine the positions of
    Commands, Arguments and Options.
    """
    print("hello:\n", msg)


@app.command()
def highlight(
    msg: str = StdInArg,
    style_cmd: str = Opt(default=default_styles["CMD"]),
    style_arg: str = Opt(default=default_styles["ARG"]),
    style_opt: str = Opt(default=default_styles["OPT"]),
) -> None:
    """
    The colors are directly passed to rich as a string style:
    https://rich.readthedocs.io/en/stable/style.html.
    A guide for the colors can be seen at rich: 
    https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
    """
    annotations = parse_message(msg)
    styles = {
        "CMD": style_cmd,
        "ARG": style_arg,
        "OPT": style_opt,
    }
    return highlight_message(
        annotations["message"], annotations["labels"], styles=styles
    )


if __name__ == "__main__":
    app()
