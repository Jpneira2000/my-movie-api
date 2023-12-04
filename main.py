from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = 'Mi aplicación con FastAPI'
app.version = '0.0.1'

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    raise HTTPException(status_code = 404, detail = 'Movie not found')

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year:str = None):
    if year is not None:

        return [ item for item in movies if item['category'] == category and item['year'] == year]

    else:
        return [ item for item in movies if item['category'] == category]

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies
