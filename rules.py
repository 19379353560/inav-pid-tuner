P_ERROR_HIGH = 20.0
P_ERROR_LOW = 2.0
I_ERROR_HIGH = 15.0
D_NOISE_HIGH = 100.0
GYRO_NOISE_HIGH = 80.0


def analyze(metrics: dict) -> dict:
    recommendations = []

    axes = ["roll", "pitch", "yaw"]
    p_params = {"roll": "p_roll", "pitch": "p_pitch", "yaw": "p_yaw"}
    i_params = {"roll": "i_roll", "pitch": "i_pitch", "yaw": "i_yaw"}

    for axis in axes:
        p_err = metrics["p_error_rms"][axis]
        i_err = metrics["i_error_rms"][axis]

        if p_err > P_ERROR_HIGH:
            recommendations.append({
                "axis": axis, "param": p_params[axis],
                "action": "increase", "pct": 10,
                "reason": f"High P error RMS ({p_err:.1f}) — response is sluggish"
            })
        elif p_err < P_ERROR_LOW:
            recommendations.append({
                "axis": axis, "param": p_params[axis],
                "action": "decrease", "pct": 10,
                "reason": f"Very low P error RMS ({p_err:.1f}) — possible oscillation"
            })

        if i_err > I_ERROR_HIGH:
            recommendations.append({
                "axis": axis, "param": i_params[axis],
                "action": "increase", "pct": 10,
                "reason": f"High I error RMS ({i_err:.1f}) — I term too low"
            })

        if axis in metrics["d_noise_rms"]:
            d_noise = metrics["d_noise_rms"][axis]
            if d_noise > D_NOISE_HIGH:
                recommendations.append({
                    "axis": axis, "param": "dterm_lpf_hz",
                    "action": "decrease", "pct": 15,
                    "reason": f"High D noise ({d_noise:.1f}) — lower dterm LPF cutoff"
                })

        gyro_noise = metrics["gyro_noise_rms"][axis]
        if gyro_noise > GYRO_NOISE_HIGH:
            recommendations.append({
                "axis": axis, "param": "gyro_lpf_hz",
                "action": "decrease", "pct": 10,
                "reason": f"High gyro noise ({gyro_noise:.1f}) — lower gyro LPF cutoff"
            })

    cli_lines = []
    for r in recommendations:
        direction = "+" if r["action"] == "increase" else "-"
        cli_lines.append(f"# {r['reason']}")
        cli_lines.append(f"# set {r['param']} = <current_value> {direction}{r['pct']}%")
        cli_lines.append(f"set {r['param']} = <adjust_manually>")

    if cli_lines:
        cli_lines.append("save")

    return {
        "recommendations": recommendations,
        "cli_commands": "\n".join(cli_lines),
    }
