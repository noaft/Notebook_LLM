from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.upload import router as upload
from data.data import init
from api.user import router as user
from api.delete import router as delete
from api.mic import router as mic
init() # init database

BASE_DIR = Path(__file__).resolve().parent
static_dir = Path(BASE_DIR, "static")
templates_dir = Path(BASE_DIR, "templates")

app = FastAPI()
# cros allow in web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # admit for all soruce and port,
    allow_credentials=True,
    allow_methods=["*"], # admit for all method
    allow_headers=["*"], # all method
)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_dir)

# Serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(router=upload)
app.include_router(router=user)
app.include_router(router=delete)
app.include_router(router=mic)

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})