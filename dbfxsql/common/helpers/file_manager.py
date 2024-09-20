from pathlib import Path
from decouple import config
import tomllib


def load_toml() -> dict:
    filepath: Path = Path(config("CONFIG_FOLDERPATH")) / "config.toml"

    if not filepath.exists():
        filepath.touch()

    with open(filepath, "rb") as file:
        toml_data: dict = tomllib.load(file)
        return toml_data


def generate_filepath(filename: str, database: str) -> str:
    filename += f".{database}"

    filepath: dict[str, str] = {
        "dbf": config("DBF_FOLDERPATH") + filename,
        "sql": config("SQL_FOLDERPATH") + filename,
    }

    return filepath[database]


def filepath_exists(filepath: str) -> None:
    return Path(filepath).exists()


def create_file(filepath: str) -> None:
    Path(filepath).touch()


def delete_file(filepath: str) -> None:
    Path(filepath).unlink()


def decompose_file(file: str) -> tuple[str, str]:
    return Path(file).stem, Path(file).suffix.removeprefix(".")
