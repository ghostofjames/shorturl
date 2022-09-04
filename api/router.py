from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import RedirectResponse
from hashids import Hashids
from pydantic import HttpUrl
from sqlmodel import Session


from api import models
from api.database import get_session
from api.config import get_settings

hashids = Hashids(salt=get_settings().SALT, min_length=get_settings().MIN_LENGTH)

router = APIRouter()


@router.post(
    "/shorten/",
    response_model=models.ShortUrlLink,
    summary="Shorten a new URL",
    response_description="A short url which will redirect to the target URL",
)
# def shorten_url(
#     target_url: HttpUrl = Body(..., embed=True), db: Session = Depends(get_session)
# ):
def shorten_url(target_url: models.ShortUrlCreate, db: Session = Depends(get_session)):
    """
    Shorten a URL

    - **target_url**: a valid HttpUrl
    """
    db_shorturl = models.ShortUrl(target_url=target_url.target_url)

    db.add(db_shorturl)
    db.commit()

    shorturl = hashids.encode(db_shorturl.id)
    db_shorturl.short = shorturl
    db.commit()

    return models.ShortUrlLink(link=f"{get_settings().BASE_URL}/{db_shorturl.short}")


@router.get("/info", response_model=list[models.ShortUrl], tags=["info"])
def read_shorturls(db: Session = Depends(get_session)):
    shorturls = db.query(models.ShortUrl).all()
    return shorturls


@router.get("/info/{shorturl}", response_model=models.ShortUrlRead, tags=["info"])
def shorturl_info(shorturl: str, db: Session = Depends(get_session)):
    decoded = hashids.decode(shorturl)
    if not decoded:
        raise HTTPException(status_code=404)
    id = decoded[0]

    db_shorturl = db.get(models.ShortUrl, id)
    if not db_shorturl:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return models.ShortUrlRead(
        **db_shorturl.dict(), link=f"{get_settings().BASE_URL}/{db_shorturl.short}"
    )


@router.get(
    "/{shorturl}",
    summary="",
    response_description="Redirect to the target url",
    response_class=RedirectResponse,
)
def redirect(shorturl: str, db: Session = Depends(get_session)):
    """
    Redirect to a target url based on the given short url

    -**shorturl**:
    """
    if shorturl == "favicon.ico":
        raise HTTPException(status_code=404)
    decoded = hashids.decode(shorturl)
    if not decoded:
        raise HTTPException(status_code=404)

    id = decoded[0]

    db_shorturl = db.get(models.ShortUrl, id)
    if not db_shorturl:
        raise HTTPException(status_code=404, detail="Short URL not found")

    url = db_shorturl.target_url
    db_shorturl.visits += 1  # type: ignore

    db.add(db_shorturl)
    db.commit()

    return url
