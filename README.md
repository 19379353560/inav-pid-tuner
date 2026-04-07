# INAV PID Tuner

Upload a Blackbox log (.bbl) and get PID/filter tuning recommendations.

## Requirements
- Python 3.10+
- `blackbox_decode` installed and in PATH
  - Download: https://github.com/iNavFlight/blackbox-tools/releases

## Run
```bash
pip install -r requirements.txt
python main.py
```
Open http://localhost:8000

## Usage
1. Fly your quad and save the Blackbox log
2. Upload the .bbl file
3. Review recommendations
4. Copy CLI commands and paste into INAV Configurator CLI
