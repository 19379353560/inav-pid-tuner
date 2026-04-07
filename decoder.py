import subprocess
import tempfile
import os
import pandas as pd


def decode_blackbox(bbl_path: str) -> pd.DataFrame:
    """Run blackbox_decode on bbl_path, return DataFrame of first log."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["blackbox_decode", "--stdout", bbl_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"blackbox_decode failed: {result.stderr}")

        lines = result.stdout.splitlines()
        if not lines:
            raise ValueError("blackbox_decode produced no output")

        csv_path = os.path.join(tmpdir, "log.csv")
        with open(csv_path, "w") as f:
            f.write(result.stdout)

        df = pd.read_csv(csv_path, skipinitialspace=True)
        df.columns = df.columns.str.strip()
        return df
