import sys

import spacy
import typer

Arg = typer.Argument
Opt = typer.Option

# StdInArg argument is copied from:
# https://github.com/tiangolo/typer/issues/345#issuecomment-1297432321
StdInArg = Arg(... if sys.stdin.isatty() else sys.stdin.read().strip())


def parse_message(msg: str) -> dict:
    nlp = spacy.load("en_helpner")
    doc = nlp(msg)
    {"message": "text", "annotations": [("LABEL", "start", "end"), ...]}
    return doc
