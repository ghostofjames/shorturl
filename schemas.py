from pydantic import BaseModel, HttpUrl


class ShortUrlBase(BaseModel):
    url: HttpUrl


class ShortUrlCreate(ShortUrlBase):
    pass


class ShortUrl(ShortUrlBase):
    id: int
    visits: int

    class Config:
        orm_mode = True
