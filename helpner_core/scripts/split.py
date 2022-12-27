"""Splits a dataset between train/test. """

import typer
from pathlib import Path

import pandas as pd


def main(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    frac: float = typer.Option(0.8, help="Fraction of data to use for training."),
):
    df = pd.read_json(input_path, lines=True)

    df_train = df.iloc[: int(frac * len(df)), :]
    df_dev = df.iloc[-(len(df) - int(frac * len(df))) :, :]

    path_train = input_path.parent / f"{input_path.stem}_train{input_path.suffix}"
    path_dev = input_path.parent / f"{input_path.stem}_dev{input_path.suffix}"

    df_train.to_json(path_train, orient="records", lines=True)
    df_dev.to_json(path_dev, orient="records", lines=True)
    print(f"Data generated at: \n- {path_train} \n- {path_dev}")


if __name__ == "__main__":
    typer.run(main)
