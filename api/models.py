from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import HttpUrl


# class ShortUrl(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     target_url: str
#     short: Optional[str] = Field(default=None)
#     visits: Optional[int] = Field(default=0)


class ShortUrlBase(SQLModel):
    target_url: HttpUrl


class ShortUrl(ShortUrlBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    short: Optional[str] = Field(default=None)
    visits: Optional[int] = Field(default=0)


class ShortUrlCreate(ShortUrlBase):
    pass


class ShortUrlRead(ShortUrlBase):
    id: int
    short: str
    visits: int
    link: str


class ShortUrlLink(SQLModel):
    link: str
