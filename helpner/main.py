"""Command Line Interface for helpner. """

import typer
from rich import print, print_json
from .highlight import default_styles, highlight_message
from .utils import Opt, StdInArg, parse_message
from rich import print_json
from download import download_model

app = typer.Typer()


@app.command()
def parse(
    help_message: str = StdInArg,
    json: bool = Opt(
        True,
        help="Print the content as a json or as a dict. May be handy to write the content to a file.",
    ),
) -> None:
    """Program to parse a CLI help message and determine the positions of
    Commands, Arguments and Options.
    """
    parsed = parse_message(help_message)
    content = {k: v for k, v in zip(parsed["entities"], parsed["labels"])}

    if len(content) == 0:
        print("Nothing was found")
        raise typer.Exit()

    if json:
        print_json(json.dumps(content))
    else:
        print(content)


@app.command()
def highlight(
    help_message: str = StdInArg,
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
    annotations = parse_message(help_message)
    styles = {
        "CMD": style_cmd,
        "ARG": style_arg,
        "OPT": style_opt,
    }
    return highlight_message(
        annotations["message"], annotations["labels"], styles=styles
    )


@app.command()
def download() -> None:
    download_model()


if __name__ == "__main__":
    app()
