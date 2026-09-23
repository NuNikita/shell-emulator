import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    vfs_path: str
    prompt: str
    script_path: str | None


def parse_arguments(arguments: list[str] | None = None) -> Config:
    parser = argparse.ArgumentParser(
        description="Графический эмулятор командной строки"
    )
    parser.add_argument(
        "--vfs",
        default=".",
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--prompt",
        default="$ ",
        help="пользовательское приглашение к вводу",
    )
    parser.add_argument(
        "--script",
        help="путь к стартовому скрипту",
    )
    namespace = parser.parse_args(arguments)

    return Config(
        vfs_path=namespace.vfs,
        prompt=namespace.prompt,
        script_path=namespace.script,
    )
