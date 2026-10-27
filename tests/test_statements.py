from finance.statements import get_annual_fact


def test_correct_fiscal_year():

    sample_data = {
        "facts": {
            "us-gaap": {
                "Assets": {
                    "units": {
                        "USD": [
                            {
                                "val": 1000,
                                "form": "10-K",
                                "fy": 2024,
                                "fp": "FY",
                                "end": "2023-09-30",
                                "filed": "2024-11-01"
                            },
                            {
                                "val": 1200,
                                "form": "10-K",
                                "fy": 2024,
                                "fp": "FY",
                                "end": "2024-09-28",
                                "filed": "2024-11-01"
                            }
                        ]
                    }
                }
            }
        }
    }

    result = get_annual_fact(
        sample_data,
        ["Assets"],
        2024
    )

    assert result["value"] == 1200
    assert result["end"] == "2024-09-28"


def test_missing_metric():

    sample_data = {
        "facts": {
            "us-gaap": {}
        }
    }

    result = get_annual_fact(
        sample_data,
        ["OperatingIncomeLoss"],
        2024
    )

    assert result is None