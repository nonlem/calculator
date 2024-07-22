from typing import Optional, TypeVar, Generic

T = TypeVar("T")


def main():
    expression_parser = ExpressionParser()
    user_input = UserInput()
    try:
        expression = user_input.get_input()
        result = expression_parser.process(expression)
        print(f"The result of the expression is: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")


class Node(Generic[T]):
    def __init__(self, data: T) -> None:
        self.data = data
        # 次のノードへのポインタ（初期値は None）
        self.next: Optional["Node[T]"] = None


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None

    # データをスタックにプッシュするメソッド
    def push(self, data: T) -> None:
        new_head = Node[T](data)
        new_head.next = self.head
        self.head = new_head

    # スタックの先頭データを参照するメソッド
    def peek(self) -> Optional[T]:
        if self.head is not None:
            return self.head.data
        return None

    # スタックからデータをポップするメソッド
    def pop(self) -> Optional[T]:
        if self.head is not None:
            temp = self.head
            self.head = self.head.next
            return temp.data
        return None


class ExpressionParser:
    _PLUS_SYMBOL = "+"
    _MINUS_SYMBOL = "-"
    _MULTIPLE_SYMBOL = "*"
    _DIVIDE_SYMBOL = "/"
    _LEFT_BRACKET = "("
    _RIGHT_BRACKET = ")"
    _SYMBOLS = set(
        [
            _PLUS_SYMBOL,
            _MINUS_SYMBOL,
            _MULTIPLE_SYMBOL,
            _DIVIDE_SYMBOL,
            _LEFT_BRACKET,
            _RIGHT_BRACKET,
        ]
    )
    _OPERATORS = set([_PLUS_SYMBOL, _MINUS_SYMBOL, _MULTIPLE_SYMBOL, _DIVIDE_SYMBOL])
    _OPERATOR_PRIORITIES = {
        _PLUS_SYMBOL: 1,
        _MINUS_SYMBOL: 1,
        _MULTIPLE_SYMBOL: 10,
        _DIVIDE_SYMBOL: 10,
    }

    def __init__(self) -> None:
        self._operand_stack = Stack[int]()
        self._operator_stack = Stack[str]()

    def process(self, expression: str) -> int:
        ref = len(expression)

        for index in reversed(range(len(expression))):
            if self._is_operator(expression, index):
                operator = expression[index]
                while (
                    (peeked_operator := self._operator_stack.peek()) is not None
                    and peeked_operator != self._RIGHT_BRACKET
                    and self._OPERATOR_PRIORITIES[peeked_operator]
                    > self._OPERATOR_PRIORITIES[operator]
                ):
                    self._operate()
                self._operator_stack.push(expression[index])

            elif self._is_sign(expression, index):
                sign = expression[index]
                if sign == self._MINUS_SYMBOL:
                    self._operand_stack.push(-1)
                    self._operator_stack.push(self._MULTIPLE_SYMBOL)

            elif self._is_left_bracket(expression, index):
                while self._operator_stack.peek() != self._RIGHT_BRACKET:
                    self._operate()
                self._operator_stack.pop()

            elif self._is_right_bracket(expression, index):
                right_bracket = expression[index]
                self._operator_stack.push(right_bracket)

            elif self._can_trim_num(expression, index):
                num = int(expression[index:ref])
                self._operand_stack.push(num)

            if self._is_symbol(expression, index):
                ref = index

        while self._operator_stack.peek() is not None:
            self._operate()

        result = self._operand_stack.pop()
        if result is None:
            raise ValueError("result is None.")
        return result

    def _operate(self) -> None:
        left_operand = self._operand_stack.pop()
        right_operand = self._operand_stack.pop()
        operator = self._operator_stack.pop()
        if left_operand is None:
            raise ValueError("left_operand: None")
        if right_operand is None:
            raise ValueError("right_operand: None")
        if operator is None:
            raise ValueError("operator: None")

        self._operand_stack.push(self._calculate(left_operand, right_operand, operator))

    def _calculate(self, left_operand: int, right_operand: int, operator: str) -> int:
        if operator == self._PLUS_SYMBOL:
            return left_operand + right_operand
        elif operator == self._MINUS_SYMBOL:
            return left_operand - right_operand
        elif operator == self._MULTIPLE_SYMBOL:
            return left_operand * right_operand
        if right_operand == 0:
            raise ValueError("right must not be zero")
        return int(left_operand / right_operand)

    def _is_operator(self, expression: str, index: int) -> bool:
        return (
            0 < index < len(expression) - 1
            and expression[index] in self._OPERATORS
            and expression[index - 1] not in self._OPERATORS
            and expression[index - 1] != self._LEFT_BRACKET
        )

    def _is_sign(self, expression: str, index: int) -> bool:
        return (
            index < len(expression) - 1
            and expression[index + 1].isdecimal()
            and (
                expression[index] == self._PLUS_SYMBOL
                or expression[index] == self._MINUS_SYMBOL
            )
            and (
                index == 0
                or expression[index - 1] in self._OPERATORS
                or expression[index - 1] == self._LEFT_BRACKET
            )
        )

    def _is_left_bracket(self, expression: str, index: int) -> bool:
        return expression[index] == self._LEFT_BRACKET

    def _is_right_bracket(self, expression: str, index: int) -> bool:
        return expression[index] == self._RIGHT_BRACKET

    def _can_trim_num(self, expression: str, index: int) -> bool:
        return expression[index].isdecimal() and (
            index == 0 or not expression[index - 1].isdecimal()
        )

    def _is_symbol(self, expression: str, index: int) -> bool:
        return expression[index] in self._SYMBOLS


class UserInput:
    def __init__(self) -> None:
        self.input_data = []

    def get_input(self) -> str:
        while True:
            user_input = input(
                "Enter a character (enter '=' to calculate, 'C' to clear): "
            )
            if user_input == "=":
                break
            elif user_input.upper() == "C":
                self.all_clear()
                continue
            self.input_data.append(user_input)
            self.display_current_input()
        return "".join(self.input_data)

    def display_current_input(self) -> None:
        print(f"Current input: {''.join(self.input_data)}")

    def all_clear(self) -> None:
        self.input_data = []
        print("All input cleared.")


if __name__ == "__main__":
    main()
