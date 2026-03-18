import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("SEVER_HOST")
port = int(os.getenv("SERVER_PORT"))
reload = bool(os.getenv("SERVER_RELOAD"))

if __name__ == "__main__":
    uvicorn.run(app="app.app:app",
                host=host,
                port=port,
                reload=reload
                )