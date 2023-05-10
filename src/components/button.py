
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tkinter import *
from tkinter import ttk

from src.services.calculator_service import Token

if TYPE_CHECKING:
    from src.components.application import Application


class CalculateButton(ttk.Button):

    def __init__(self, *args: Any, application: Application, token: Token, **kwargs: Any) -> None:

        def command() -> None:
            application.display.set_result_label_text(text=application.calculator.evalutate_expression())

        super().__init__(*args, text=token.value, style='calculate.TButton', command=command, **kwargs)


class ClearButton(ttk.Button):

    def __init__(self, *args: Any, application: Application, token: Token, **kwargs: Any) -> None:

        def command() -> None:
            application.calculator.clear_expression()
            application.display.set_current_expression_label_text(text=application.calculator.get_expression())
            application.display.set_result_label_text(text=application.calculator.evalutate_expression())

        super().__init__(*args, text=token.value, style='clear.TButton', command=command, **kwargs)


class SendTokenButton(ttk.Button):
    def __init__(self, *args: Any, application: Application, token: Token, **kwargs: Any) -> None:

        def command() -> None:
            application.calculator.send_token(token=token)
            application.display.set_current_expression_label_text(text=application.calculator.get_expression())
            application.display.set_result_label_text(text=application.calculator.evalutate_expression())

        super().__init__(*args, text=token.value, command=command, **kwargs)
