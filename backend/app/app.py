from fastapi import FastAPI
from  fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.databases.db import cursor
from app.model.model import home_Entity, home_Entitys

app = FastAPI()

# origins
origins = [
    "http://localhost:5173",
    "https://adminasimsaifi.netlify.app",
    "http://127.0.0.1:3000"
]

# make a bridge connection between frontend and admin <---> backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/home")
async def home():
    select_query = "SELECT * FROM logs"
    cursor.execute(select_query)
    data = cursor.fetchall()
    result = home_Entitys(data)
    print(len(result))
    cursor.execute("COMMIT")
    return JSONResponse(content=result, status_code=200)


