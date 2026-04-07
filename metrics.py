import pandas as pd
import numpy as np
from scipy.fft import rfft, rfftfreq


def extract_metrics(df: pd.DataFrame) -> dict:
    time_us = df["time (us)"].values
    dt = np.diff(time_us).mean() / 1e6
    sample_rate = 1.0 / dt

    def rms(col):
        return float(np.sqrt(np.mean(df[col].values ** 2))) if col in df else 0.0

    def noise_rms(col):
        if col not in df:
            return 0.0
        sig = df[col].values
        n = len(sig)
        freqs = rfftfreq(n, d=dt)
        fft_mag = np.abs(rfft(sig))
        hf_mask = freqs > 100
        return float(np.sqrt(np.mean(fft_mag[hf_mask] ** 2)))

    return {
        "sample_rate": float(sample_rate),
        "p_error_rms": {
            "roll": rms("axisP[0]"),
            "pitch": rms("axisP[1]"),
            "yaw": rms("axisP[2]") if "axisP[2]" in df else 0.0,
        },
        "i_error_rms": {
            "roll": rms("axisI[0]"),
            "pitch": rms("axisI[1]"),
            "yaw": rms("axisI[2]") if "axisI[2]" in df else 0.0,
        },
        "d_noise_rms": {
            "roll": noise_rms("axisD[0]"),
            "pitch": noise_rms("axisD[1]"),
        },
        "gyro_noise_rms": {
            "roll": noise_rms("gyroADC[0]"),
            "pitch": noise_rms("gyroADC[1]"),
            "yaw": noise_rms("gyroADC[2]"),
        },
    }
