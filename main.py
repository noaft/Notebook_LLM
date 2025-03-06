from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).resolve().parent
static_dir = Path(BASE_DIR, "static")
templates_dir = Path(BASE_DIR, "templates")

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_dir)

# Serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# cros allow in web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # admit for all soruce and port,
    allow_credentials=True,
    allow_methods=["*"], # admit for all method
    allow_headers=["*"], # all method
)

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})