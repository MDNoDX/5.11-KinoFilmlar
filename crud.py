from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models import Film, Rating
from schemas import FilmCreate, RatingCreate, FilmResponse, RatingResponse, FilmAverageResponse


# Flm

async def create_film(film: FilmCreate, db: AsyncSession) -> FilmResponse:
    new_film = Film(**film.model_dump())
    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return FilmResponse.model_validate(new_film)


async def read_films(db: AsyncSession, limit: int = 10, offset: int = 0) -> list[FilmResponse]:
    result = await db.execute(select(Film).offset(offset).limit(limit))
    films = result.scalars().all()

    film_responses = []
    for film in films:
        result = await db.execute(
            select(func.avg(Rating.score)).where(Rating.film_id == film.id)
        )
        avg = result.scalar()
        film.average_score = round(avg, 2) if avg else None
        film_responses.append(FilmResponse.model_validate(film))

    return film_responses


async def read_film(film_id: int, db: AsyncSession) -> FilmResponse:
    film = await db.get(Film, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    result = await db.execute(
        select(func.avg(Rating.score)).where(Rating.film_id == film_id)
    )
    avg = result.scalar()
    film.average_score = round(avg, 2) if avg else None

    return FilmResponse.model_validate(film)


async def update_film(film_id: int, film: FilmCreate, db: AsyncSession) -> FilmResponse:
    db_film = await db.get(Film, film_id)
    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    for key, value in film.model_dump().items():
        setattr(db_film, key, value)

    await db.commit()
    await db.refresh(db_film)
    return FilmResponse.model_validate(db_film)


async def delete_film(film_id: int, db: AsyncSession):
    db_film = await db.get(Film, film_id)
    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    await db.delete(db_film)
    await db.commit()
    return {"detail": "Film deleted"}


# Rating

async def create_rating(rating: RatingCreate, db: AsyncSession) -> RatingResponse:
    new_rating = Rating(**rating.model_dump())
    db.add(new_rating)
    await db.commit()
    await db.refresh(new_rating)
    return RatingResponse.model_validate(new_rating)


async def read_ratings(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[RatingResponse]:
    result = await db.execute(select(Rating).offset(offset).limit(limit))
    ratings = result.scalars().all()
    return [RatingResponse.model_validate(r) for r in ratings]


async def read_rate(rating_id: int, db: AsyncSession) -> RatingResponse:
    result = await db.execute(
        select(Rating).options(joinedload(Rating.film)).where(Rating.id == rating_id)
    )
    rating = result.scalar_one_or_none()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return RatingResponse.model_validate(rating)


async def update_rate(rating_id: int, rating: RatingCreate, db: AsyncSession) -> RatingResponse:
    db_rating = await db.get(Rating, rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    for key, value in rating.model_dump().items():
        setattr(db_rating, key, value)

    await db.commit()
    await db.refresh(db_rating)
    return RatingResponse.model_validate(db_rating)


async def delete_rate(rating_id: int, db: AsyncSession):
    db_rating = await db.get(Rating, rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    await db.delete(db_rating)
    await db.commit()
    return {"detail": "Rating deleted"}


# Average

async def get_average_rating(film_id: int, db: AsyncSession) -> FilmAverageResponse:
    film = await db.get(Film, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    result = await db.execute(
        select(func.avg(Rating.score)).where(Rating.film_id == film_id)
    )
    avg = result.scalar()

    return FilmAverageResponse(
        film_id=film.id,
        title=film.title,
        average_score=round(avg, 2) if avg else None
    )