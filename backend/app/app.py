from importlib.util import find_spec

import mariadb
from fastapi import FastAPI, HTTPException
from  fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.databases.db import cursor, conn
from app.model.model import home_Entitys
from app.schema.schema import CreateLog, UpdateLog

app = FastAPI()

# origins
origins = [
    "http://localhost:5173",
    "https://eshopmine.netlify.app"
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
async def get_logs():
    # fetch all rows
    select_query = "SELECT * FROM logs"
    cursor.execute(select_query)
    data = cursor.fetchall()
    result = home_Entitys(data)
    return JSONResponse(content=result, status_code=200)


@app.post("/post")
async def post_log(row: CreateLog):
    # Fix date format for mariadb date insertion
    date = row.Created_At if row.Created_At=='Default' else f'{row.Created_At}'
    try:
        # Data Insertion Query
        insert_query = f"INSERT INTO logs (Name, Contact, Service, Service_Type, Govt_Fee, Service_Charge, Total_Amount, Month, Created_At, Application_ID, Due) VALUES ('{row.Name}', '{row.Contact}', '{row.Service}', '{row.Service_Type}', '{row.Govt_Fee}', '{row.Service_Charge}', '{row.Total_Amount}', '{row.Month}', {date}, '{row.Application_ID}', '{row.Due}')"

        # Execute Query
        cursor.execute(insert_query)

        return JSONResponse(content=f"Insertion Done Successfully!", status_code=201)
    except mariadb.Error as e:
        return HTTPException(detail=f"Insertion Failed! With Status Code {e}", status_code=500)

    finally:
        # Commit Table data
        conn.commit()
        print("Data Commited Successfully")


@app.put("/post/update/")
async def update_log(row: UpdateLog):
    # Fix date format for mariadb date insertion
    date = row.Created_At if row.Created_At == 'Default' else f'{row.Created_At}'

    # Checking the ID authenticity for updating
    if row.id > 0:
        try:
            # Getting ID is available or not
            find_query = f"SELECT * FROM logs WHERE ID={row.id}"
            cursor.execute(find_query)
            find_data = cursor.fetchrows(row.id)

            # Update If given ID is available
            if len(find_data) == 1:
                # Build Query for updating the existing data row
                update_query = f"UPDATE logs SET Name='{row.Name}', Contact='{row.Contact}', Service='{row.Service}', Service_Type='{row.Service_Type}', Govt_Fee='{row.Govt_Fee}', Service_Charge='{row.Service_Charge}', Total_Amount='{row.Total_Amount}', Month='{row.Month}', Created_at='{date}', Application_ID='{row.Application_ID}', Due='{row.Due}' WHERE ID={row.id}"

                # Execute update query
                cursor.execute(update_query)

                return JSONResponse(content=f"Log Updated Successfully at ID {row.id}")

            else:
                raise HTTPException(detail=f"Entered ID {row.id} not found", status_code=404)

        except mariadb.Error as e:
            raise HTTPException(detail=f"Couldn't able to update log at ID {row.id}: {e}", status_code=500)

        finally:
            # Commit Table data
            conn.commit()
            print("Data Commited Successfully")

    else:
        raise HTTPException(detail="Enter an ID that should be greater than 0!", status_code=404)