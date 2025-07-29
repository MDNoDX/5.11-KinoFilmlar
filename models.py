from typing import List, Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Film(Base):
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    year: Mapped[Optional[int]] = mapped_column(nullable=True)

    ratings: Mapped[List['Rating']] = relationship(
        back_populates='film',
        cascade='all, delete-orphan'
    )

class Rating(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey('films.id', ondelete='CASCADE'))
    score: Mapped[int] = mapped_column(Integer)

    film: Mapped[Film] = relationship(back_populates='ratings')