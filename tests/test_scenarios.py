
import pandas as pd
import pytest

from finance.scenarios import project_scenario


SAMPLE_DATA = pd.DataFrame({
    "fiscal_year": [2024, 2025],
    "revenue": [115_000_000, 135_000_000]
})


def test_first_year_revenue():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[0]["revenue"] == pytest.approx(
        145_800_000
    )


def test_compounded_revenue():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[-1]["revenue"] == pytest.approx(
        170_061_120
    )


def test_operating_income():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[0]["operating_income"] == pytest.approx(
        145_800_000 * 0.23
    )


def test_missing_base_year():

    with pytest.raises(ValueError):
        project_scenario(
            SAMPLE_DATA, 2030, 8, 23
        )


def test_invalid_growth():

    with pytest.raises(ValueError):
        project_scenario(
            SAMPLE_DATA, 2025, -110, 23
        )


def test_duplicate_base_year():

    duplicated = pd.concat(
        [SAMPLE_DATA, SAMPLE_DATA.iloc[[1]]],
        ignore_index=True
    )

    with pytest.raises(ValueError):
        project_scenario(
            duplicated, 2025, 8, 23
        )

import pandas as pd
import pytest

from finance.scenarios import project_scenario


SAMPLE_DATA = pd.DataFrame({
    "fiscal_year": [2024, 2025],
    "revenue": [115_000_000, 135_000_000]
})


def test_first_year_revenue():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[0]["revenue"] == pytest.approx(
        145_800_000
    )


def test_compounded_revenue():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[-1]["revenue"] == pytest.approx(
        170_061_120
    )


def test_operating_income():

    result = project_scenario(
        SAMPLE_DATA, 2025, 8, 23
    )

    assert result.iloc[0]["operating_income"] == pytest.approx(
        145_800_000 * 0.23
    )


def test_missing_base_year():

    with pytest.raises(ValueError):
        project_scenario(
            SAMPLE_DATA, 2030, 8, 23
        )


def test_invalid_growth():

    with pytest.raises(ValueError):
        project_scenario(
            SAMPLE_DATA, 2025, -110, 23
        )


def test_duplicate_base_year():

    duplicated = pd.concat(
        [SAMPLE_DATA, SAMPLE_DATA.iloc[[1]]],
        ignore_index=True
    )

    with pytest.raises(ValueError):
        project_scenario(
            duplicated, 2025, 8, 23
        )
