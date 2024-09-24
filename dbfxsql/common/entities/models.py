import click
from dataclasses import dataclass
from importlib import import_module
from functools import cached_property
from watchfiles import Change, DefaultFilter


@dataclass(frozen=True, slots=True)
class Filter:
    field: str
    operator: str
    value: str

    def __str__(self) -> str:
        return f"{self.field} {self.operator} {self.value}"


@dataclass
class Watcher(DefaultFilter):
    allowed_extensions: tuple[str] = (".dbf", ".sql")

    def __call__(self, change: Change, path: str) -> bool:
        return (
            super().__call__(change, path)
            and change == Change.modified
            and path.endswith(self.allowed_extensions)
        )


class OrderCommands(click.Group):
    def list_commands(self, ctx: click.Context) -> list[str]:
        return self.commands


class LazyGroup(click.Group):
    """
    A click Group that imports the actual implementation only when
    needed.  This allows for more resilient CLIs where the top-level
    command does not fail when a subcommand is broken enough to fail
    at import time.
    """

    def __init__(self, import_name: str, **kwargs: any) -> None:
        self._import_name: str = import_name
        super().__init__(**kwargs)

    @cached_property
    def _impl(self) -> click.Group:
        module, name = self._import_name.split(":", 1)
        return getattr(import_module(module), name)

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        return self._impl.get_command(ctx, cmd_name)

    def list_commands(self, ctx: click.Context) -> list[str]:
        return self._impl.list_commands(ctx)

    def invoke(self, ctx: click.Context) -> None:
        return self._impl.invoke(ctx)

    def get_usage(self, ctx: click.Context) -> str:
        return self._impl.get_usage(ctx)

    def get_params(self, ctx: click.Context) -> list[click.Parameter]:
        return self._impl.get_params(ctx)
