import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext
from src.config import Config
from pathlib import Path

from src.shell import execute


def window_title() -> str:
    return f"Эмулятор - [{getpass.getuser()}@{socket.gethostname()}]"


class EmulatorWindow:
    def __init__(self, root: tk.Tk, config: Config) -> None:
        self.root = root
        self.config = config
        root.title(window_title())
        root.geometry("760x480")

        self.history = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED
        )
        self.history.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(10, 5),
        )

        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            input_frame,
            text=config.prompt,
        ).pack(side=tk.LEFT)

        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()

        self._write_config()
        self._write("Эмулятор, этап 2. Команды: ls, cd, exit.\n")
        if config.script_path is not None:
            root.after(0, self._run_startup_script)

    def _write(self, message: str) -> None:
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, message)
        self.history.configure(state=tk.DISABLED)
        self.history.see(tk.END)

    def _write_config(self) -> None:
        script_path = self.config.script_path or "не указан"
        message = (
            "Параметры запуска:\n"
            f"VFS: {self.config.vfs_path}\n"
            f"Приглашение: {self.config.prompt!r}\n"
            f"Стартовый скрипт: {script_path}\n\n"
        )
        self._write(message)


    def submit(self, _event: tk.Event) -> None:
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._execute_line(line)

    def _execute_line(self, line: str) -> bool:
        self._write(f"{self.config.prompt}{line}\n")
        result = execute(line)

        if result.output:
            self._write(f"{result.output}\n")

        if result.should_exit:
            self.root.destroy()

        return not result.is_error

    def _run_startup_script(self) -> None:
        script_path = Path(self.config.script_path or "")

        try:
            lines = script_path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            self._write(f"Ошибка стартового скрипта: {error}\n")
            return

        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            if line.strip() == "exit":
                self._execute_line(line)
                return
            if not self._execute_line(line):
                self._write(
                    "Выполнение стартового скрипта остановлено: "
                    f"ошибка в строке {line_number}.\n"
                )
                return


def main(config: Config) -> None:
    root = tk.Tk()
    EmulatorWindow(root, config)
    root.mainloop()
