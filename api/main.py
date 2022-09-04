from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.database import create_db_and_tables
from api.router import router

app = FastAPI(
    title="ShortURL",
    description="A simple URL shortener",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

app.include_router(router)


@app.on_event("startup")
def on_starup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("frontpage.html", {"request": request})
