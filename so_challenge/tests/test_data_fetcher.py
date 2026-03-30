"""
Tests for data_fetcher module.
"""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# ✅ FIXED IMPORT
import data_fetcher

@pytest.fixture
def sample_api_response_large():
    """Mock API response with ~50 entries across multiple months."""
    items = []

    # Generate 50 timestamps across Jan–Mar 2009
    base_timestamp = 1230768000  # Jan 1, 2009

    for i in range(50):
        items.append({
            "creation_date": base_timestamp + (i * 86400)  # +1 day
        })

    return {"items": items}


def test_successful_data_fetch_returns_dataframe(tmp_path, sample_api_response_large):
    """Test successful fetch returns correct DataFrame with aggregated data."""

    cache_file = tmp_path / "cache.csv"

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_response_large
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        # ✅ Basic checks
        assert isinstance(df, pd.DataFrame)
        assert "year_month" in df.columns
        assert "question_count" in df.columns

        # ✅ Should not be empty
        assert len(df) > 0

        # ✅ Total count should match input size
        assert df["question_count"].sum() == 50


def test_cached_data_is_used(tmp_path):
    """Test that cached data is returned without making API call."""

    cache_file = tmp_path / "cache.csv"

    cached_df = pd.DataFrame({
        "year_month": ["2009-01", "2009-02"],
        "question_count": [10, 20],
    })
    cached_df.to_csv(cache_file, index=False)

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        # ✅ API should not be called
        mock_get.assert_not_called()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df["question_count"].sum() == 30


def test_network_error_triggers_retry(tmp_path):
    """Test retry logic when network error occurs."""

    cache_file = tmp_path / "cache.csv"

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        mock_get.side_effect = [
            Exception("Network error"),
            MagicMock(status_code=200, json=lambda: {"items": []})
        ]

        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        # ✅ Ensure retry happened
        assert mock_get.call_count >= 2

        assert isinstance(df, pd.DataFrame)


def test_empty_api_response_returns_empty_dataframe(tmp_path):
    """Test behavior when API returns no data."""

    cache_file = tmp_path / "cache.csv"

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["year_month", "question_count"]
        assert df.empty