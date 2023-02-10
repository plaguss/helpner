import sys
from typing import TypedDict

import spacy
import typer
from spacy.tokens.span import Span

Arg = typer.Argument
Opt = typer.Option

HELPNER_MODEL = "en_helpner_core"

# StdInArg argument is copied from:
# https://github.com/tiangolo/typer/issues/345#issuecomment-1297432321
StdInArg = Arg(
    ... if sys.stdin.isatty() else sys.stdin.read().strip(),
    help="Command line help message.",
)

Annotations = list[tuple[str, int, int]]
ParsedMessage = TypedDict(
    "ParsedMessage",
    {"message": str, "entities": tuple[Span, ...], "labels": Annotations},
)


def _process_message(msg: str) -> tuple[Span, ...]:  # pragma: no cover
    """Load the spacy model, process the text and return the entities.

    Args:
        msg (str): A help message from a cli.

    Returns:
        tuple: It returns a tuple with the entities (if any)
    """
    # This function is to simplify the testing only.
    try:
        nlp = spacy.load(HELPNER_MODEL)
    except OSError as e:
        raise ValueError(
            "The model couldn't be found, try running `helpner download` first"
        ) from e
    return nlp(msg).ents


def parse_message(msg: str) -> ParsedMessage:
    """Processes a string message (its expected to be the result of
    calling from the console a help message, i.e. `git add -h` or
    `pip install --help`).

    Args:
        msg (str): A help message from a cli.

    Returns:
        dict (ParsedMessage): Dict containing the
            original message, entities obtained from spacy
            and a list of tuples with the labels.
    """
    entities = _process_message(msg)
    return {
        "message": msg,
        "entities": entities,
        "labels": [(ent.label_, ent.start_char, ent.end_char) for ent in entities],
    }
