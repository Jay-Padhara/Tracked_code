import pandas as pd
import requests
import time
from pathlib import Path


def fetch_so_data(cache_path: Path) -> pd.DataFrame:
    """
    Fetch Stack Overflow question data aggregated by year-month.
    Uses cache if available, otherwise fetches from API with retry logic.
    """
    if cache_path.exists():
        return pd.read_csv(cache_path)

    # API endpoint for Stack Overflow questions (example URL, mocked in tests)
    url = "https://api.stackexchange.com/2.3/questions?site=stackoverflow&fromdate=1230768000&todate=1233446400&order=desc&sort=creation&filter=default"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])

            if not items:
                # Return empty DataFrame with expected columns
                return pd.DataFrame(columns=["year_month", "question_count"])

            # Process data
            df = pd.DataFrame(items)
            df['creation_date'] = pd.to_datetime(df['creation_date'], unit='s')
            df['year_month'] = df['creation_date'].dt.to_period('M').astype(str)
            df_agg = df.groupby('year_month').size().reset_index(name='question_count')

            # Save to cache
            df_agg.to_csv(cache_path, index=False)
            return df_agg

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                raise e