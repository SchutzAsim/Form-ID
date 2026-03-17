import mariadb
from fastapi import FastAPI
from  fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.databases.db import cursor, conn
from app.model.model import home_Entitys
from app.schema.schema import CreateLog

app = FastAPI()

# origins
origins = [
    "http://localhost:5173",
    "https://eshopmine.netlify.app/"
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
    conn.commit()
    return JSONResponse(content=result, status_code=200)


@app.post("/post")
async def data_post(row: CreateLog):
    print(row)
    try:
        # Data Insertion Query
        insert_query = f"INSERT INTO logs (Name, Contact, Service, Service_Type, Govt_Fee, Service_Charge, Total_Amount, Month, Created_At, Application_ID, Due) VALUES ('{row.Name}', '{row.Contact}', '{row.Service}', '{row.Service_Type}', '{row.Govt_Fee}', '{row.Service_Charge}', '{row.Total_Amount}', '{row.Month}', '{row.Created_At}', '{row.Application_ID}', '{row.Due}')"

        # Execute Query
        cursor.execute(insert_query)

        # Commit Table data
        conn.commit()

        return JSONResponse(content=f"Insertion Done Successfully!", status_code=201)
    except mariadb.Error as e:
        return JSONResponse(content=f"Insertion Failed! With Status Code {e}", status_code=500)

    finally:
        print("Insertion Done Successfully!")

