import unittest

from src.shell import execute


class ShellTests(unittest.TestCase):

    def test_stub_commands(self) -> None:
        """Заглушки показывают имя и аргументы."""
        self.assertEqual(execute("ls").output, "ls: аргументы: []")
        self.assertEqual(
            execute("cd folder").output, "cd: аргументы: ['folder']"
        )

    def test_quoted_arguments(self) -> None:
        """Пробелы внутри кавычек остаются частью аргумента."""
        self.assertEqual(
            execute('ls "my folder" \'two words\'').output,
            "ls: аргументы: ['my folder', 'two words']",
        )

    def test_exit(self) -> None:
        """Команда exit завершает сеанс только без аргументов."""
        self.assertTrue(execute("exit").should_exit)
        self.assertTrue(execute("exit now").is_error)


if __name__ == "__main__":
    unittest.main()
