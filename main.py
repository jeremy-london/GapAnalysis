import os
import tomllib

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import ana

# Load environment variables
load_dotenv()


# Read version from pyproject.toml
def get_version():
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


app = FastAPI(title="LLM-KG-API", version=get_version())
app.include_router(ana.router)

@app.get("/")
async def read_main():
    return {"msg": "LLM-KG-API"}

# CORS Configuration
allow_origins = ["http://localhost:5173", "http://localhost:3000"]
allow_origin_regex = r"^https:\/\/(.*\.)?tryrecess\.vercel\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins if os.getenv("ENV") == "development" else [],
    allow_origin_regex=(
        None if os.getenv("ENV") == "development" else allow_origin_regex
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
