from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import requests

app = FastAPI()

def parse_rezka():
    url = "https://rezka.ag/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movie_list = []

    for item in soup.select(".b-content__inline_item"):
        title = item.select_one(".b-content__inline_item-link").text.strip()
        link = item.select_one(".b-content__inline_item-link")["href"]
        year_tag = item.select_one(".b-content__inline_item-link span")
        year = int(year_tag.text.strip()) if year_tag else None

        movie = {
            "title": title,
            "category": "unknown",
            "year": year,
            "url": link
        }
        movie_list.append(movie)

    return movie_list

@app.get("/api/latest")
def latest():
    return parse_rezka()

@app.get("/api/search")
def search(q: str = Query(...)):
    movies = parse_rezka()
    result = [movie for movie in movies if q.lower() in movie["title"].lower()]
    return JSONResponse(content=result)

@app.get("/api/category")
def category(name: str = Query(...)):
    movies = parse_rezka()
    result = [movie for movie in movies if movie["category"].lower() == name.lower()]
    return JSONResponse(content=result)
