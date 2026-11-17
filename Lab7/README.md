# Lab 7 - Fuzz Testing (vending_machine.py)

Hypothesis fuzz testing of `parse_coins`, `slot_position` and `change_due` (assigned repo `SETAPESU26/L6_L7_30_vending_machine`).

| Run | Result |
|-----|--------|
| Original script | 4 of 6 tests fail (crashes on `None`, bad text; silent loss of change) |
| Fixed script | 6 of 6 pass |

- `vending_machine.py` - hardened script
- `test_vending_machine.py` - Hypothesis tests
- `Lab7_Fuzz_Testing_Report.pdf` - report with the output of each handout step
- `screenshots/`, `evidence/`, `legacy/vending_machine_before.py` - original script and raw outputs

Run: `pip install hypothesis pytest && python -m pytest test_vending_machine.py`
