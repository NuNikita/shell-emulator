import shlex
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    output: str = ""
    should_exit: bool = False
    is_error: bool = False


def execute(line: str) -> CommandResult:
    try:
        parts = shlex.split(line, posix=True)
    except ValueError as error:
        return CommandResult(f"Ошибка синтаксиса: {error}", is_error=True)

    if not parts:
        return CommandResult()

    name, *arguments = parts
    if name == "exit":
        if arguments:
            return CommandResult(
                "exit: аргументы не поддерживаются", is_error=True
            )
        return CommandResult(should_exit=True)
    if name in ("ls", "cd"):
        return CommandResult(f"{name}: аргументы: {arguments}")
    return CommandResult(f"{name}: команда не найдена", is_error=True)
