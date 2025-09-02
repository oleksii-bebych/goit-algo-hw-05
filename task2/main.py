import re
from decimal import Decimal, InvalidOperation
from typing import Callable, Iterator

def generator_numbers(text: str) -> Iterator[Decimal]:
    # Regex: optional sign, digits, optional decimal part
    for match in re.findall(r"[+-]?\d+(?:[.,]\d+)?", text):
        try:
            # normalize commas to dots (1,23 → 1.23)
            yield Decimal(match.replace(",", "."))
        except InvalidOperation:
            continue

def sum_profit(text: str, func: Callable[[str], Iterator[Decimal]]) -> Decimal:
    return sum(func(text), start=Decimal("0"))

if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
