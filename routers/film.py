from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import FilmCreate, FilmResponse
from crud import create_film, read_films, read_film, update_film, delete_film

router = APIRouter(prefix="/films", tags=["Films"])

@router.post("/", response_model=FilmResponse)
async def create(film: FilmCreate, db: AsyncSession = Depends(get_db)):
    return await create_film(film, db)

@router.get("/", response_model=list[FilmResponse])
async def get_all(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db)):
    return await read_films(db, limit, offset)

@router.get("/{film_id}", response_model=FilmResponse)
async def get_one(film_id: int, db: AsyncSession = Depends(get_db)):
    return await read_film(film_id, db)

@router.put("/{film_id}", response_model=FilmResponse)
async def update(film_id: int, film: FilmCreate, db: AsyncSession = Depends(get_db)):
    return await update_film(film_id, film, db)

@router.delete("/{film_id}")
async def delete(film_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_film(film_id, db)