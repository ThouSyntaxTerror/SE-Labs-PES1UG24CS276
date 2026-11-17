from hypothesis import given, strategies as st
from vending_machine import parse_coins, slot_position, change_due


def run(call):
    """Return the result, or None if the function rejects the input with ValueError."""
    try:
        return call()
    except ValueError:
        return None


@given(st.text() | st.none())
def test_parse_coins_no_crash(s):
    run(lambda: parse_coins(s))


@given(st.text() | st.none())
def test_slot_position_no_crash(s):
    run(lambda: slot_position(s))


@given(st.text() | st.none())
def test_change_due_no_crash(s):
    run(lambda: change_due(s))


@given(st.lists(st.integers(min_value=1, max_value=10**6), min_size=1))
def test_parse_coins_roundtrip(coins):
    assert parse_coins(",".join(map(str, coins))) == coins


@given(st.sampled_from("abcXYZ"), st.integers(min_value=1, max_value=999))
def test_slot_position_valid(letter, number):
    row, col = slot_position(f"{letter}{number}")
    assert row >= 0 and col == number - 1


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=0, max_value=10**6))
def test_change_due_never_loses_money(price, extra):
    paid = price + extra
    result = run(lambda: change_due(f"{paid}/{price}"))
    if extra % 5 == 0:
        assert result == f"{extra // 5} five-coins"
    else:
        assert result is None  # cannot be paid out in five-coins: must be rejected
