"""Lab 6 - branch coverage tests for vending_machine.py.

Every decision is exercised both ways (True and False).

Run:
    coverage run --branch -m pytest BranchCoverageTest_vending_machine.py
    coverage report -m
"""
import pytest
from vending_machine import select_item, make_change, purchase


# ---- select_item: each `if` taken and not taken ----
def test_item_not_in_prices():
    assert select_item("water", {}, 100) == "invalid"


def test_item_in_prices_but_missing_from_stock():
    # stock.get(item, 0) falls back to 0 -> sold_out
    assert select_item("chips", {}, 500) == "sold_out"


def test_item_stock_zero():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_credit_below_price():
    assert select_item("cola", {"cola": 3}, 149) == "insufficient"


def test_credit_exactly_price_is_ok():
    # boundary: credit == price is NOT insufficient
    assert select_item("candy", {"candy": 1}, 75) == "ok"


def test_credit_above_price_is_ok():
    assert select_item("chips", {"chips": 2}, 300) == "ok"


# ---- make_change: negative / zero / loop / remainder branches ----
def test_negative_amount_raises():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)


def test_zero_amount_gives_empty_list():
    # for-loop runs, while never enters, amount > 0 False
    assert make_change(0) == []


def test_single_coin():
    assert make_change(25) == [25]


def test_repeated_coin_while_loop_iterates():
    assert make_change(200) == [100, 100]


def test_all_denominations_used():
    assert make_change(190) == [100, 50, 25, 10, 5]


def test_leftover_returns_none():
    assert make_change(3) is None


def test_leftover_after_some_coins_returns_none():
    # 100 + 50 consumed, 2 cents left over
    assert make_change(152) is None


# ---- purchase: status != ok / change None / dispensed ----
@pytest.mark.parametrize(
    "item, stock, credit, status",
    [
        ("water", {}, 500, "invalid"),
        ("cola", {"cola": 0}, 500, "sold_out"),
        ("cola", {"cola": 1}, 10, "insufficient"),
    ],
)
def test_purchase_rejected_by_select_item(item, stock, credit, status):
    before = dict(stock)
    assert purchase(item, stock, credit) == (status, [])
    assert stock == before


def test_purchase_no_exact_change_keeps_stock():
    stock = {"cola": 2}
    assert purchase("cola", stock, 153) == ("no_exact_change", [])
    assert stock["cola"] == 2


def test_purchase_exact_payment_no_change():
    stock = {"candy": 1}
    assert purchase("candy", stock, 75) == ("dispensed", [])
    assert stock["candy"] == 0


def test_purchase_dispensed_with_change_decrements_stock():
    stock = {"cola": 2}
    assert purchase("cola", stock, 200) == ("dispensed", [50])
    assert stock["cola"] == 1
