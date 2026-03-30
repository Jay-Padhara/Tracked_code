"""
Tests for data_fetcher module.
"""

import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# Assuming function name will be: fetch_so_data
from so_challenge import data_fetcher


@pytest.fixture
def sample_api_response():
    """Mock API JSON response."""
    return {
        "items": [
            {"creation_date": 1230768000},  # Jan 2009
            {"creation_date": 1233446400},  # Feb 2009
        ]
    }


def test_successful_data_fetch_returns_dataframe(tmp_path, sample_api_response):
    """Test that successful fetch returns correct DataFrame structure."""

    cache_file = tmp_path / "cache.csv"

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_api_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        assert isinstance(df, pd.DataFrame)
        assert "year_month" in df.columns
        assert "question_count" in df.columns


def test_cached_data_is_used(tmp_path):
    """Test that cached data is returned without making API call."""

    cache_file = tmp_path / "cache.csv"

    # Create fake cached data
    cached_df = pd.DataFrame({
        "year_month": ["2009-01", "2009-02"],
        "question_count": [10, 20],
    })
    cached_df.to_csv(cache_file, index=False)

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        # Ensure API was NOT called
        mock_get.assert_not_called()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2


def test_network_error_triggers_retry(tmp_path):
    """Test retry logic when network error occurs."""

    cache_file = tmp_path / "cache.csv"

    with patch("so_challenge.data_fetcher.requests.get") as mock_get:
        # First call fails, second succeeds
        mock_get.side_effect = [
            Exception("Network error"),
            MagicMock(status_code=200, json=lambda: {"items": []})
        ]

        df = data_fetcher.fetch_so_data(cache_path=cache_file)

        # Ensure retry happened (called more than once)
        assert mock_get.call_count >= 2

        assert isinstance(df, pd.DataFrame)