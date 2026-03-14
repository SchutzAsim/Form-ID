from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.databases.db import cursor
from app.model.model import home_Entity, home_Entitys

app = FastAPI()

@app.get("/home")
async def home():
    select_query = "SELECT * FROM logs"
    cursor.execute(select_query)
    data = cursor.fetchall()
    result = home_Entitys(data)
    return JSONResponse(content=result, status_code=200)


