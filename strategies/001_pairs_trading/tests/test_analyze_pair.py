import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import pandas as pd
import pytest
from analyze_pair import analyze


def test_identical_returns_have_correlation_one():
    idx = pd.date_range('2024-01-01', periods=5)
    prices = pd.DataFrame({'KO': [100, 102, 101, 105, 103],
                           'PEP': [200, 204, 202, 210, 206]}, index=idx)
    returns, indexed, corr = analyze(prices)
    assert corr == pytest.approx(1.0)
    assert len(returns) == 4
    assert indexed.iloc[0].tolist() == pytest.approx([100, 100])
