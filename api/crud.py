from hashids import Hashids
from sqlmodel import Session
from fastapi import Depends

from api.models import ShortUrl, ShortUrlCreate
from api.config import get_settings
from api.database import get_session

hashids = Hashids(salt=get_settings().SALT, min_length=get_settings().MIN_LENGTH)


def create_shorturl(
    target_url: ShortUrlCreate, db: Session = Depends(get_session)
) -> ShortUrl:
    shorturl = ShortUrl(target_url=target_url.target_url)

    db.add(shorturl)
    db.flush()
    shorturl.short = hashids.encode(shorturl.id)
    db.commit()

    return shorturl


def read_all_urls(db: Session = Depends(get_session)) -> list[ShortUrl]:
    shorturls = db.query(ShortUrl).all()
    return shorturls


def read_url(shorturl: str, db: Session = Depends(get_session)) -> ShortUrl | None:
    decoded = hashids.decode(shorturl)
    if not decoded:
        return None
    id = decoded[0]

    db_shorturl = db.get(ShortUrl, id)

    return db_shorturl
