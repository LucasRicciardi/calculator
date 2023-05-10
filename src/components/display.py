
from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

from tkinter import *
from tkinter import font, ttk

if TYPE_CHECKING:
    from src.components.application import Application

CURRENT_EXPRESSION_LABEL_FONT_SIZE: int = 16
RESULT_LABEL_FONT_SIZE: int = 32

DEFAULT_LABEL_PADDING: tuple[int, int, int, int] = (10, 10, 10, 10)


class Display(Frame):

    @cached_property
    def current_expression_label(self) -> ttk.Label:
        return ttk.Label(master=self, text='', anchor='e', font=font.Font(size=CURRENT_EXPRESSION_LABEL_FONT_SIZE), padding=DEFAULT_LABEL_PADDING)

    @cached_property
    def result_label(self) -> ttk.Label:
        return ttk.Label(master=self, text='0', anchor='e', font=font.Font(size=RESULT_LABEL_FONT_SIZE), padding=DEFAULT_LABEL_PADDING)

    def __init__(self, master: Application, *args: Any, **kwargs: Any) -> None:
        super().__init__(master=master, *args, **kwargs)

        self.rowconfigure(index=0, minsize=CURRENT_EXPRESSION_LABEL_FONT_SIZE, weight=1)
        self.rowconfigure(index=1, minsize=RESULT_LABEL_FONT_SIZE, weight=1)

        self.columnconfigure(index=0, weight=1)

        self.current_expression_label.grid(row=0, column=0, sticky='nsew')
        self.result_label.grid(row=1, column=0, sticky='nsew')

    def set_current_expression_label_text(self, text: str) -> None:
        self.current_expression_label.config(text=text)

    def set_result_label_text(self, text: str) -> None:
        self.result_label.config(text=text)
