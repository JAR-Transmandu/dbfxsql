import tomllib
from decouple import config
from pathlib import Path


def generate_filepath(filename: str, database: str) -> str:
    """Generates a filepath based on the filename and database."""

    filename += f".{database}"

    filepaths: dict[str, str] = {
        "dbf": config("DBF_FOLDERPATH") + filename,
        "sql": config("SQL_FOLDERPATH") + filename,
    }

    return filepaths[database]


def filepath_exists(filepath: str) -> None:
    return Path(filepath).exists()


def decompose_filename(file: str) -> tuple[str, str]:
    """Decomposes a filename into its stem and suffix."""

    return Path(file).stem, Path(file).suffix.removeprefix(".")


def create_file(filepath: str) -> None:
    Path(filepath).touch()


def delete_file(filepath: str) -> None:
    Path(filepath).unlink()


def load_toml() -> dict:
    filepath: Path = Path(config("CONFIG_FOLDERPATH")) / "config.toml"

    if not filepath.exists():
        filepath.touch()

    with open(filepath, "rb") as file:
        toml_data: dict = tomllib.load(file)

        return toml_data
