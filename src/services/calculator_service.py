
from dataclasses import MISSING, dataclass, field
from enum import StrEnum
from logging import Logger, getLogger
from typing import Optional, Self

logger: Logger = getLogger(name=__name__)


@dataclass
class ExpressionTreeNode:
    value: str = field(default=MISSING)
    left: Optional[Self] = field(default=None)
    right: Optional[Self] = field(default=None)


class Token(StrEnum):

    # Digits
    zero: str = '0'
    one: str = '1'
    two: str = '2'
    three: str = '3'
    four: str = '4'
    five: str = '5'
    six: str = '6'
    seven: str = '7'
    eight: str = '8'
    nine: str = '9'

    # Operators
    plus: str = '+'
    minus: str = '-'
    multiply: str = '*'
    divide: str = '/'
    negate: str = '+/-'

    # Other
    parenthesis: str = '()'
    decimal: str = ','


DIGIT_TOKENS: set[Token] = {token for token in Token if token.value.isdigit()}
OPERATORS_TOKENS: set[Token] = {Token.plus, Token.minus, Token.multiply, Token.divide}


class CalculatorService:

    def __init__(self) -> None:
        self.expression: list[str] = []
        self.last_result: float = 0.0

    @property
    def last_element(self) -> str:
        if len(self.expression) > 0:
            return self.expression[-1]
        return ''

    @property
    def number_of_open_parenthesis(self) -> int:
        number_of_open_parenthesis: int = 0
        for token in self.expression:
            if token == '(':
                number_of_open_parenthesis += 1
            elif token == ')':
                number_of_open_parenthesis -= 1
        return number_of_open_parenthesis

    def send_token(self, token: Token) -> None:
        if token == Token.parenthesis:
            if self.last_element == '':
                self.expression += ['(']
            elif self.last_element.isdigit():
                if self.number_of_open_parenthesis == 0:
                    self.expression += ['*', '(']
                else:
                    self.expression += [')']
            else:
                self.expression += ['(']
        elif token == Token.negate:
            if self.last_element.isdigit():
                last_digit_index: int = -1
                while self.expression[last_digit_index].isdigit() or self.expression[last_digit_index] == ',':
                    last_digit_index += -1
                    if last_digit_index == -len(self.expression):
                        break
                self.expression = self.expression[:last_digit_index-1] + '-(' + self.expression[last_digit_index:]
            elif self.last_element == '(':
                self.expression += ['-']
            else:
                self.expression += ['(-']
        elif token == Token.decimal:
            if self.last_element.isdigit():
                is_decimal_number: bool = False
                last_digit_index: int = -1
                while last_digit_index > -len(self.expression):
                    if self.expression[last_digit_index] == ',':
                        is_decimal_number = True
                        break
                    elif not self.expression[last_digit_index].isdigit():
                        break
                    last_digit_index += -1
                if is_decimal_number:
                    logger.warning(msg='That will result in a invalid expression')
                else:
                    self.expression += [',']
            else:
                self.expression = ['0', ',']
        elif token in DIGIT_TOKENS:
            if self.last_element == ')':
                self.expression += ['*', token.value]
            else:
                self.expression += [token.value]
        elif token in OPERATORS_TOKENS:
            if self.last_element == '' or self.last_element == '(':
                logger.warning(msg='That will result in a invalid expression')
            elif self.last_element in OPERATORS_TOKENS:
                self.expression[-1] = token.value
            else:
                self.expression += [token.value]

    def backspace_expression(self) -> None:
        if len(self.expression) > 0:
            self.expression.pop()

    def get_expression(self) -> str:
        return ''.join(self.expression)

    def evalutate_expression(self) -> int | float:
        try:
            if len(self.expression) == 0:
                self.last_result = 0.0
            else:
                self.last_result = self._evaluate_expression_tree(
                    node=self._postfix_to_tree(
                        postfix=self._infix_to_postfix(
                            infix=self.expression
                        )
                    )
                )
        except Exception as e:
            logger.warning(msg=f'Could not calculate result due to malformed expression. Reason: {e}')
        finally:
            return self._normalize_result(value=self.last_result)

    def clear_expression(self) -> None:
        self.expression = []

    def _normalize_result(self, value: float) -> int | float:
        return int(value) if value.is_integer() else value

    @staticmethod
    def _precedence(operator: str) -> int:
        if operator in {Token.plus, Token.minus}:
            return 1
        elif operator in {Token.multiply, Token.divide}:
            return 2
        else:
            return 3

    def _infix_to_postfix(self, infix: list[str]) -> list[str]:
        output_queue: list[str] = []
        operator_stack: list[str] = []

        for token in infix:
            if token.isdigit():
                output_queue.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            elif token in OPERATORS_TOKENS:
                operator_one: str = token
                while operator_stack and operator_stack[-1] in OPERATORS_TOKENS:
                    operator_two: str = operator_stack[-1]
                    if (self._precedence(operator_one) <= self._precedence(operator_two) and operator_one != '-') or (self._precedence(operator_one) < self._precedence(operator_two) and operator_one == '-'):
                        output_queue.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    @staticmethod
    def _postfix_to_tree(postfix: list[str]) -> ExpressionTreeNode:
        stack: list[ExpressionTreeNode] = []
        for token in postfix:
            if token.isdigit():
                stack.append(ExpressionTreeNode(value=token))
            elif token in OPERATORS_TOKENS:
                stack.append(
                    ExpressionTreeNode(value=token, left=stack.pop(), right=stack.pop())
                )
        return stack.pop()

    def _evaluate_expression_tree(self, node: ExpressionTreeNode) -> float:
        if node.left is None and node.right is None:
            return float(node.value)

        left_result: float = self._evaluate_expression_tree(node=node.left)
        right_result: float = self._evaluate_expression_tree(node=node.right)

        match node.value:
            case Token.multiply:
                return right_result * left_result
            case Token.divide:
                return right_result / left_result
            case Token.plus:
                return right_result + left_result
            case Token.minus:
                return right_result - left_result
