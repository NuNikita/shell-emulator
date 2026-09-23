import unittest

from src.config import parse_arguments


class ConfigTests(unittest.TestCase):
    """Проверки параметров командной строки."""

    def test_default_arguments(self) -> None:
        """Парсер возвращает значения по умолчанию."""

        config = parse_arguments([])

        self.assertEqual(config.vfs_path, ".")
        self.assertEqual(config.prompt, "$ ")
        self.assertIsNone(config.script_path)

    def test_all_arguments(self) -> None:
        """Парсер принимает все параметры второго этапа."""

        config = parse_arguments(
            [
                "--vfs",
                "virtual_fs",
                "--prompt",
                "shell> ",
                "--script",
                "starttt.txt",
            ]
        )

        self.assertEqual(config.vfs_path, "virtual_fs")
        self.assertEqual(config.prompt, "shell> ")
        self.assertEqual(config.script_path, "starttt.txt")

    def test_unknown_argument(self) -> None:
        """Парсер отклоняет неизвестный параметр."""

        with self.assertRaises(SystemExit):
            parse_arguments(["--unknown", "value"])

    def test_argument_without_value(self) -> None:
        """Парсер отклоняет параметр без значения."""

        with self.assertRaises(SystemExit):
            parse_arguments(["--vfs"])

if __name__ == "__main__":
    unittest.main()