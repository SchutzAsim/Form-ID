# E-Shopmine
E-Shopmine is a privacy focus transcations manager system web app that will store all you data on your local computer.

## Project Structure
```bash

E-Shopmine
|
├── backend
│   ├── app
│   │   ├── app.py
│   │   ├── auth.py
│   │   ├── databases
│   │   │   ├── db.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── model
│   │   │   ├── __init__.py
│   │   │   └── model.py
│   │   ├── schema
│   │   │   ├── __init__.py
│   │   │   └── schema.py
│   │   └── Search
│   │       ├── __init__.py
│   │       └── search.py
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── __init__.py
│   ├── main.py
│   ├── pyproject.toml
│   └── uv.lock
|
└── Frontend
    ├── eslint.config.js
    ├── index.html
    ├── netlify.toml
    ├── package.json
    ├── package-lock.json
    ├── public
    │   ├── favicon.ico
    │   └── vite.svg
    ├── src
    │   ├── App.jsx
    │   ├── assets
    │   │   └── react.svg
    │   ├── components
    │   │   ├── CardForm.jsx
    │   │   ├── Home.jsx
    │   │   ├── LogForm.jsx
    │   │   ├── Login.jsx
    │   │   └── Nav.jsx
    │   ├── Context
    │   │   └── context.js
    │   ├── Main.css
    │   └── main.jsx
    └── vite.config.js

```
## Requirements
- MariaDB - for the data storage.
- Docker - for running the server without continuously.

## Prerequisites
#### Replace Value key word with your desire values (e.g. IP Address, Expiraction Time, Global Web URL, etc.)

- Place one .env file on backend folder with these variables values
    - Create a MariaDB account for enable docker intigration with the server with replace host with your IP Address.
    - Create a Secret key for JWT Token Validation.
    - Set Token Expiration Time in Minutes.

```bash
# Authentication Secrets
SECRET_KEY=Value
ALOGRITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=Value

# Server Configurations
SERVER_PORT=8181
SERVER_HOST=0.0.0.0
SERVER_RELOAD=True

# Database Configurations
DB_USER=Value
DB_PASSWORD=Value
DB_HOST=Value
DB_PORT=3306
DB_DATABASE=Value

# frontend server connection
self_connect=http://localhost:5173
local_connect=http://Value:5173
global_connect=Value
```
- Place Another one in Frontend Folder
```bash
# Backend API
VITE_API=http://localhost:8000
```

## Instalation
```bash
git clone https://github.com/SchutzAsim/E-Shopmine.git

cd E-Shopmine
```

### Start Python Server
```bash
cd backend

python -m venv .venv

source .venv/bin/activate

uv sync

python main.py
```

### Start Node.js Server
```bash
cd Frontend

npm run dev
```

## License

🚧 **License Pending** 🚧

This project will be open-sourced under a permissive license soon.
You are free to use this repo for learning & personal use.
For any query, please connect on [asimsaifioffical12@gmail.com] for permissions.