import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

serverPort = int(os.getenv("SERVER_PORT"))


if __name__ == "__main__":
    uvicorn.run(app="app.auth_test_file:app",
                host="0.0.0.0",
                port=serverPort,
                reload=True
                )