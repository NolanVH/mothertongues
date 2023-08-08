import json
from enum import Enum
from pathlib import Path

import typer

from mothertongues.config.models import MTDConfiguration
from mothertongues.dictionary import MTDictionary
from mothertongues.utils import load_mtd_configuration

app = typer.Typer()


class OutputFormat(str, Enum):
    json = "json"
    js = "js"


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def export(
    language_config_path: Path = typer.Argument(
        default=None, exists=True, file_okay=True, dir_okay=False, readable=True
    ),
    output_format: OutputFormat = typer.Option(OutputFormat.js),
):
    config = MTDConfiguration(**load_mtd_configuration(language_config_path))
    dictionary = MTDictionary(config)
    output = dictionary.export()
    if output_format == OutputFormat.json:
        with open("dictionary_data.json", "w", encoding="utf8") as f:
            json.dump(output, f)


if __name__ == "__main__":
    app()
