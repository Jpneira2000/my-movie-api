from fastapi import FastAPI, HTTPException, Body, Path, Query, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = 'Mi aplicación con FastAPI'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code = 403, detail = 'Credenciales inválidas')

class User(BaseModel):
    email:str
    password:str

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
                'id': 1,
                'title': 'El título de la película',
                'overview': 'Descripción de la película',
                'year': 'Año de lanzamiento de la película',
                'rating': 0.0,
                'category': 'Categoría de la película'
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planera llamado Pandora viven los Na'Vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planera llamado Pandora viven los Na'Vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello, World</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.model_dump())
    return JSONResponse(status_code = 200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        result = db.query(MovieModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    try:
        db = Session()
        result = db.query(MovieModel).filter(MovieModel.id == id).first()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if not result:
            raise HTTPException(status_code = 404, detail = 'Movie not found')
        return JSONResponse(status_code = 200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_Length=5, max_Length=15), year:Optional[str] = Query(None, min_Length=4, max_Length=4)) -> List[Movie]:
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        if year is not None:
            result = db.query(MovieModel).filter(MovieModel.category == category, MovieModel.year == year).all()
            
            if not result:
                raise HTTPException(status_code=404, detail = 'Not Found')
            else:
                return JSONResponse(status_code=200, content=jsonable_encoder(result))

        else:
            result = db.query(MovieModel).filter(MovieModel.category == category).all()
            
            if not result:
                raise HTTPException(status_code=404, detail = 'Not Found')
            else:
                return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        new_movie = MovieModel(**movie.model_dump())
        db.add(new_movie)
        db.commit()
        return JSONResponse(status_code=201, content={'message': 'Movie created sucessfully'})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail = 'Not Found')

    else:
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit()

        result = db.query(MovieModel).filter(MovieModel.id == id).first()
        return JSONResponse(status_code=200, content={'message': 'Movie updated successfully'})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail = 'Not Found')
    else:
        db.delete(result)
        db.commit()

        return JSONResponse(status_code=200, content={'message': 'Movie removed successfully'})
    