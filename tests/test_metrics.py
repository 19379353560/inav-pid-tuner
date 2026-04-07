# tests/test_metrics.py
import pandas as pd
import numpy as np
from metrics import extract_metrics

def make_df(n=1000, sample_rate=1000):
    t = np.arange(n) / sample_rate
    df = pd.DataFrame({
        "time (us)": (t * 1e6).astype(int),
        "axisP[0]": np.random.normal(0, 5, n),
        "axisP[1]": np.random.normal(0, 5, n),
        "axisI[0]": np.random.normal(0, 2, n),
        "axisI[1]": np.random.normal(0, 2, n),
        "axisD[0]": np.random.normal(0, 3, n),
        "axisD[1]": np.random.normal(0, 3, n),
        "gyroADC[0]": np.random.normal(0, 10, n),
        "gyroADC[1]": np.random.normal(0, 10, n),
        "gyroADC[2]": np.random.normal(0, 10, n),
    })
    return df

def test_extract_metrics_returns_expected_keys():
    df = make_df()
    m = extract_metrics(df)
    for key in ["p_error_rms", "i_error_rms", "d_noise_rms", "gyro_noise_rms", "sample_rate"]:
        assert key in m, f"missing key: {key}"

def test_p_error_rms_positive():
    df = make_df()
    m = extract_metrics(df)
    assert m["p_error_rms"]["roll"] > 0
    assert m["p_error_rms"]["pitch"] > 0

def test_sample_rate_detected():
    df = make_df(n=1000, sample_rate=1000)
    m = extract_metrics(df)
    assert 900 < m["sample_rate"] < 1100
