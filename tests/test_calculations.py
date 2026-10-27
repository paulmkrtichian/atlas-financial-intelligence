import pytest

from finance.calculations import (
    revenue_growth,
    operating_margin,
    current_ratio,
    net_profit_margin,
    return_on_assets,
    return_on_equity,
    free_cash_flow
)


def test_revenue_growth():
    assert revenue_growth(1200, 1000) == pytest.approx(20.0)


def test_operating_margin():
    assert operating_margin(250, 1000) == pytest.approx(25.0)


def test_current_ratio():
    assert current_ratio(500, 250) == pytest.approx(2.0)


def test_zero_revenue():
    with pytest.raises(ValueError):
        operating_margin(100, 0)


def test_zero_liabilities():
    with pytest.raises(ValueError):
        current_ratio(500, 0)

def test_net_profit_margin():
    result = net_profit_margin(150, 1000)
    assert result == pytest.approx(15)


def test_return_on_assets():
    result = return_on_assets(100, 900, 1100)
    assert result == pytest.approx(10)


def test_return_on_equity():
    result = return_on_equity(100, 400, 600)
    assert result == pytest.approx(20)


def test_free_cash_flow():
    result = free_cash_flow(120, 35)
    assert result == pytest.approx(85)


def test_zero_average_assets():
    with pytest.raises(ValueError):
        return_on_assets(100, 0, 0)


def test_zero_average_equity():
    with pytest.raises(ValueError):
        return_on_equity(100, 0, 0)


def test_negative_capital_expenditures():
    with pytest.raises(ValueError):
        free_cash_flow(120, -35)