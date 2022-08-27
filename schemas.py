from pydantic import BaseModel, HttpUrl


class ShortUrlBase(BaseModel):
    url: HttpUrl


class ShortUrlCreate(ShortUrlBase):
    pass


class ShortUrl(ShortUrlBase):
    id: int
    visits: int
    short: str

    class Config:
        orm_mode = True
