# tests/test_rules.py
from rules import analyze

def test_high_p_error_suggests_raise_p():
    metrics = {
        "p_error_rms": {"roll": 50.0, "pitch": 50.0, "yaw": 50.0},
        "i_error_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "d_noise_rms": {"roll": 1.0, "pitch": 1.0},
        "gyro_noise_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "sample_rate": 1000.0,
    }
    result = analyze(metrics)
    assert any("p_roll" in r["param"] for r in result["recommendations"])

def test_high_d_noise_suggests_lower_lpf():
    metrics = {
        "p_error_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "i_error_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "d_noise_rms": {"roll": 500.0, "pitch": 500.0},
        "gyro_noise_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "sample_rate": 1000.0,
    }
    result = analyze(metrics)
    assert any("dterm_lpf" in r["param"] for r in result["recommendations"])

def test_cli_commands_not_empty_when_recommendations_exist():
    metrics = {
        "p_error_rms": {"roll": 50.0, "pitch": 50.0, "yaw": 50.0},
        "i_error_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "d_noise_rms": {"roll": 1.0, "pitch": 1.0},
        "gyro_noise_rms": {"roll": 1.0, "pitch": 1.0, "yaw": 1.0},
        "sample_rate": 1000.0,
    }
    result = analyze(metrics)
    assert len(result["cli_commands"]) > 0
    assert "save" in result["cli_commands"]
