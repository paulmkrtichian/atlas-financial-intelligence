def revenue_growth(current_revenue, previous_revenue):
    """Calculate revenue growth as a percentage."""

    if previous_revenue <= 0:
        raise ValueError("Previous revenue must be positive.")

    growth = (
        (current_revenue - previous_revenue)
        / previous_revenue
    ) * 100

    return growth


def operating_margin(operating_income, revenue):
    """Calculate operating margin as a percentage."""

    if revenue <= 0:
        raise ValueError("Revenue must be positive.")

    margin = (operating_income / revenue) * 100

    return margin


def current_ratio(current_assets, current_liabilities):
    """Calculate a company's current ratio."""

    if current_liabilities <= 0:
        raise ValueError("Current liabilities must be positive.")

    ratio = current_assets / current_liabilities

    return ratio

def net_profit_margin(net_income, revenue):
    """
    Calculate net profit margin as a percentage.
    """
    if revenue <= 0:
        raise ValueError("Revenue must be positive.")

    return (net_income / revenue) * 100


def return_on_assets(net_income, beginning_assets, ending_assets):
    """
    Calculate ROA using average total assets.
    """
    average_assets = (beginning_assets + ending_assets) / 2

    if average_assets <= 0:
        raise ValueError("Average assets must be positive.")

    return (net_income / average_assets) * 100


def return_on_equity(net_income, beginning_equity, ending_equity):
    """
    Calculate ROE using average shareholders' equity.
    """
    average_equity = (beginning_equity + ending_equity) / 2

    if average_equity <= 0:
        raise ValueError("Average equity must be positive.")

    return (net_income / average_equity) * 100


def free_cash_flow(operating_cash_flow, capital_expenditures):
    """
    Calculate free cash flow.

    Capital expenditures must be entered as a
    nonnegative amount representing cash spent.
    """
    if capital_expenditures < 0:
        raise ValueError(
            "Capital expenditures must be nonnegative."
        )

    return operating_cash_flow - capital_expenditures