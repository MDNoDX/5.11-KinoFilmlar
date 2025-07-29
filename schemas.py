from pydantic import BaseModel, Field
from typing import Optional

class FilmCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    year: Optional[int] = Field(default=None, ge=1888, le=2100)

class FilmResponse(FilmCreate):
    id: int
    average_score: Optional[float] = None

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    film_id: int = Field(..., gt=0)
    score: int = Field(..., ge=1, le=10)

class RatingResponse(RatingCreate):
    id: int

    class Config:
        from_attributes = True

class FilmAverageResponse(BaseModel):
    film_id: int
    title: str
    average_score: Optional[float] = None