"""Lab 6 - code (line) coverage tests for vending_machine.py.

Run:
    coverage run -m pytest CodeCoverageTest_vending_machine.py
    coverage report -m
"""
import pytest
from vending_machine import select_item, make_change, purchase


# ---- select_item: one test per return statement ----
def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"


def test_sold_out_item():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"


def test_insufficient_credit():
    assert select_item("cola", {"cola": 3}, 100) == "insufficient"


def test_item_ok():
    assert select_item("chips", {"chips": 2}, 100) == "ok"


# ---- make_change ----
def test_no_change_needed():
    assert make_change(0) == []


def test_negative_amount_raises():
    with pytest.raises(ValueError):
        make_change(-5)


def test_change_with_several_coins():
    assert make_change(185) == [100, 50, 25, 10]


def test_change_not_possible():
    # 3 cents cannot be made from coins of 5 or more
    assert make_change(3) is None


# ---- purchase ----
def test_purchase_dispensed_with_change():
    stock = {"cola": 2}
    assert purchase("cola", stock, 200) == ("dispensed", [50])
    assert stock["cola"] == 1


def test_purchase_rejected_when_not_ok():
    assert purchase("water", {}, 100) == ("invalid", [])


def test_purchase_no_exact_change():
    stock = {"cola": 2}
    assert purchase("cola", stock, 153) == ("no_exact_change", [])
    assert stock["cola"] == 2  # stock untouched
