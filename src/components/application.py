
from functools import cached_property
from typing import Any

from tkinter import *
from tkinter import ttk

from src.components.display import Display
from src.components.keyboard import Keyboard

from src.services.calculator_service import CalculatorService


class Application(Tk):

    @cached_property
    def calculator(self) -> CalculatorService:
        return CalculatorService()

    @cached_property
    def display(self) -> Display:
        return Display(master=self)

    @cached_property
    def keyboard(self) -> Keyboard:
        return Keyboard(master=self)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        style = ttk.Style(master=self)

        style.configure('TButton', font=('Arial', 16))

        style.configure('clear.TButton', foreground='red')
        style.configure('calculate.TButton', foreground='blue')

        self.geometry(newGeometry='500x700')
        self.title(string='Calculator')

        self.rowconfigure(index=0, weight=0)
        self.rowconfigure(index=1, weight=1)

        self.columnconfigure(index=0, weight=1)

        self.display.grid(row=0, column=0, sticky='nsew')
        self.keyboard.grid(row=1, column=0, sticky='nsew')
