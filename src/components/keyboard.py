
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tkinter import *
from tkinter import ttk

from src.services.calculator_service import Token

from .button import BackspaceButton, CalculateButton, ClearButton, SendTokenButton, ToggleModeButton

if TYPE_CHECKING:
    from src.components.application import Application


class Keyboard(Frame):

    @property
    def number_of_rows(self) -> int:
        return 6 if self.master.calculator.scientific_mode else 5

    @property
    def number_of_columns(self) -> int:
        return 5 if self.master.calculator.scientific_mode else 4

    def __init__(self, master: Application, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, master=master, **kwargs)
        self._create_layout()

    def _create_layout(self) -> None:
        # Clear existing buttons
        for widget in self.winfo_children():
            widget.destroy()

        if self.master.calculator.scientific_mode:
            buttons: list[ttk.Button] = [
                # first row
                ToggleModeButton(application=self.master, master=self),
                SendTokenButton(application=self.master, token=Token.sin, master=self),
                SendTokenButton(application=self.master, token=Token.cos, master=self),
                SendTokenButton(application=self.master, token=Token.tan, master=self),
                SendTokenButton(application=self.master, token=Token.sqrt, master=self),

                # second row
                ClearButton(application=self.master, text='C', master=self),
                SendTokenButton(application=self.master, token=Token.log, master=self),
                SendTokenButton(application=self.master, token=Token.ln, master=self),
                SendTokenButton(application=self.master, token=Token.exp, master=self),
                SendTokenButton(application=self.master, token=Token.power, master=self),

                # third row
                SendTokenButton(application=self.master, token=Token.seven, master=self),
                SendTokenButton(application=self.master, token=Token.eight, master=self),
                SendTokenButton(application=self.master, token=Token.nine, master=self),
                SendTokenButton(application=self.master, token=Token.divide, master=self),
                BackspaceButton(application=self.master, text='⌫', master=self),

                # fourth row
                SendTokenButton(application=self.master, token=Token.four, master=self),
                SendTokenButton(application=self.master, token=Token.five, master=self),
                SendTokenButton(application=self.master, token=Token.six, master=self),
                SendTokenButton(application=self.master, token=Token.multiply, master=self),
                SendTokenButton(application=self.master, token=Token.parenthesis, master=self),

                # fifth row
                SendTokenButton(application=self.master, token=Token.one, master=self),
                SendTokenButton(application=self.master, token=Token.two, master=self),
                SendTokenButton(application=self.master, token=Token.three, master=self),
                SendTokenButton(application=self.master, token=Token.minus, master=self),
                SendTokenButton(application=self.master, token=Token.pi, master=self),

                # sixth row
                SendTokenButton(application=self.master, token=Token.negate, master=self),
                SendTokenButton(application=self.master, token=Token.zero, master=self),
                SendTokenButton(application=self.master, token=Token.decimal, master=self),
                SendTokenButton(application=self.master, token=Token.plus, master=self),
                CalculateButton(application=self.master, text='=', master=self),
            ]
        else:
            buttons: list[ttk.Button] = [
                # first row
                ToggleModeButton(application=self.master, master=self),
                ClearButton(application=self.master, text='C', master=self),
                BackspaceButton(application=self.master, text='⌫', master=self),
                SendTokenButton(application=self.master, token=Token.parenthesis, master=self),

                # second row
                SendTokenButton(application=self.master, token=Token.seven, master=self),
                SendTokenButton(application=self.master, token=Token.eight, master=self),
                SendTokenButton(application=self.master, token=Token.nine, master=self),
                SendTokenButton(application=self.master, token=Token.divide, master=self),

                # third row
                SendTokenButton(application=self.master, token=Token.four, master=self),
                SendTokenButton(application=self.master, token=Token.five, master=self),
                SendTokenButton(application=self.master, token=Token.six, master=self),
                SendTokenButton(application=self.master, token=Token.multiply, master=self),

                # fourth row
                SendTokenButton(application=self.master, token=Token.one, master=self),
                SendTokenButton(application=self.master, token=Token.two, master=self),
                SendTokenButton(application=self.master, token=Token.three, master=self),
                SendTokenButton(application=self.master, token=Token.minus, master=self),

                # fifth row
                SendTokenButton(application=self.master, token=Token.negate, master=self),
                SendTokenButton(application=self.master, token=Token.zero, master=self),
                SendTokenButton(application=self.master, token=Token.decimal, master=self),
                SendTokenButton(application=self.master, token=Token.plus, master=self),
            ]
            # Add calculate button for basic mode
            buttons.append(CalculateButton(application=self.master, text='=', master=self))

        for row in range(self.number_of_rows):
            self.rowconfigure(index=row, weight=1)

        for column in range(self.number_of_columns):
            self.columnconfigure(index=column, weight=1)

        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                idx = (self.number_of_columns * row) + column
                if idx < len(buttons):
                    buttons[idx].grid(row=row, column=column, sticky='nsew')

    def refresh_layout(self) -> None:
        self._create_layout()
