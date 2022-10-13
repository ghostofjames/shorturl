from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
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


app.include_router(router)


@app.on_event("startup")
def on_starup():
    create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("api/templates/frontpage.html")
