import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

from src.shell import execute


def window_title() -> str:
    return f"Эмулятор - [{getpass.getuser()}@{socket.gethostname()}]"


class EmulatorWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title(window_title())
        root.geometry("760x480")

        self.history = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state=tk.DISABLED
        )
        self.history.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(input_frame, text="$ ").pack(side=tk.LEFT)
        self.entry = tk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.submit)
        self.entry.focus_set()
        self._write("Эмулятор, этап 1. Команды: ls, cd, exit.\n")

    def _write(self, message: str) -> None:
        self.history.configure(state=tk.NORMAL)
        self.history.insert(tk.END, message)
        self.history.configure(state=tk.DISABLED)
        self.history.see(tk.END)

    def submit(self, _event: tk.Event) -> None:
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._write(f"$ {line}\n")
        result = execute(line)
        if result.output:
            self._write(f"{result.output}\n")
        if result.should_exit:
            self.root.destroy()


def main() -> None:
    root = tk.Tk()
    EmulatorWindow(root)
    root.mainloop()
