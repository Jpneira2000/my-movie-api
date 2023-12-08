from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: str = Field(min_length= 4, max_length=4)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'El título',
                'overview': 'Descripción de la película',
                'year': '2023',
                'rating': 7.0,
                'category': 'Categoría'
            }
        }