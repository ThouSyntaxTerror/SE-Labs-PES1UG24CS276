import re

COIN_RE = re.compile(r"[0-9]+", re.ASCII)
SLOT_RE = re.compile(r"([A-Za-z])([0-9]+)", re.ASCII)
PAYMENT_RE = re.compile(r"([0-9]+)/([0-9]+)", re.ASCII)


def _require_str(value, name):
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def parse_coins(coins_csv):
    """'5,10,25' -> [5, 10, 25]. Every coin must be a positive integer."""
    _require_str(coins_csv, "coins")
    coins = []
    for part in coins_csv.split(","):
        part = part.strip()
        if not COIN_RE.fullmatch(part) or int(part) == 0:
            raise ValueError(f"invalid coin value: {part!r}")
        coins.append(int(part))
    return coins


def slot_position(code):
    """'B7' -> (1, 6). Letter = row, number (1-based) = column."""
    _require_str(code, "slot code")
    match = SLOT_RE.fullmatch(code.strip())
    if not match or int(match.group(2)) == 0:
        raise ValueError(f"invalid slot code: {code!r}")
    return ord(match.group(1).upper()) - ord("A"), int(match.group(2)) - 1


def change_due(payment):
    """'200/150' -> '10 five-coins'. Payment must cover the price and the change must be a multiple of 5."""
    _require_str(payment, "payment")
    match = PAYMENT_RE.fullmatch(payment.strip())
    if not match:
        raise ValueError(f"expected 'paid/price', got {payment!r}")
    change = int(match.group(1)) - int(match.group(2))
    if change < 0:
        raise ValueError("payment is less than the price")
    if change % 5:
        raise ValueError("change cannot be paid out in five-coins")
    return str(change // 5) + " five-coins"


def _ask(label, prompt, func):
    print(f"\n==== Running {label} ====")
    try:
        print(func(input(prompt)))
    except ValueError as err:
        print("Invalid input:", err)


def main():
    _ask("parse_coins", "Enter coin values as CSV (e.g. 5,10,25): ", lambda s: f"Coins: {parse_coins(s)}")
    _ask("slot_position", "Enter a slot code (e.g. B7): ", lambda s: f"Row and Column: {slot_position(s)}")
    _ask("change_due", "Enter paid/price (e.g. 200/150): ", lambda s: f"Change Due: {change_due(s)}")


if __name__ == "__main__":
    main()
