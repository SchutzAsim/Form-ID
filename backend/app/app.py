import os
from typing import Annotated
from datetime import date
import mariadb
from fastapi import FastAPI, HTTPException, Depends
from  fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.databases.mongo import conn
from app.model.model import home_entitys
from app.Search.search import SimpleSearchIndex
from app.schema.schema import CreateLog, UpdateLog, UpdateDue
from app.auth import auth_router, get_current_active_user, User

load_dotenv()

# fetch know urls
self_connect = os.getenv("self_connect")
local_connect = os.getenv("local_connect")
global_connect = os.getenv("global_connect")

app = FastAPI()
app.include_router(auth_router)

# Current Active User Dependency for methods
current_active_user = Annotated[User, Depends(get_current_active_user)]

# origins
origins = [
    self_connect,
    local_connect,
    global_connect
]

# make a bridge connection between frontend and admin <---> backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DataBase Table Selection
table_name = 'logs' # if int(os.getenv("SERVER_PORT")) == 8181 else 'test_table'


# User Session
@app.get("/user/session")
def user_session(current_user: current_active_user):
    if current_user:
        return True
    return False


@app.get("/home")
async def get_logs(current_user: current_active_user):
    # fetch all rows
    docs = conn.Shop.logs.find()
    result = home_entitys(docs)

    if not result:
        raise HTTPException(status_code=404, detail="Data Not Found!")

    return JSONResponse(content=result[::-1], status_code=200)


@app.post("/post", response_model=CreateLog)
async def post_log(row: CreateLog, current_user: current_active_user):
    # Fix date format for mariadb date insertion
    new_doc_dict = row.model_dump()
    doc_date = f"{date.today()}" if row.Created_At.title() == 'Default' else f"'{row.Created_At}'"
    new_doc_dict["Created_At"] = doc_date
    try:
        doc_count = conn.Shop.logs.count_documents({})
        new_doc_dict["id_no"] = doc_count + 1

        # Insert New Doc
        new_doc = conn.Shop.logs.insert_one(new_doc_dict)
        print(new_doc)

        return JSONResponse(content=f"Insertion Done Successfully!", status_code=201)
    except mariadb.Error as e:
        return HTTPException(detail=f"Insertion Failed! With Status Code {e}", status_code=500)



@app.put("/post/update")
async def update_log(row: UpdateLog, current_user: current_active_user):
    # Fix date format for mariadb date insertion
    date = row.Created_At.capitalize() if row.Created_At.capitalize() == 'Default' else f"'{row.Created_At}'"

    # Checking the ID authenticity for updating
    if row.id > 0:
        try:
            # Getting ID is available or not
            find_query = f"SELECT * FROM {table_name} WHERE ID={row.id}"
            cursor.execute(find_query)
            find_data = cursor.fetchrows(row.id)

            # Update If given ID is available
            if len(find_data) == 1:
                # Build Query for updating the existing data row
                update_query = f"UPDATE {table_name} SET Name='{row.Name.title()}', Contact='{row.Contact}', Service='{row.Service.title()}', Service_Type='{row.Service_Type.title()}', Govt_Fee='{row.Govt_Fee}', Service_Charge='{row.Service_Charge}', Total_Amount='{row.Total_Amount}', Month='{row.Month.capitalize()}', Created_at={date}, Application_ID='{row.Application_ID}', Due='{row.Due}' WHERE ID={row.id}"

                # Execute update query
                cursor.execute(update_query)

                return JSONResponse(content=f"Log Updated Successfully at ID {row.id}")

            else:
                raise HTTPException(detail=f"Too many post ID {row.id} found", status_code=404)

        except mariadb.Error as e:
            raise HTTPException(detail=f"Couldn't able to update log at ID {row.id}: {e}", status_code=500)

        finally:
            # Commit Table data
            conn.commit()

    else:
        raise HTTPException(detail="Enter an ID that should be greater than 0!", status_code=400)


@app.put("/post/UpdateDue")
async def update_due(due_id: UpdateDue, current_user: current_active_user):
    # Store Due column ID
    find_id = due_id.id

    # ID Validation
    if find_id > 0:
        try:
            # Search Due ID
            search_id = f"SELECT id FROM {table_name} WHERE ID='{find_id}'"
            cursor.execute(search_id)
            validate_id = cursor.fetchrows(find_id)

            # Check Due ID availability
            if len(validate_id) == 1:
                # Update Due column Query
                update_query = f"UPDATE {table_name} SET DUE={due_id.Due} WHERE id='{find_id}'"

                # Run Due column update query
                cursor.execute(update_query)

                return JSONResponse(content=f"Due value updated at id {find_id}", status_code=200)
            else:
                raise HTTPException(status_code=404, detail=f"ID {find_id} for update Due not found!")

        except mariadb.Error as e:
            raise HTTPException(detail=f"Couldn't able to update ID {find_id} with error {e}", status_code=500)

        finally:
            # Commit Table Data
            conn.commit()

    else:
        raise HTTPException(detail=f"Enter ID should be greater than 0", status_code=400)


@app.get("/search/post/{query}")
async def search_row(query, current_user: current_active_user):
    try:
        search_engine = SimpleSearchIndex()
        # fetch all rows
        select_query = f"SELECT * FROM {table_name}"
        cursor.execute(select_query)
        data = cursor.fetchall()
        conn.commit()
        rows = home_entitys(data)

        searchTitles = ["Name", "Contact", "Application_ID", "Service", "Service_Type"]

        for row in rows:
            search_engine.add_to_index(searchTitles, row)

        filter_data = search_engine.search(query)
        result = home_entitys(filter_data)
        return JSONResponse(content=result[::-1], status_code=200)
    except:
        raise HTTPException(detail="Not Found", status_code=404)
