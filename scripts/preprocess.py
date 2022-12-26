"""Script to transform the a dataset in jsonl to a DocBin.

Copied from the spacy tutorials:
https://spacy.io/usage/training#training-data
https://github.com/explosion/projects/blob/v3/tutorials/ner_fashion_brands/scripts/preprocess.py
"""

import typer
import srsly
from pathlib import Path
from spacy.tokens import DocBin
import spacy


def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output_path: Path = typer.Argument(..., dir_okay=False),
):
    nlp = spacy.blank("en")
    doc_bin = DocBin()
    i = 0
    for eg in srsly.read_jsonl(input_path):

        doc = nlp(eg["message"])

        if doc is None:
            raise ValueError("??")
        ents = []
        for label, start, end in eg["annotations"]:
            ents.append(doc.char_span(start, end, label=label))

        if len(ents) > 0:
            try:
                doc.ents = ents
            except TypeError:
                print(f"Message i={i} can't be created, review cli_help_maker generator.")
                continue

        doc_bin.add(doc)
        i += 1

    doc_bin.to_disk(output_path)
    print(f"Processed {len(doc_bin)} documents: {output_path.name}")


if __name__ == "__main__":
    typer.run(main)
