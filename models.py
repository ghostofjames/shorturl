from sqlalchemy import Column, Integer, String

from database import Base


class ShortUrl(Base):
    __tablename__ = "shorturls"

    id = Column(Integer, primary_key=True, index=True)
    short = Column(String)
    url = Column(String)
    visits = Column(Integer)

    def __str__(self) -> str:
        return str(self.__dict__)
