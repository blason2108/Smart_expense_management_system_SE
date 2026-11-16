from decimal import Decimal

import pytest

from reports.views import expense_scale, safe_cell


@pytest.mark.parametrize(
    "amount,scale",
    [("0.01", "0.01"), ("0.03", "0.05"), ("850", "1000"), ("1000", "1000"), ("1000.01", "2000")],
)
def test_expense_scale_covers_the_peak(amount, scale):
    assert expense_scale(Decimal(amount)) == Decimal(scale)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Lunch", "Lunch"),
        (Decimal("12.50"), "12.50"),
        ("  +2", "'  +2"),
        ("\tFood", "'\tFood"),
    ],
)
def test_csv_cell_keeps_text_literal(value, expected):
    assert safe_cell(value) == expected
