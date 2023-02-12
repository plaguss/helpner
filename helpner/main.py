"""Command Line Interface for helpner. """

import typer
from rich import print, print_json

from .download import download_model
from .highlight import default_styles, highlight_message
from .utils import Opt, StdInArg, parse_message

app = typer.Typer()


@app.command()
def parse(
    help_message: str = StdInArg,
    json: bool = Opt(
        True,
        help="Print the content as a json or as a dict. May be handy to write "
        "the content to a file.",
    ),
) -> None:
    """Program to parse a CLI help message and determine the positions of
    Commands, Arguments and Options.
    """
    parsed = parse_message(help_message)
    content = {
        k.text: v for k, v in zip(parsed["entities"], parsed["labels"])  # type: ignore
    }

    if len(content) == 0:
        print("Nothing was found")
        raise typer.Exit()

    if json:
        import json as jsonlib

        print_json(jsonlib.dumps(content))
    else:
        print(content)


@app.command()
def highlight(
    help_message: str = StdInArg,
    style_cmd: str = Opt(
        default=default_styles["CMD"], help="rich style to be passed for CMD entitites"
    ),
    style_arg: str = Opt(
        default=default_styles["ARG"], help="rich style to be passed for ARG entitites"
    ),
    style_opt: str = Opt(
        default=default_styles["OPT"], help="rich style to be passed for ARG entitites"
    ),
    save_svg: bool = False,
    svg_filename: str = Opt(default="program-help.svg", help="Name of the svg file."),
) -> None:  # pragma: no cover
    """
    The colors are directly passed to rich as a string style:
    https://rich.readthedocs.io/en/stable/style.html.
    A guide for the colors can be seen at rich:
    https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
    """
    annotations = parse_message(help_message)
    styles = {
        "CMD": style_cmd,
        "ARG": style_arg,
        "OPT": style_opt,
    }
    return highlight_message(
        annotations["message"],
        annotations["labels"],
        styles=styles,
        save_svg=save_svg,
        svg_filename=svg_filename,
    )


@app.command()
def download() -> None:  # pragma: no cover
    """Download the spaCy model to start playing."""
    download_model()


if __name__ == "__main__":
    app()
