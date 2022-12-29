
import sys

import spacy
from spacy.tokens.span import Span
import typer

Arg = typer.Argument
Opt = typer.Option

HELPNER_MODEL = "en_helpner"

# StdInArg argument is copied from:
# https://github.com/tiangolo/typer/issues/345#issuecomment-1297432321
StdInArg = Arg(... if sys.stdin.isatty() else sys.stdin.read().strip(), help="Command line help message.")

Annotations = dict[str, tuple[str, int, int]]

def _process_message(msg: str) -> tuple[None] | tuple[Span, ...]:
    """Load the spacy model, process the text and return the entities.

    Args:
        msg (str): A help message from a cli.

    Returns:
        tuple: It returns a tuple with the entities (if any)
    """
    # This function is to simplify the testing only.
    nlp = spacy.load(HELPNER_MODEL)
    return nlp(msg).ents


def parse_message(msg: str) -> dict[str, str | Annotations]:
    """Processes a string message (its expected to be the result of
    calling from the console a help message, i.e. `git add -h` or
    `pip install --help`).

    Args:
        msg (str): A help message from a cli.

    Returns:
        dict (dict[str, str | Annotations]): Dict containing the
            original message and a list of tuples with the labels.
    """
    # TODO: Check if the model was properly installed/downloaded
    entities = _process_message(msg)
    return {
        "message": msg,
        "entities": entities,
        "labels": [(ent.label_, ent.start_char, ent.end_char) for ent in entities],
    }
