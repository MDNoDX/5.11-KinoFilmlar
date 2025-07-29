from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import RatingCreate, RatingResponse, FilmAverageResponse
from crud import create_rating, read_ratings, read_rate, update_rate, delete_rate, get_average_rating

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
async def create(rating: RatingCreate, db: AsyncSession = Depends(get_db)):
    return await create_rating(rating, db)

@router.get("/", response_model=list[RatingResponse])
async def get_all(limit: int = Query(100, ge=1), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db)):
    return await read_ratings(db, limit, offset)

@router.get("/{rating_id}", response_model=RatingResponse)
async def get_one(rating_id: int, db: AsyncSession = Depends(get_db)):
    return await read_rate(rating_id, db)

@router.put("/{rating_id}", response_model=RatingResponse)
async def update(rating_id: int, rating: RatingCreate, db: AsyncSession = Depends(get_db)):
    return await update_rate(rating_id, rating, db)

@router.delete("/{rating_id}")
async def delete(rating_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_rate(rating_id, db)

@router.get("/average/{film_id}", response_model=FilmAverageResponse)
async def average(film_id: int, db: AsyncSession = Depends(get_db)):
    return await get_average_rating(film_id, db)