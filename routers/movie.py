from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie
from fastapi import HTTPException, status

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str('Movie not found'))
    else:
        return JSONResponse(status_code = 200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_Length=5, max_Length=15), year:Optional[str] = Query(None, min_Length=4, max_Length=4)) -> List[Movie]:
    db = Session()
    if year is not None:
        result = MovieService(db).get_movies_by_category_and_year(category, year)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    else:
        result = MovieService(db).get_movies_by_category(category)
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)

    return JSONResponse(status_code=201, content={'message': 'Movie created sucessfully'})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()    
    result = MovieService(db).get_movie(id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str('Movie not found'))
    else:
        MovieService(db).update_movie(id, movie)
        return JSONResponse(status_code=200, content={'message': 'Movie updated successfully'})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str('Movie not found'))
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message': 'Movie removed successfully'})
