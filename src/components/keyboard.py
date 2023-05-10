
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tkinter import *
from tkinter import ttk

from src.services.calculator_service import Token

from .button import BackspaceButton, CalculateButton, ClearButton, SendTokenButton

if TYPE_CHECKING:
    from src.components.application import Application


class Keyboard(Frame):

    @property
    def number_of_rows(self) -> int:
        return 5

    @property
    def number_of_columns(self) -> int:
        return 4

    def __init__(self, master: Application, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, master=master, **kwargs)

        buttons: list[ttk.Button] = [

            # first row
            ClearButton(application=master, text='C', master=self),
            BackspaceButton(application=master, text='⌫', master=self),
            SendTokenButton(application=master, token=Token.parenthesis, master=self),
            SendTokenButton(application=master, token=Token.divide, master=self),

            # second row
            SendTokenButton(application=master, token=Token.seven, master=self),
            SendTokenButton(application=master, token=Token.eight, master=self),
            SendTokenButton(application=master, token=Token.nine, master=self),
            SendTokenButton(application=master, token=Token.multiply, master=self),

            # third row
            SendTokenButton(application=master, token=Token.four, master=self),
            SendTokenButton(application=master, token=Token.five, master=self),
            SendTokenButton(application=master, token=Token.six, master=self),
            SendTokenButton(application=master, token=Token.minus, master=self),

            # fourth row
            SendTokenButton(application=master, token=Token.one, master=self),
            SendTokenButton(application=master, token=Token.two, master=self),
            SendTokenButton(application=master, token=Token.three, master=self),
            SendTokenButton(application=master, token=Token.plus, master=self),

            # fifth row
            SendTokenButton(application=master, token=Token.negate, master=self),
            SendTokenButton(application=master, token=Token.zero, master=self),
            SendTokenButton(application=master, token=Token.decimal, master=self),
            CalculateButton(application=master, text='=', master=self),

        ]

        for row in range(self.number_of_rows):
            self.rowconfigure(index=row, weight=1)

        for column in range(self.number_of_columns):
            self.columnconfigure(index=column, weight=1)

        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                buttons[(self.number_of_columns * row) + column].grid(row=row, column=column, sticky='nsew')
