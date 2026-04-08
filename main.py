import tempfile
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from decoder import decode_blackbox
from metrics import extract_metrics
from rules import analyze

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("frontend/index.html").read_text()


@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    if not file.filename.endswith((".bbl", ".bfl")):
        raise HTTPException(400, "Only .bbl or .bfl files are supported")

    with tempfile.NamedTemporaryFile(suffix=".bbl", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        df = decode_blackbox(tmp_path)
        metrics = extract_metrics(df)
        result = analyze(metrics)
        result["metrics"] = metrics
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
