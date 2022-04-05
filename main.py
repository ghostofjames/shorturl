import pprint
from wsgiref.util import request_uri
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from hashids import Hashids
from sqladmin import Admin, ModelAdmin
from sqlalchemy.orm import Session
from fastapi_security import FastAPISecurity, User

import models
import schemas
from database import engine, get_db

SALT = "test"
MIN_LENGTH = 6
ROOT = "http://127.0.0.1:8000/short/"
ADMIN = [{"username": "ADMIN", "password": "ADMIN"}]

hashids = Hashids(salt=SALT, min_length=MIN_LENGTH)

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
admin = Admin(app, engine)

security = FastAPISecurity()
security.init_basic_auth(ADMIN)


class ShortUrlAdmin(ModelAdmin, model=models.ShortUrl):
    def is_accessible(self, request) -> bool:
        if request.user:
            return True
        else:
            return False

    name = "Short URL"
    name_plural = "Short URLs"
    icon = "fa-solid fa-link"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [models.ShortUrl.id, models.ShortUrl.url, models.ShortUrl.visits]  # type: ignore


admin.register_model(ShortUrlAdmin)


@app.get("/adminpage/")
def admin_page(user: User = Depends(security.authenticated_user_or_401)):
    return user


@app.get("/")
def home():
    return {"hello": "world"}


@app.get("/shorturls/", response_model=list[schemas.ShortUrl])
def read_shorturls(db: Session = Depends(get_db)):
    shorturls = db.query(models.ShortUrl).all()
    return shorturls


@app.post("/shorten/")
def shorten_url(url: schemas.ShortUrlCreate, db: Session = Depends(get_db)):
    db_shorturl = models.ShortUrl(url=url.url, visits=0)
    db.add(db_shorturl)
    db.commit()
    db.refresh(db_shorturl)

    shorturl = hashids.encode(db_shorturl.id)

    return f"{ROOT}{shorturl}"


@app.get("/go/{shorturl}/", response_class=RedirectResponse)
def redirect(shorturl: str, db: Session = Depends(get_db)):
    id = hashids.decode(shorturl)[0]  # type: ignore
    db_shorturl = db.query(models.ShortUrl).filter(models.ShortUrl.id == id).first()
    if db_shorturl is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    db_shorturl.visits += 1
    db.commit()
    db.refresh(db_shorturl)
    return db_shorturl.url