from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# Тимчасовий список фільмів (поки без реального парсингу)
movies = [
    {"id": 1, "title": "Dune 2", "category": "fantasy", "year": 2024, "url": "https://example.com/dune2.mp4"},
    {"id": 2, "title": "Reacher", "category": "action", "year": 2023, "url": "https://example.com/reacher.mp4"},
    {"id": 3, "title": "Rick and Morty", "category": "cartoon", "year": 2023, "url": "https://example.com/rick.mp4"},
]

@app.get("/api/latest")
def latest():
    return movies

@app.get("/api/search")
def search(q: str = Query(...)):
    result = [movie for movie in movies if q.lower() in movie["title"].lower()]
    return JSONResponse(content=result)

@app.get("/api/category")
def category(name: str = Query(...)):
    result = [movie for movie in movies if movie["category"] == name]
    return JSONResponse(content=result)
