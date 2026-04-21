from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/articles")
def get_articles():
    # membuka dan membaca JSON
    try:
        with open("wired_scraped_data.json","r", encoding="utf-8") as file:
            data =json.load(file)
        return data
    except FileNotFoundError:
        return {"error": "File wired_scraped_data.json belum tersedia."}